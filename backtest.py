import backtrader as bt
import matplotlib.pyplot as plt

class PandasData(bt.feeds.PandasData):
    lines = ('signal',)
    params = (('signal', -1),)

class MLSignalStrategy(bt.Strategy):
    def next(self):
        if self.position:
            return
        if self.data.signal[0] == 1:
            self.buy(size=100)
        elif self.data.signal[0] == -1:
            self.sell(size=100)

def run_backtest(df_bt):
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(10000)
    cerebro.broker.setcommission(commission=0.001)
    data = PandasData(dataname=df_bt)
    cerebro.adddata(data)
    cerebro.addstrategy(MLSignalStrategy)
    print("Capital initial:", cerebro.broker.getvalue())
    cerebro.run()
    print("Capital final:", cerebro.broker.getvalue())
    cerebro.plot(figsize=(15, 7))
