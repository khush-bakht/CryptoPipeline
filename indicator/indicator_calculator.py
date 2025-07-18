#indicator/indicator/calculator.py
import talib

class IndicatorCalculator:
    def __init__(self, df):
        self.df = df

    def apply_indicators(self, indicators=None):
        close = self.df["close"]
        high = self.df["high"]
        low = self.df["low"]
        volume = self.df["volume"]
        open_price = self.df["open"]  

        if not indicators:
            return self.df

        # Overlap Studies
        if indicators.get("sma"):
            self.df["sma_20"] = talib.SMA(close, timeperiod=20)
        if indicators.get("ema"):
            self.df["ema_20"] = talib.EMA(close, timeperiod=20)
        if indicators.get("dema"):
            self.df["dema_20"] = talib.DEMA(close, timeperiod=20)
        if indicators.get("tema"):
            self.df["tema_20"] = talib.TEMA(close, timeperiod=20)
        if indicators.get("trima"):
            self.df["trima_20"] = talib.TRIMA(close, timeperiod=20)
        if indicators.get("kama"):
            self.df["kama_20"] = talib.KAMA(close, timeperiod=20)
        if indicators.get("mama"):
            self.df["mama"], self.df["fama"] = talib.MAMA(close, fastlimit=0.5, slowlimit=0.05)
        if indicators.get("mavp"):
            self.df["mavp"] = talib.MAVP(close, periods=close, minperiod=2, maxperiod=30)
        if indicators.get("midpoint"):
            self.df["midpoint_20"] = talib.MIDPOINT(close, timeperiod=20)
        if indicators.get("midprice"):
            self.df["midprice"] = talib.MIDPRICE(high, low)
        if indicators.get("sar"):
            self.df["sar"] = talib.SAR(high, low, acceleration=0.02, maximum=0.2)
        if indicators.get("sarext"):
            self.df["sarext"] = talib.SAREXT(high, low, startvalue=0, offsetonreverse=0, accelerationinitlong=0.02, accelerationlong=0.02, accelerationmaxlong=0.2, accelerationinitshort=0.02, accelerationshort=0.02, accelerationmaxshort=0.2)
        if indicators.get("t3"):
            self.df["t3_20"] = talib.T3(close, timeperiod=20, vfactor=0.7)
        if indicators.get("wma"):
            self.df["wma_20"] = talib.WMA(close, timeperiod=20)
        if indicators.get("bbands"):
            upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
            self.df["bb_upper"] = upper
            self.df["bb_middle"] = middle
            self.df["bb_lower"] = lower

        # Momentum Indicators
        if indicators.get("adx"):
            self.df["adx"] = talib.ADX(high, low, close, timeperiod=14)
        if indicators.get("adxr"):
            self.df["adxr"] = talib.ADXR(high, low, close, timeperiod=14)
        if indicators.get("apo"):
            self.df["apo"] = talib.APO(close, fastperiod=12, slowperiod=26)
        if indicators.get("aroon"):
            aroondown, aroonup = talib.AROON(high, low, timeperiod=14)
            self.df["aroon_down"] = aroondown
            self.df["aroon_up"] = aroonup
        if indicators.get("aroonosc"):
            self.df["aroonosc"] = talib.AROONOSC(high, low, timeperiod=14)
        if indicators.get("bop"):
            self.df["bop"] = talib.BOP(open_price, high, low, close)
        if indicators.get("cci"):
            self.df["cci"] = talib.CCI(high, low, close, timeperiod=14)
        if indicators.get("cmo"):
            self.df["cmo"] = talib.CMO(close, timeperiod=14)
        if indicators.get("dx"):
            self.df["dx"] = talib.DX(high, low, close, timeperiod=14)
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
        if indicators.get("mfi"):
            self.df["mfi"] = talib.MFI(high, low, close, volume, timeperiod=14)
        if indicators.get("minus_di"):
            self.df["minus_di"] = talib.MINUS_DI(high, low, close, timeperiod=14)
        if indicators.get("minus_dm"):
            self.df["minus_dm"] = talib.MINUS_DM(high, low, timeperiod=14)
        if indicators.get("mom"):
            self.df["momentum"] = talib.MOM(close, timeperiod=10)
        if indicators.get("plus_di"):
            self.df["plus_di"] = talib.PLUS_DI(high, low, close, timeperiod=14)
        if indicators.get("plus_dm"):
            self.df["plus_dm"] = talib.PLUS_DM(high, low, timeperiod=14)
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
        if indicators.get("rsi"):
            self.df["rsi"] = talib.RSI(close, timeperiod=14)
        if indicators.get("stoch"):
            slowk, slowd = talib.STOCH(high, low, close, fastk_period=5, slowk_period=3, slowd_period=3)
            self.df["stoch_k"] = slowk
            self.df["stoch_d"] = slowd
        if indicators.get("stochf"):
            fastk, fastd = talib.STOCHF(high, low, close, fastk_period=5, fastd_period=3)
            self.df["stochf_k"] = fastk
            self.df["stochf_d"] = fastd
        if 'stochrsi' in indicators:
            slowk, slowd = talib.STOCHRSI(close, timeperiod=14)
            self.df["stochrsi_k"] = slowk
            self.df["stochrsi_d"] = slowd

        if indicators.get("trix"):
            self.df["trix"] = talib.TRIX(close, timeperiod=15)
        if indicators.get("ultosc"):
            self.df["ultosc"] = talib.ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
        if indicators.get("willr"):
            self.df["williams_r"] = talib.WILLR(high, low, close, timeperiod=14)

        # Volume Indicators
        if indicators.get("ad"):
            self.df["ad"] = talib.AD(high, low, close, volume)
        if indicators.get("adosc"):
            self.df["adosc"] = talib.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
        if indicators.get("obv"):
            self.df["obv"] = talib.OBV(close, volume)

        # Volatility Indicators
        if indicators.get("atr"):
            self.df["atr"] = talib.ATR(high, low, close, timeperiod=14)
        if indicators.get("natr"):
            self.df["natr"] = talib.NATR(high, low, close, timeperiod=14)
        if indicators.get("trange"):
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
        if indicators.get("cdl2crows"):
            self.df["cdl2crows"] = talib.CDL2CROWS(open_price, high, low, close)
        if indicators.get("cdl3blackcrows"):
            self.df["cdl3blackcrows"] = talib.CDL3BLACKCROWS(open_price, high, low, close)
        if indicators.get("cdl3inside"):
            self.df["cdl3inside"] = talib.CDL3INSIDE(open_price, high, low, close)
        if indicators.get("cdl3linestrike"):
            self.df["cdl3linestrike"] = talib.CDL3LINESTRIKE(open_price, high, low, close)
        if indicators.get("cdl3outside"):
            self.df["cdl3outside"] = talib.CDL3OUTSIDE(open_price, high, low, close)
        if indicators.get("cdl3starsinsouth"):
            self.df["cdl3starsinsouth"] = talib.CDL3STARSINSOUTH(open_price, high, low, close)
        if indicators.get("cdl3whitesoldiers"):
            self.df["cdl3whitesoldiers"] = talib.CDL3WHITESOLDIERS(open_price, high, low, close)
        if indicators.get("cdlabandonedbaby"):
            self.df["cdlabandonedbaby"] = talib.CDLABANDONEDBABY(open_price, high, low, close)
        if indicators.get("cdladvanceblock"):
            self.df["cdladvanceblock"] = talib.CDLADVANCEBLOCK(open_price, high, low, close)
        if indicators.get("cdlbelthold"):
            self.df["cdlbelthold"] = talib.CDLBELTHOLD(open_price, high, low, close)
        if indicators.get("cdlbreakaway"):
            self.df["cdlbreakaway"] = talib.CDLBREAKAWAY(open_price, high, low, close)
        if indicators.get("cdlclosingmarubozu"):
            self.df["cdlclosingmarubozu"] = talib.CDLCLOSINGMARUBOZU(open_price, high, low, close)
        if indicators.get("cdlconcealbabyswall"):
            self.df["cdlconcealbabyswall"] = talib.CDLCONCEALBABYSWALL(open_price, high, low, close)
        if indicators.get("cdlcounterattack"):
            self.df["cdlcounterattack"] = talib.CDLCOUNTERATTACK(open_price, high, low, close)
        if indicators.get("cdldarkcloudcover"):
            self.df["cdldarkcloudcover"] = talib.CDLDARKCLOUDCOVER(open_price, high, low, close)
        if indicators.get("cdldoji"):
            self.df["cdldoji"] = talib.CDLDOJI(open_price, high, low, close)
        if indicators.get("cdldojistar"):
            self.df["cdldojistar"] = talib.CDLDOJISTAR(open_price, high, low, close)
        if indicators.get("cdldragonflydoji"):
            self.df["cdldragonflydoji"] = talib.CDLDRAGONFLYDOJI(open_price, high, low, close)
        if indicators.get("cdlengulfing"):
            self.df["cdlengulfing"] = talib.CDLENGULFING(open_price, high, low, close)
        if indicators.get("cdleveningdojistar"):
            self.df["cdleveningdojistar"] = talib.CDLEVENINGDOJISTAR(open_price, high, low, close)
        if indicators.get("cdleveningstar"):
            self.df["cdleveningstar"] = talib.CDLEVENINGSTAR(open_price, high, low, close)
        if indicators.get("cdlgapsidesidewhite"):
            self.df["cdlgapsidesidewhite"] = talib.CDLGAPSIDESIDEWHITE(open_price, high, low, close)
        if indicators.get("cdlgravestonedoji"):
            self.df["cdlgravestonedoji"] = talib.CDLGRAVESTONEDOJI(open_price, high, low, close)
        if indicators.get("cdlhammer"):
            self.df["cdlhammer"] = talib.CDLHAMMER(open_price, high, low, close)
        if indicators.get("cdlhangingman"):
            self.df["cdlhangingman"] = talib.CDLHANGINGMAN(open_price, high, low, close)
        if indicators.get("cdlharami"):
            self.df["cdlharami"] = talib.CDLHARAMI(open_price, high, low, close)
        if indicators.get("cdlharamicross"):
            self.df["cdlharamicross"] = talib.CDLHARAMICROSS(open_price, high, low, close)
        if indicators.get("cdlhighwave"):
            self.df["cdlhighwave"] = talib.CDLHIGHWAVE(open_price, high, low, close)
        if indicators.get("cdlhikkake"):
            self.df["cdlhikkake"] = talib.CDLHIKKAKE(open_price, high, low, close)
        if indicators.get("cdlhikkakemod"):
            self.df["cdlhikkakemod"] = talib.CDLHIKKAKEMOD(open_price, high, low, close)
        if indicators.get("cdlidentical3crows"):
            self.df["cdlidentical3crows"] = talib.CDLIDENTICAL3CROWS(open_price, high, low, close)
        if indicators.get("cdlinneck"):
            self.df["cdlinneck"] = talib.CDLINNECK(open_price, high, low, close)
        if indicators.get("cdlinvertedhammer"):
            self.df["cdlinvertedhammer"] = talib.CDLINVERTEDHAMMER(open_price, high, low, close)
        if indicators.get("cdlkicking"):
            self.df["cdlkicking"] = talib.CDLKICKING(open_price, high, low, close)
        if indicators.get("cdlkickingbylength"):
            self.df["cdlkickingbylength"] = talib.CDLKICKINGBYLENGTH(open_price, high, low, close)
        if indicators.get("cdlladderbottom"):
            self.df["cdlladderbottom"] = talib.CDLLADDERBOTTOM(open_price, high, low, close)
        if indicators.get("cdllongleggeddoji"):
            self.df["cdllongleggeddoji"] = talib.CDLLONGLEGGEDDOJI(open_price, high, low, close)
        if indicators.get("cdllongline"):
            self.df["cdllongline"] = talib.CDLLONGLINE(open_price, high, low, close)
        if indicators.get("cdlmarubozu"):
            self.df["cdlmarubozu"] = talib.CDLMARUBOZU(open_price, high, low, close)
        if indicators.get("cdlmatchinglow"):
            self.df["cdlmatchinglow"] = talib.CDLMATCHINGLOW(open_price, high, low, close)
        if indicators.get("cdlonneck"):
            self.df["cdlonneck"] = talib.CDLONNECK(open_price, high, low, close)
        if indicators.get("cdlpiercing"):
            self.df["cdlpiercing"] = talib.CDLPIERCING(open_price, high, low, close)
        if indicators.get("cdlrickshawman"):
            self.df["cdlrickshawman"] = talib.CDLRICKSHAWMAN(open_price, high, low, close)
        if indicators.get("cdlrisefall3methods"):
            self.df["cdlrisefall3methods"] = talib.CDLRISEFALL3METHODS(open_price, high, low, close)
        if indicators.get("cdlseparatinglines"):
            self.df["cdlseparatinglines"] = talib.CDLSEPARATINGLINES(open_price, high, low, close)
        if indicators.get("cdlshootingstar"):
            self.df["cdlshootingstar"] = talib.CDLSHOOTINGSTAR(open_price, high, low, close)
        if indicators.get("cdlshortline"):
            self.df["cdlshortline"] = talib.CDLSHORTLINE(open_price, high, low, close)
        if indicators.get("cdlspinningtop"):
            self.df["cdlspinningtop"] = talib.CDLSPINNINGTOP(open_price, high, low, close)
        if indicators.get("cdlstalledpattern"):
            self.df["cdlstalledpattern"] = talib.CDLSTALLEDPATTERN(open_price, high, low, close)
        if indicators.get("cdlsticksandwich"):
            self.df["cdlsticksandwich"] = talib.CDLSTICKSANDWICH(open_price, high, low, close)
        if indicators.get("cdltakuri"):
            self.df["cdltakuri"] = talib.CDLTAKURI(open_price, high, low, close)
        if indicators.get("cdltasukigap"):
            self.df["cdltasukigap"] = talib.CDLTASUKIGAP(open_price, high, low, close)
        if indicators.get("cdlthrusting"):
            self.df["cdlthrusting"] = talib.CDLTHRUSTING(open_price, high, low, close)
        if indicators.get("cdltristar"):
            self.df["cdltristar"] = talib.CDLTRISTAR(open_price, high, low, close)
        if indicators.get("cdlunique3river"):
            self.df["cdlunique3river"] = talib.CDLUNIQUE3RIVER(open_price, high, low, close)
        if indicators.get("cdlupsidegap2crows"):
            self.df["cdlupsidegap2crows"] = talib.CDLUPSIDEGAP2CROWS(open_price, high, low, close)
        if indicators.get("cdlxsidegap3methods"):
            self.df["cdlxsidegap3methods"] = talib.CDLXSIDEGAP3METHODS(open_price, high, low, close)

        return self.df