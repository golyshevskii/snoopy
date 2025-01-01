from core.scripts.exchange.base import Exchange, Divergence


class DIV(Divergence):
    def __init__(self, symbol: str, exchange: Exchange):
        """
        Params:
            symbol: "BTC_USDT"
            exchange: object Exchange (MEXCExchange)
        """
        super().__init__(symbol, exchange)

    async def find(self):
        klines = await self.exchange.fetch_futures_klines(
            symbol=self.symbol, interval=self.interval, start=self.start, end=self.end
        )

        results = {}
        # TODO: Calculate divergence

        return results
