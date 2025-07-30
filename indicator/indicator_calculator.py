import pandas as pd
import talib

class IndicatorCalculator:
    def __init__(self, df):
        self.df = df.copy()

    def apply_indicators(self, indicators=None, params=None):
        if indicators is None:
            return self.df
        if params is None:
            params = {}
        close = self.df["close"]
        high = self.df["high"]
        low = self.df["low"]
        volume = self.df["volume"]
        open_price = self.df["open"]

        # Overlap Studies
        if indicators.get("sma"):
            window = params.get('sma', {}).get('window', 20)
            self.df[f"sma_{window}"] = talib.SMA(close, timeperiod=window)
        if indicators.get("ema"):
            window = params.get('ema', {}).get('window', 20)
            self.df[f"ema_{window}"] = talib.EMA(close, timeperiod=window)
        if indicators.get("wma"):
            window = params.get('wma', {}).get('window', 20)
            self.df[f"wma_{window}"] = talib.WMA(close, timeperiod=window)
        if indicators.get("dema"):
            window = params.get('dema', {}).get('window', 20)
            self.df[f"dema_{window}"] = talib.DEMA(close, timeperiod=window)
        if indicators.get("tema"):
            window = params.get('tema', {}).get('window', 20)
            self.df[f"tema_{window}"] = talib.TEMA(close, timeperiod=window)
        if indicators.get("trima"):
            window = params.get('trima', {}).get('window', 30)
            self.df[f"trima_{window}"] = talib.TRIMA(close, timeperiod=window)
        if indicators.get("kama"):
            window = params.get('kama', {}).get('window', 30)
            self.df[f"kama_{window}"] = talib.KAMA(close, timeperiod=window)
        if indicators.get("t3"):
            window = params.get('t3', {}).get('window', 5)
            self.df[f"t3_{window}"] = talib.T3(close, timeperiod=window, vfactor=0.7)
        if indicators.get("midpoint"):
            window = params.get('midpoint', {}).get('window', 14)
            self.df[f"midpoint_{window}"] = talib.MIDPOINT(close, timeperiod=window)
        if indicators.get("bbands"):
            window = params.get('bbands', {}).get('window', 20)
            upper, middle, lower = talib.BBANDS(close, timeperiod=window, nbdevup=2, nbdevdn=2, matype=0)
            self.df["bb_upper"] = upper
            self.df["bb_middle"] = middle
            self.df["bb_lower"] = lower
        if indicators.get("mama"):
            self.df["mama"], self.df["fama"] = talib.MAMA(close, fastlimit=0.5, slowlimit=0.05)
        if indicators.get("mavp"):
            self.df["mavp"] = talib.MAVP(close, periods=close, minperiod=2, maxperiod=30)
        if indicators.get("midprice"):
            self.df["midprice"] = talib.MIDPRICE(high, low)
        if indicators.get("sar"):
            self.df["sar"] = talib.SAR(high, low, acceleration=0.02, maximum=0.2)
        if indicators.get("sarext"):
            self.df["sarext"] = talib.SAREXT(high, low, startvalue=0, offsetonreverse=0, accelerationinitlong=0.02, accelerationlong=0.02, accelerationmaxlong=0.2, accelerationinitshort=0.02, accelerationshort=0.02, accelerationmaxshort=0.2)

        # Momentum Indicators
        if indicators.get("adx"):
            window = params.get('adx', {}).get('window', 14)
            self.df["adx"] = talib.ADX(high, low, close, timeperiod=window)
        if indicators.get("adxr"):
            window = params.get('adxr', {}).get('window', 14)
            self.df["adxr"] = talib.ADXR(high, low, close, timeperiod=window)
        if indicators.get("aroon"):
            window = params.get('aroon', {}).get('window', 14)
            aroondown, aroonup = talib.AROON(high, low, timeperiod=window)
            self.df["aroon_down"] = aroondown
            self.df["aroon_up"] = aroonup
        if indicators.get("aroonosc"):
            window = params.get('aroonosc', {}).get('window', 14)
            self.df["aroonosc"] = talib.AROONOSC(high, low, timeperiod=window)
        if indicators.get("cci"):
            window = params.get('cci', {}).get('window', 14)
            self.df["cci"] = talib.CCI(high, low, close, timeperiod=window)
        if indicators.get("cmo"):
            window = params.get('cmo', {}).get('window', 14)
            self.df["cmo"] = talib.CMO(close, timeperiod=window)
        if indicators.get("dx"):
            window = params.get('dx', {}).get('window', 14)
            self.df["dx"] = talib.DX(high, low, close, timeperiod=window)
        if indicators.get("mfi"):
            window = params.get('mfi', {}).get('window', 14)
            self.df["mfi"] = talib.MFI(high, low, close, volume, timeperiod=window)
        if indicators.get("minus_di"):
            window = params.get('minus_di', {}).get('window', 14)
            self.df["minus_di"] = talib.MINUS_DI(high, low, close, timeperiod=window)
        if indicators.get("minus_dm"):
            window = params.get('minus_dm', {}).get('window', 14)
            self.df["minus_dm"] = talib.MINUS_DM(high, low, timeperiod=window)
        if indicators.get("plus_di"):
            window = params.get('plus_di', {}).get('window', 14)
            self.df["plus_di"] = talib.PLUS_DI(high, low, close, timeperiod=window)
        if indicators.get("plus_dm"):
            window = params.get('plus_dm', {}).get('window', 14)
            self.df["plus_dm"] = talib.PLUS_DM(high, low, timeperiod=window)
        if indicators.get("rsi"):
            window = params.get('rsi', {}).get('window', 14)
            self.df["rsi"] = talib.RSI(close, timeperiod=window)
        if indicators.get("trix"):
            window = params.get('trix', {}).get('window', 15)
            self.df["trix"] = talib.TRIX(close, timeperiod=window)
        if indicators.get("willr"):
            window = params.get('willr', {}).get('window', 14)
            self.df["williams_r"] = talib.WILLR(high, low, close, timeperiod=window)
        if indicators.get("apo"):
            self.df["apo"] = talib.APO(close, fastperiod=12, slowperiod=26)
        if indicators.get("bop"):
            self.df["bop"] = talib.BOP(open_price, high, low, close)
        if indicators.get("macd"):
            macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
            self.df["macd"] = macd
            self.df["macd_signal"] = macdsignal
            self.df["macd_hist"] = macdhist
        if indicators.get("macdext"):
            macd, macdsignal, macdhist = talib.MACDEXT(close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
            self.df["macdext"] = macd
            self.df["macdext_signal"] = macdsignal
            self.df["macdext_hist"] = macdhist
        if indicators.get("macdfix"):
            macd, macdsignal, macdhist = talib.MACDFIX(close, signalperiod=9)
            self.df["macdfix"] = macd
            self.df["macdfix_signal"] = macdsignal
            self.df["macdfix_hist"] = macdhist
        if indicators.get("ppo"):
            self.df["ppo"] = talib.PPO(close, fastperiod=12, slowperiod=26)
        if indicators.get("roc"):
            self.df["roc"] = talib.ROC(close, timeperiod=10)
        if indicators.get("rocp"):
            self.df["rocp"] = talib.ROCP(close, timeperiod=10)
        if indicators.get("rocr"):
            self.df["rocr"] = talib.ROCR(close, timeperiod=10)
        if indicators.get("rocr100"):
            self.df["rocr100"] = talib.ROCR100(close, timeperiod=10)
        if indicators.get("stoch"):
            slowk, slowd = talib.STOCH(high, low, close, fastk_period=5, slowk_period=3, slowd_period=3)
            self.df["stoch_k"] = slowk
            self.df["stoch_d"] = slowd
        if indicators.get("stochf"):
            fastk, fastd = talib.STOCHF(high, low, close, fastk_period=5, fastd_period=3)
            self.df["stochf_k"] = fastk
            self.df["stochf_d"] = fastd
        if indicators.get("stochrsi"):
            slowk, slowd = talib.STOCHRSI(close, timeperiod=14)
            self.df["stochrsi_k"] = slowk
            self.df["stochrsi_d"] = slowd

        # Volume Indicators
        if indicators.get("ad"):
            self.df["ad"] = talib.AD(high, low, close, volume)
        if indicators.get("adosc"):
            self.df["adosc"] = talib.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
        if indicators.get("obv"):
            self.df["obv"] = talib.OBV(close, volume)

        # Volatility Indicators
        if indicators.get("atr"):
            window = params.get('atr', {}).get('window', 14)
            self.df["atr"] = talib.ATR(high, low, close, timeperiod=window)
        if indicators.get("natr"):
            window = params.get('natr', {}).get('window', 14)
            self.df["natr"] = talib.NATR(high, low, close, timeperiod=window)
        if indicators.get("trange"):
            window = params.get('trange', {}).get('window', 14)
            self.df["true_range"] = talib.TRANGE(high, low, close)

        # Price Transform
        if indicators.get("avgprice"):
            self.df["avgprice"] = talib.AVGPRICE(open_price, high, low, close)
        if indicators.get("medprice"):
            self.df["medprice"] = talib.MEDPRICE(high, low)
        if indicators.get("typprice"):
            self.df["typprice"] = talib.TYPPRICE(high, low, close)
        if indicators.get("wclprice"):
            self.df["wclprice"] = talib.WCLPRICE(high, low, close)

        # Cycle Indicators
        if indicators.get("ht_dcperiod"):
            self.df["ht_dcperiod"] = talib.HT_DCPERIOD(close)
        if indicators.get("ht_dcphase"):
            self.df["ht_dcphase"] = talib.HT_DCPHASE(close)
        if indicators.get("ht_phasor"):
            inphase, quadrature = talib.HT_PHASOR(close)
            self.df["ht_phasor_inphase"] = inphase
            self.df["ht_phasor_quadrature"] = quadrature
        if indicators.get("ht_sine"):
            sine, leadsine = talib.HT_SINE(close)
            self.df["ht_sine"] = sine
            self.df["ht_leadsine"] = leadsine
        if indicators.get("ht_trendmode"):
            self.df["ht_trendmode"] = talib.HT_TRENDMODE(close)

        # Pattern Recognition
        for ind in indicators:
            if ind.startswith('cdl') and indicators.get(ind):
                self.df[ind] = getattr(talib, ind.upper())(open_price, high, low, close)

        return self.df.dropna(how='any')