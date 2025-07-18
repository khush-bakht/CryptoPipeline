#signals/technical_indicator_signal/signal_generator.py
import pandas as pd
import numpy as np

class SignalGenerator:
    def __init__(self, df):
        self.df = df.copy()

    def generate_signals(self):
        df = self.df

        #Signal columns list
        signal_cols = []

        def has_cols(*cols):
            return all(col in df.columns for col in cols)

        # Overlap Studies
        if 'sma_20' in df.columns:
            df['signal_sma_20'] = np.where(df['close'] > df['sma_20'], 1,
                                    np.where(df['close'] < df['sma_20'], -1, 0))
            signal_cols.append('signal_sma_20')
        if 'ema_20' in df.columns:
            df['signal_ema_20'] = np.where(df['close'] > df['ema_20'], 1,
                                    np.where(df['close'] < df['ema_20'], -1, 0))
            signal_cols.append('signal_ema_20')
        if 'dema_20' in df.columns:
            df['signal_dema_20'] = np.where(df['close'] > df['dema_20'], 1,
                                     np.where(df['close'] < df['dema_20'], -1, 0))
            signal_cols.append('signal_dema_20')
        if 'tema_20' in df.columns:
            df['signal_tema_20'] = np.where(df['close'] > df['tema_20'], 1,
                                     np.where(df['close'] < df['tema_20'], -1, 0))
            signal_cols.append('signal_tema_20')
        if 'trima_20' in df.columns:
            df['signal_trima_20'] = np.where(df['close'] > df['trima_20'], 1,
                                      np.where(df['close'] < df['trima_20'], -1, 0))
            signal_cols.append('signal_trima_20')
        if 'kama_20' in df.columns:
            df['signal_kama_20'] = np.where(df['close'] > df['kama_20'], 1,
                                     np.where(df['close'] < df['kama_20'], -1, 0))
            signal_cols.append('signal_kama_20')
        if 'mama' in df.columns and 'fama' in df.columns:
            df['signal_mama'] = np.where(df['close'] > df['mama'], 1,
                                  np.where(df['close'] < df['fama'], -1, 0))
            signal_cols.append('signal_mama')
        if 'mavp' in df.columns:
            df['signal_mavp'] = np.where(df['close'] > df['mavp'], 1,
                                  np.where(df['close'] < df['mavp'], -1, 0))
            signal_cols.append('signal_mavp')
        if 'midpoint_20' in df.columns:
            df['signal_midpoint_20'] = np.where(df['close'] > df['midpoint_20'], 1,
                                         np.where(df['close'] < df['midpoint_20'], -1, 0))
            signal_cols.append('signal_midpoint_20')
        if 'midprice' in df.columns:
            df['signal_midprice'] = np.where(df['close'] > df['midprice'], 1,
                                      np.where(df['close'] < df['midprice'], -1, 0))
            signal_cols.append('signal_midprice')
        if 'sar' in df.columns:
            df['signal_sar'] = np.where(df['close'] > df['sar'], 1,
                                 np.where(df['close'] < df['sar'], -1, 0))
            signal_cols.append('signal_sar')
        if 'sarext' in df.columns:
            df['signal_sarext'] = np.where(df['close'] > df['sarext'], 1,
                                    np.where(df['close'] < df['sarext'], -1, 0))
            signal_cols.append('signal_sarext')
        if 't3_20' in df.columns:
            df['signal_t3_20'] = np.where(df['close'] > df['t3_20'], 1,
                                   np.where(df['close'] < df['t3_20'], -1, 0))
            signal_cols.append('signal_t3_20')
        if 'wma_20' in df.columns:
            df['signal_wma_20'] = np.where(df['close'] > df['wma_20'], 1,
                                    np.where(df['close'] < df['wma_20'], -1, 0))
            signal_cols.append('signal_wma_20')
        if has_cols('bb_upper', 'bb_lower'):
            df['signal_bb'] = np.where(df['close'] > df['bb_upper'], -1,
                                np.where(df['close'] < df['bb_lower'], 1, 0))
            signal_cols.append('signal_bb')

        # Momentum Indicators
        if 'adx' in df.columns:
            df['signal_adx'] = np.where(df['adx'] > 25, 1, 0)
            signal_cols.append('signal_adx')
        if 'adxr' in df.columns:
            df['signal_adxr'] = np.where(df['adxr'] > 25, 1, 0)
            signal_cols.append('signal_adxr')
        if 'apo' in df.columns:
            df['signal_apo'] = np.where(df['apo'] > 0, 1,
                                 np.where(df['apo'] < 0, -1, 0))
            signal_cols.append('signal_apo')
        if has_cols('aroon_up', 'aroon_down'):
            df['signal_aroon'] = np.where(df['aroon_up'] > df['aroon_down'], 1,
                                   np.where(df['aroon_up'] < df['aroon_down'], -1, 0))
            signal_cols.append('signal_aroon')
        if 'aroonosc' in df.columns:
            df['signal_aroonosc'] = np.where(df['aroonosc'] > 0, 1,
                                     np.where(df['aroonosc'] < 0, -1, 0))
            signal_cols.append('signal_aroonosc')
        if 'bop' in df.columns:
            df['signal_bop'] = np.where(df['bop'] > 0, 1,
                                 np.where(df['bop'] < 0, -1, 0))
            signal_cols.append('signal_bop')
        if 'cci' in df.columns:
            df['signal_cci'] = np.where(df['cci'] > 100, 1,
                                 np.where(df['cci'] < -100, -1, 0))
            signal_cols.append('signal_cci')
        if 'cmo' in df.columns:
            df['signal_cmo'] = np.where(df['cmo'] > 50, 1,
                                 np.where(df['cmo'] < 50, -1, 0))
            signal_cols.append('signal_cmo')
        if 'dx' in df.columns:
            df['signal_dx'] = np.where(df['dx'] > 25, 1, 0)
            signal_cols.append('signal_dx')
        if has_cols('macd', 'macd_signal'):
            df['signal_macd'] = np.where(df['macd'] > df['macd_signal'], 1,
                                  np.where(df['macd'] < df['macd_signal'], -1, 0))
            signal_cols.append('signal_macd')
        if has_cols('macdext', 'macdext_signal'):
            df['signal_macdext'] = np.where(df['macdext'] > df['macdext_signal'], 1,
                                     np.where(df['macdext'] < df['macdext_signal'], -1, 0))
            signal_cols.append('signal_macdext')
        if has_cols('macdfix', 'macdfix_signal'):
            df['signal_macdfix'] = np.where(df['macdfix'] > df['macdfix_signal'], 1,
                                     np.where(df['macdfix'] < df['macdfix_signal'], -1, 0))
            signal_cols.append('signal_macdfix')
        if 'mfi' in df.columns:
            df['signal_mfi'] = np.where(df['mfi'] > 80, -1,
                                 np.where(df['mfi'] < 20, 1, 0))
            signal_cols.append('signal_mfi')
        if 'minus_di' in df.columns:
            df['signal_minus_di'] = np.where(df['minus_di'] > 25, -1, 0)
            signal_cols.append('signal_minus_di')
        if 'minus_dm' in df.columns:
            df['signal_minus_dm'] = np.where(df['minus_dm'] > 25, -1, 0)
            signal_cols.append('signal_minus_dm')
        if 'mom' in df.columns:
            df['signal_mom'] = np.where(df['momentum'] > 0, 1,
                                 np.where(df['momentum'] < 0, -1, 0))
            signal_cols.append('signal_mom')
        if 'plus_di' in df.columns:
            df['signal_plus_di'] = np.where(df['plus_di'] > 25, 1, 0)
            signal_cols.append('signal_plus_di')
        if 'plus_dm' in df.columns:
            df['signal_plus_dm'] = np.where(df['plus_dm'] > 25, 1, 0)
            signal_cols.append('signal_plus_dm')
        if 'ppo' in df.columns:
            df['signal_ppo'] = np.where(df['ppo'] > 0, 1,
                                 np.where(df['ppo'] < 0, -1, 0))
            signal_cols.append('signal_ppo')
        if 'roc' in df.columns:
            df['signal_roc'] = np.where(df['roc'] > 0, 1,
                                 np.where(df['roc'] < 0, -1, 0))
            signal_cols.append('signal_roc')
        if 'rocp' in df.columns:
            df['signal_rocp'] = np.where(df['rocp'] > 0, 1,
                                  np.where(df['rocp'] < 0, -1, 0))
            signal_cols.append('signal_rocp')
        if 'rocr' in df.columns:
            df['signal_rocr'] = np.where(df['rocr'] > 1, 1,
                                  np.where(df['rocr'] < 1, -1, 0))
            signal_cols.append('signal_rocr')
        if 'rocr100' in df.columns:
            df['signal_rocr100'] = np.where(df['rocr100'] > 100, 1,
                                     np.where(df['rocr100'] < 100, -1, 0))
            signal_cols.append('signal_rocr100')
        if 'rsi' in df.columns:
            df['signal_rsi'] = np.where(df['rsi'] > 70, -1,
                                 np.where(df['rsi'] < 30, 1, 0))
            signal_cols.append('signal_rsi')
        if has_cols('stoch_k', 'stoch_d'):
            df['signal_stoch'] = np.where((df['stoch_k'] > df['stoch_d']) & (df['stoch_k'] < 80), 1,
                                   np.where((df['stoch_k'] < df['stoch_d']) & (df['stoch_k'] > 20), -1, 0))
            signal_cols.append('signal_stoch')
        if has_cols('stochf_k', 'stochf_d'):
            df['signal_stochf'] = np.where((df['stochf_k'] > df['stochf_d']) & (df['stochf_k'] < 80), 1,
                                    np.where((df['stochf_k'] < df['stochf_d']) & (df['stochf_k'] > 20), -1, 0))
            signal_cols.append('signal_stochf')
        if 'stochrsi' in df.columns:
            df['signal_stochrsi'] = np.where(df['stochrsi'] > 0.8, -1,
                                      np.where(df['stochrsi'] < 0.2, 1, 0))
            signal_cols.append('signal_stochrsi')
        if 'trix' in df.columns:
            df['trix_prev'] = df['trix'].shift(1)
            df['signal_trix'] = np.where(df['trix'] > df['trix_prev'], 1,
                                  np.where(df['trix'] < df['trix_prev'], -1, 0))
            signal_cols.append('signal_trix')
        if 'ultosc' in df.columns:
            df['signal_ultosc'] = np.where(df['ultosc'] > 70, -1,
                                    np.where(df['ultosc'] < 30, 1, 0))
            signal_cols.append('signal_ultosc')
        if 'willr' in df.columns:
            df['signal_willr'] = np.where(df['williams_r'] < -80, 1,
                                   np.where(df['williams_r'] > -20, -1, 0))
            signal_cols.append('signal_willr')

        # Volume Indicators
        if 'ad' in df.columns:
            df['ad_prev'] = df['ad'].shift(1)
            df['signal_ad'] = np.where(df['ad'] > df['ad_prev'], 1,
                                np.where(df['ad'] < df['ad_prev'], -1, 0))
            signal_cols.append('signal_ad')
        if 'adosc' in df.columns:
            df['adosc_prev'] = df['adosc'].shift(1)
            df['signal_adosc'] = np.where(df['adosc'] > df['adosc_prev'], 1,
                                   np.where(df['adosc'] < df['adosc_prev'], -1, 0))
            signal_cols.append('signal_adosc')
        if 'obv' in df.columns:
            df['obv_prev'] = df['obv'].shift(1)
            df['signal_obv'] = np.where(df['obv'] > df['obv_prev'], 1,
                                 np.where(df['obv'] < df['obv_prev'], -1, 0))
            signal_cols.append('signal_obv')

        # Volatility Indicators
        if 'atr' in df.columns:
            df['atr_prev'] = df['atr'].shift(1)
            df['signal_atr'] = np.where(df['atr'] > df['atr_prev'], 1,
                                 np.where(df['atr'] < df['atr_prev'], -1, 0))
            signal_cols.append('signal_atr')
        if 'natr' in df.columns:
            df['natr_prev'] = df['natr'].shift(1)
            df['signal_natr'] = np.where(df['natr'] > df['natr_prev'], 1,
                                  np.where(df['natr'] < df['natr_prev'], -1, 0))
            signal_cols.append('signal_natr')
        if 'trange' in df.columns:
            df['trange_prev'] = df['true_range'].shift(1)
            df['signal_trange'] = np.where(df['true_range'] > df['trange_prev'], 1,
                                    np.where(df['true_range'] < df['trange_prev'], -1, 0))
            signal_cols.append('signal_trange')

        # Price Transform
        if 'avgprice' in df.columns:
            df['signal_avgprice'] = np.where(df['close'] > df['avgprice'], 1,
                                      np.where(df['close'] < df['avgprice'], -1, 0))
            signal_cols.append('signal_avgprice')
        if 'medprice' in df.columns:
            df['signal_medprice'] = np.where(df['close'] > df['medprice'], 1,
                                      np.where(df['close'] < df['medprice'], -1, 0))
            signal_cols.append('signal_medprice')
        if 'typprice' in df.columns:
            df['signal_typprice'] = np.where(df['close'] > df['typprice'], 1,
                                      np.where(df['close'] < df['typprice'], -1, 0))
            signal_cols.append('signal_typprice')
        if 'wclprice' in df.columns:
            df['signal_wclprice'] = np.where(df['close'] > df['wclprice'], 1,
                                      np.where(df['close'] < df['wclprice'], -1, 0))
            signal_cols.append('signal_wclprice')

        # Cycle Indicators
        if 'ht_dcperiod' in df.columns:
            df['ht_dcperiod_prev'] = df['ht_dcperiod'].shift(1)
            df['signal_ht_dcperiod'] = np.where(df['ht_dcperiod'] > df['ht_dcperiod_prev'], 1,
                                         np.where(df['ht_dcperiod'] < df['ht_dcperiod_prev'], -1, 0))
            signal_cols.append('signal_ht_dcperiod')
        if 'ht_dcphase' in df.columns:
            df['ht_dcphase_prev'] = df['ht_dcphase'].shift(1)
            df['signal_ht_dcphase'] = np.where(df['ht_dcphase'] > df['ht_dcphase_prev'], 1,
                                        np.where(df['ht_dcphase'] < df['ht_dcphase_prev'], -1, 0))
            signal_cols.append('signal_ht_dcphase')
        if has_cols('ht_phasor_inphase', 'ht_phasor_quadrature'):
            df['signal_ht_phasor'] = np.where(df['ht_phasor_inphase'] > df['ht_phasor_quadrature'], 1,
                                       np.where(df['ht_phasor_inphase'] < df['ht_phasor_quadrature'], -1, 0))
            signal_cols.append('signal_ht_phasor')
        if has_cols('ht_sine', 'ht_leadsine'):
            df['signal_ht_sine'] = np.where(df['ht_sine'] > df['ht_leadsine'], 1,
                                     np.where(df['ht_sine'] < df['ht_leadsine'], -1, 0))
            signal_cols.append('signal_ht_sine')
        if 'ht_trendmode' in df.columns:
            df['signal_ht_trendmode'] = np.where(df['ht_trendmode'] == 1, 1, 0)
            signal_cols.append('signal_ht_trendmode')

        # Pattern Recognition

        if 'cdl2crows' in df.columns:
            df['signal_cdl2crows'] = np.where(df['cdl2crows'] != 0, -1, 0)
            signal_cols.append('signal_cdl2crows')
        if 'cdl3blackcrows' in df.columns:
            df['signal_cdl3blackcrows'] = np.where(df['cdl3blackcrows'] != 0, -1, 0)
            signal_cols.append('signal_cdl3blackcrows')
        if 'cdl3inside' in df.columns:
            df['signal_cdl3inside'] = np.where(df['cdl3inside'] != 0, 1, 0)
            signal_cols.append('signal_cdl3inside')
        if 'cdl3linestrike' in df.columns:
            df['signal_cdl3linestrike'] = np.where(df['cdl3linestrike'] != 0, 1, 0)
            signal_cols.append('signal_cdl3linestrike')
        if 'cdl3outside' in df.columns:
            df['signal_cdl3outside'] = np.where(df['cdl3outside'] != 0, 1, 0)
            signal_cols.append('signal_cdl3outside')
        if 'cdl3starsinsouth' in df.columns:
            df['signal_cdl3starsinsouth'] = np.where(df['cdl3starsinsouth'] != 0, 1, 0)
            signal_cols.append('signal_cdl3starsinsouth')
        if 'cdl3whitesoldiers' in df.columns:
            df['signal_cdl3whitesoldiers'] = np.where(df['cdl3whitesoldiers'] != 0, 1, 0)
            signal_cols.append('signal_cdl3whitesoldiers')
        if 'cdlabandonedbaby' in df.columns:
            df['signal_cdlabandonedbaby'] = np.where(df['cdlabandonedbaby'] != 0, -1, 0)
            signal_cols.append('signal_cdlabandonedbaby')
        if 'cdladvanceblock' in df.columns:
            df['signal_cdladvanceblock'] = np.where(df['cdladvanceblock'] != 0, -1, 0)
            signal_cols.append('signal_cdladvanceblock')
        if 'cdlbelthold' in df.columns:
            df['signal_cdlbelthold'] = np.where(df['cdlbelthold'] != 0, 1, 0)
            signal_cols.append('signal_cdlbelthold')
        if 'cdlbreakaway' in df.columns:
            df['signal_cdlbreakaway'] = np.where(df['cdlbreakaway'] != 0, 1, 0)
            signal_cols.append('signal_cdlbreakaway')
        if 'cdlclosingmarubozu' in df.columns:
            df['signal_cdlclosingmarubozu'] = np.where(df['cdlclosingmarubozu'] != 0, 1, 0)
            signal_cols.append('signal_cdlclosingmarubozu')
        if 'cdlconcealbabyswall' in df.columns:
            df['signal_cdlconcealbabyswall'] = np.where(df['cdlconcealbabyswall'] != 0, 1, 0)
            signal_cols.append('signal_cdlconcealbabyswall')
        if 'cdlcounterattack' in df.columns:
            df['signal_cdlcounterattack'] = np.where(df['cdlcounterattack'] != 0, 1, 0)
            signal_cols.append('signal_cdlcounterattack')
        if 'cdldarkcloudcover' in df.columns:
            df['signal_cdldarkcloudcover'] = np.where(df['cdldarkcloudcover'] != 0, -1, 0)
            signal_cols.append('signal_cdldarkcloudcover')
        if 'cdldoji' in df.columns:
            df['signal_cdldoji'] = np.where(df['cdldoji'] != 0, 0, 0)  # Neutral signal for Doji
            signal_cols.append('signal_cdldoji')
        if 'cdldojistar' in df.columns:
            df['signal_cdldojistar'] = np.where(df['cdldojistar'] != 0, 0, 0)
            signal_cols.append('signal_cdldojistar')
        if 'cdldragonflydoji' in df.columns:
            df['signal_cdldragonflydoji'] = np.where(df['cdldragonflydoji'] != 0, 1, 0)
            signal_cols.append('signal_cdldragonflydoji')
        if 'cdlengulfing' in df.columns:
            df['signal_cdlengulfing'] = np.where(df['cdlengulfing'] > 0, 1,
                                         np.where(df['cdlengulfing'] < 0, -1, 0))
            signal_cols.append('signal_cdlengulfing')
        if 'cdleveningdojistar' in df.columns:
            df['signal_cdleveningdojistar'] = np.where(df['cdleveningdojistar'] != 0, -1, 0)
            signal_cols.append('signal_cdleveningdojistar')
        if 'cdleveningstar' in df.columns:
            df['signal_cdleveningstar'] = np.where(df['cdleveningstar'] != 0, -1, 0)
            signal_cols.append('signal_cdleveningstar')
        if 'cdlgapsidesidewhite' in df.columns:
            df['signal_cdlgapsidesidewhite'] = np.where(df['cdlgapsidesidewhite'] != 0, 1, 0)
            signal_cols.append('signal_cdlgapsidesidewhite')
        if 'cdlgravestonedoji' in df.columns:
            df['signal_cdlgravestonedoji'] = np.where(df['cdlgravestonedoji'] != 0, -1, 0)
            signal_cols.append('signal_cdlgravestonedoji')
        if 'cdlhammer' in df.columns:
            df['signal_cdlhammer'] = np.where(df['cdlhammer'] != 0, 1, 0)
            signal_cols.append('signal_cdlhammer')
        if 'cdlhangingman' in df.columns:
            df['signal_cdlhangingman'] = np.where(df['cdlhangingman'] != 0, -1, 0)
            signal_cols.append('signal_cdlhangingman')
        if 'cdlharami' in df.columns:
            df['signal_cdlharami'] = np.where(df['cdlharami'] != 0, 1, 0)
            signal_cols.append('signal_cdlharami')
        if 'cdlharamicross' in df.columns:
            df['signal_cdlharamicross'] = np.where(df['cdlharamicross'] != 0, 1, 0)
            signal_cols.append('signal_cdlharamicross')
        if 'cdlhighwave' in df.columns:
            df['signal_cdlhighwave'] = np.where(df['cdlhighwave'] != 0, 0, 0)
            signal_cols.append('signal_cdlhighwave')
        if 'cdlhikkake' in df.columns:
            df['signal_cdlhikkake'] = np.where(df['cdlhikkake'] != 0, 1, 0)
            signal_cols.append('signal_cdlhikkake')
        if 'cdlhikkakemod' in df.columns:
            df['signal_cdlhikkakemod'] = np.where(df['cdlhikkakemod'] != 0, 1, 0)
            signal_cols.append('signal_cdlhikkakemod')
        if 'cdlidentical3crows' in df.columns:
            df['signal_cdlidentical3crows'] = np.where(df['cdlidentical3crows'] != 0, -1, 0)
            signal_cols.append('signal_cdlidentical3crows')
        if 'cdlinneck' in df.columns:
            df['signal_cdlinneck'] = np.where(df['cdlinneck'] != 0, -1, 0)
            signal_cols.append('signal_cdlinneck')
        if 'cdlinvertedhammer' in df.columns:
            df['signal_cdlinvertedhammer'] = np.where(df['cdlinvertedhammer'] != 0, 1, 0)
            signal_cols.append('signal_cdlinvertedhammer')
        if 'cdlkicking' in df.columns:
            df['signal_cdlkicking'] = np.where(df['cdlkicking'] != 0, 1, 0)
            signal_cols.append('signal_cdlkicking')
        if 'cdlkickingbylength' in df.columns:
            df['signal_cdlkickingbylength'] = np.where(df['cdlkickingbylength'] != 0, 1, 0)
            signal_cols.append('signal_cdlkickingbylength')
        if 'cdlladderbottom' in df.columns:
            df['signal_cdlladderbottom'] = np.where(df['cdlladderbottom'] != 0, 1, 0)
            signal_cols.append('signal_cdlladderbottom')
        if 'cdllongleggeddoji' in df.columns:
            df['signal_cdllongleggeddoji'] = np.where(df['cdllongleggeddoji'] != 0, 0, 0)
            signal_cols.append('signal_cdllongleggeddoji')
        if 'cdllongline' in df.columns:
            df['signal_cdllongline'] = np.where(df['cdllongline'] != 0, 1, 0)
            signal_cols.append('signal_cdllongline')
        if 'cdlmarubozu' in df.columns:
            df['signal_cdlmarubozu'] = np.where(df['cdlmarubozu'] != 0, 1, 0)
            signal_cols.append('signal_cdlmarubozu')
        if 'cdlmatchinglow' in df.columns:
            df['signal_cdlmatchinglow'] = np.where(df['cdlmatchinglow'] != 0, 1, 0)
            signal_cols.append('signal_cdlmatchinglow')
        if 'cdlonneck' in df.columns:
            df['signal_cdlonneck'] = np.where(df['cdlonneck'] != 0, -1, 0)
            signal_cols.append('signal_cdlonneck')
        if 'cdlpiercing' in df.columns:
            df['signal_cdlpiercing'] = np.where(df['cdlpiercing'] != 0, 1, 0)
            signal_cols.append('signal_cdlpiercing')
        if 'cdlrickshawman' in df.columns:
            df['signal_cdlrickshawman'] = np.where(df['cdlrickshawman'] != 0, 0, 0)
            signal_cols.append('signal_cdlrickshawman')
        if 'cdlrisefall3methods' in df.columns:
            df['signal_cdlrisefall3methods'] = np.where(df['cdlrisefall3methods'] != 0, 1, 0)
            signal_cols.append('signal_cdlrisefall3methods')
        if 'cdlseparatinglines' in df.columns:
            df['signal_cdlseparatinglines'] = np.where(df['cdlseparatinglines'] != 0, 1, 0)
            signal_cols.append('signal_cdlseparatinglines')
        if 'cdlshootingstar' in df.columns:
            df['signal_cdlshootingstar'] = np.where(df['cdlshootingstar'] != 0, -1, 0)
            signal_cols.append('signal_cdlshootingstar')
        if 'cdlshortline' in df.columns:
            df['signal_cdlshortline'] = np.where(df['cdlshortline'] != 0, 1, 0)
            signal_cols.append('signal_cdlshortline')
        if 'cdlspinningtop' in df.columns:
            df['signal_cdlspinningtop'] = np.where(df['cdlspinningtop'] != 0, 0, 0)
            signal_cols.append('signal_cdlspinningtop')
        if 'cdlstalledpattern' in df.columns:
            df['signal_cdlstalledpattern'] = np.where(df['cdlstalledpattern'] != 0, -1, 0)
            signal_cols.append('signal_cdlstalledpattern')
        if 'cdlsticksandwich' in df.columns:
            df['signal_cdlsticksandwich'] = np.where(df['cdlsticksandwich'] != 0, 1, 0)
            signal_cols.append('signal_cdlsticksandwich')
        if 'cdltakuri' in df.columns:
            df['signal_cdltakuri'] = np.where(df['cdltakuri'] != 0, 1, 0)
            signal_cols.append('signal_cdltakuri')
        if 'cdltasukigap' in df.columns:
            df['signal_cdltasukigap'] = np.where(df['cdltasukigap'] != 0, 1, 0)
            signal_cols.append('signal_cdltasukigap')
        if 'cdlthrusting' in df.columns:
            df['signal_cdlthrusting'] = np.where(df['cdlthrusting'] != 0, -1, 0)
            signal_cols.append('signal_cdlthrusting')
        if 'cdltristar' in df.columns:
            df['signal_cdltristar'] = np.where(df['cdltristar'] != 0, 0, 0)
            signal_cols.append('signal_cdltristar')
        if 'cdlunique3river' in df.columns:
            df['signal_cdlunique3river'] = np.where(df['cdlunique3river'] != 0, 1, 0)
            signal_cols.append('signal_cdlunique3river')
        if 'cdlupsidegap2crows' in df.columns:
            df['signal_cdlupsidegap2crows'] = np.where(df['cdlupsidegap2crows'] != 0, -1, 0)
            signal_cols.append('signal_cdlupsidegap2crows')
        if 'cdlxsidegap3methods' in df.columns:
            df['signal_cdlxsidegap3methods'] = np.where(df['cdlxsidegap3methods'] != 0, 1, 0)
            signal_cols.append('signal_cdlxsidegap3methods')

        # Final output
        base_cols = ["datetime", 'open', 'high', 'low', 'close', 'volume']
        if 'datetime' not in df.columns and df.index.name == 'datetime':
            df = df.reset_index()

        output = df[base_cols + signal_cols].copy()
        return output
