import psycopg2
import sshtunnel
import pandas as pd
from typing import Any, Dict, List, Tuple, Union
from psycopg2.extras import execute_batch
from sqlalchemy import create_engine, text

from logs.logger import get_logger
from core.scripts.tools.files import read_file


logger = get_logger(__name__)


class PSQLClient:
    """
    Class for working with PostgreSQL database

    Attributes:
        conn_str: connection string. Used for direct connection
        conn_params: connection parameters. Used for SSH connection
        ssh_params: SSH connection parameters
        ssh_tunnel: SSH tunnel
        engine: SQLAlchemy engine for working with queries

        CONN_STR_PATTERN: connection string pattern. Used for SSH connection
    """

    CONN_STR_PATTERN = "postgresql://%(username)s:%(password)s@%(host)s:%(port)d/%(db)s"

    def __init__(
        self,
        conn_str: str = None,
        username: str = None,
        password: str = None,
        db: str = None,
        ssh_address_or_host: Tuple = None,
        ssh_username: str = None,
        ssh_pkey: str = None,
        local_bind_address: Tuple = None,
        remote_bind_address: Tuple = None,
    ):
        """
        Params:
            conn_str: PSQL connection string.
                Use it if you want to connect to PSQL directly (not through SSH)
            username: PSQL username
            password: PSQL password
            db: PSQL database

            ssh_address_or_host: SSH address or host. For example: ("11.222.33.44", 22)
            ssh_username: SSH username
            ssh_pkey: SSH private key str or path to the private key file
            remote_bind_address: Remote bind address. For example: ("11.222.3.4", 5432)
        """
        self.conn_str = conn_str
        self.conn_params = {"username": username, "password": password, "host": None, "port": None, "db": db}

        self.ssh_params = {
            "ssh_address_or_host": ssh_address_or_host,
            "ssh_username": ssh_username,
            "ssh_pkey": ssh_pkey,
            "local_bind_address": local_bind_address,
            "remote_bind_address": remote_bind_address,
        }
        self.ssh_tunnel = None
        self.engine = None

    def execute(
        self, sql: str, select: bool = False, format: Dict[str, Any] = None
    ) -> Union[pd.DataFrame, None]:
        """
        Executes SQL query

        Params:
            sql: SQL query or path to the SQL file
            select: if True, returns the result of the query as a DataFrame
            format: additional parameters for the SQL query
        """
        if sql.endswith(".sql"):
            sql = read_file(sql)

        if format:
            sql = sql.format(**format)

        self._connect()
        with self.engine.connect() as connection:
            data = None

            if select:
                data = pd.read_sql(sql=text(sql), con=connection)
                logger.info(f"Data has been extracted. Shape: {data.shape}")
            else:
                result = connection.execute(text(sql))
                logger.info(f"SQL has been executed. Effected rows: {result.rowcount}")
        self._disconnect()

        return data

    def insert(
        self,
        schema: str,
        table: str,
        data: List[dict],
        on_conflict_do_nothing: bool = False,
        on_conflict_do_update: bool = False,
        constraint: str = None,
        pkeys: List[str] = None,
        row_buffer: int = 50000,
    ):
        """
        Inserts a specific size batch of data into PostgreSQL table

        Params:
            schema: schema name
            table: table name
            data: a list of dictionaries representing the data
            on_conflict_do_nothing: if True, the ON CONFLICT DO NOTHING method will be used
            on_conflict_do_update: if True, the ON CONFLICT DO UPDATE SET method will be used

            ! One of the following parameters must be provided if we want to use on conflict methods:
            constraint: the name of the constraint for the
                ON CONFLICT ON CONSTRAINT constraint DO UPDATE SET clause
            pkeys: the primary keys of the table wich will be used in the
                ON CONFLICT (pkeys) DO UPDATE SET clause

            row_buffer: the number of rows to be inserted in each batch
        """

        SQL = self._get_insert_query(
            schema=schema,
            table=table,
            data=data,
            do_nothing=on_conflict_do_nothing,
            do_update=on_conflict_do_update,
            constraint=constraint,
            pkeys=pkeys,
        )

        self._connect()
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                execute_batch(cursor, SQL, data, page_size=row_buffer)
                conn.commit()
        self._disconnect()

        logger.info(f"Rows have been inserted (updated): {len(data)}")

    def _get_insert_query(
        self,
        schema: str,
        table: str,
        data: List[dict],
        do_nothing: bool = False,
        do_update: bool = False,
        constraint: str = None,
        pkeys: List[str] = None,
    ) -> str:
        """Returns the insert query, depending on the parameters"""
        columns = list(data[0].keys())
        attributes = ",".join(columns)

        values = ["%({0})s".format(column) for column in columns]
        values = ",".join(values)

        on_conflict_clause, action = "", ""
        if do_update or do_nothing:
            on_conflict_clause = "ON CONFLICT " + (
                f"({','.join(pkeys)})" if pkeys else f"ON CONSTRAINT {constraint}"
            )

            action = "DO NOTHING"
            if do_update:
                duplicates = ["{0}=%({0})s".format(column) for column in columns]
                duplicates = ",".join(duplicates)

                action = f"DO UPDATE SET {duplicates}"

        SQL = f"""
        INSERT INTO {schema}.{table} ({attributes})
        VALUES ({values})
        {on_conflict_clause}
        {action};
        """
        return SQL

    def _open_sshtunnel(self):
        """Creates SSH tunnel to the server"""
        self.ssh_tunnel = sshtunnel.SSHTunnelForwarder(**self.ssh_params)
        self.ssh_tunnel.start()

        self.conn_params["host"] = self.ssh_tunnel.local_bind_host
        self.conn_params["port"] = self.ssh_tunnel.local_bind_port

    def _connect(self):
        """Connects to the PSQL database"""
        try:
            if not self.conn_str:
                self._open_sshtunnel()
                self.conn_str = self.CONN_STR_PATTERN % self.conn_params

            self.engine = create_engine(self.conn_str)
        except Exception as e:
            logger.error(f"Failed to connect to the PSQL database\n{e}")
            self._disconnect()
            raise e

    def _disconnect(self):
        """Closes SSH tunnel"""
        if self.ssh_tunnel:
            self.ssh_tunnel.stop()
