from datetime import datetime, timedelta, timezone

INTERVALS = [15, 30, 60, 240]


def get_first_run_time(interval_minutes: int) -> datetime:
    now = datetime.now(timezone.utc)
    run_dtt = (now + timedelta(minutes=interval_minutes - now.minute % interval_minutes)).replace(
        second=0, microsecond=0
    )
    return run_dtt
