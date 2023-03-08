import pandas as pd
import numpy as np


def get_volume_list(raw_volume):
    raw_volume.append(100)
    raw_volume.append(0)
    raw_volume.sort()
    volume_1 = raw_volume[1] - raw_volume[0]
    volume_2 = raw_volume[2] - raw_volume[1]
    volume_3 = raw_volume[3] - raw_volume[2]
    volume_4 = raw_volume[4] - raw_volume[3]
    volume_5 = raw_volume[5] - raw_volume[4]
    return [volume_1, volume_2, volume_3, volume_4, volume_5]


def change(source, length=1):
    return source - source.shift(length)


def r_change(change, source, length=1):
    change_value = pd.Series(
        source.iloc[-1] - source.iloc[-1 - length],
        [source.index[-1]]
    )
    result = pd.concat([change, change_value])
    return result


def stdev(source, length, biased=True):
    result = source.rolling(length).std(ddof=0 if biased else 1)
    return result


def r_stdev(stdev, source, length, biased=True):
    stdev_value = pd.Series(
        source[-length:].std(ddof=0 if biased else 1),
        [source.index[-1]]
    )
    result = pd.concat([stdev, stdev_value])
    return result


def sma(source, length):
    result = source.rolling(length).mean()
    return result


def r_sma(sma, source, length):
    sma_value = pd.Series(
        sma.iloc[-1] - source.iloc[-1 - length] / length + \
            source.iloc[-1] / length,
        [source.index[-1]]
    )
    result = pd.concat([sma, sma_value])
    return result


def rma(source, length):
    data = source.copy()
    alpha = 1 / length
    na = data.isna().sum()
    sma = data[na:length + na].mean()
    data[length + na - 1] = sma
    rma = pd.DataFrame.ewm(
        data[length + na - 1:], alpha=alpha, adjust=False
    ).mean()
    result = [np.nan] * (length + na - 1)
    result.extend(rma)
    return pd.Series(result, source.index)


def r_rma(rma, source, length):
    alpha = 1 / length
    rma_value = pd.Series(
        alpha * source.iloc[-1] + (1 - alpha) * rma.iloc[-1],
        [source.index[-1]]
    )
    result = pd.concat([rma, rma_value])
    return result


def rsi(source, length):
    def max(*args):
        df = pd.DataFrame(args).transpose()
        na = df.isna().sum().max()
        result = [np.nan] * na
        result.extend(df.max(axis=1)[na:])
        return pd.Series(result, args[0].index)

    zero = pd.Series([0] * source.shape[0], source.index)
    u = max(source - source.shift(), zero)
    d = max(source.shift() - source, zero)
    rma_u = pd.Series(rma(u, length), source.index)
    rma_d = pd.Series(rma(d, length), source.index)
    rsi = pd.Series(
        100 - 100 / (1 + (rma_u / rma_d)), 
        source.index
    )
    return (u, d, rma_u, rma_d, rsi)


def r_rsi(u, d, rma_u, rma_d, rsi, source, length):
    u_value = pd.Series(
        max(source.iloc[-1] - source.iloc[-2], 0),
        [source.index[-1]]
    )
    d_value = pd.Series(
        max(source.iloc[-2] - source.iloc[-1], 0),
        [source.index[-1]]
    )
    u = pd.concat([u, u_value])
    d = pd.concat([d, d_value])
    rma_u = r_rma(rma_u, u, length)
    rma_d = r_rma(rma_d, d, length)
    rsi_value = pd.Series(
        100 - 100 / (1 + (rma_u.iloc[-1] / rma_d.iloc[-1])),
        [source.index[-1]]
    )
    rsi = pd.concat([rsi, rsi_value])
    return (u, d, rma_u, rma_d, rsi)


def tr(high, low, close, handle_na):
    hl = high - low
    hc = abs(high - close.shift())
    lc = abs(low - close.shift())
    if handle_na:
        hc[0] = abs(high[0] - close[0])
        lc[0] = abs(low[0] - close[0])
    df = pd.DataFrame([hl, hc, lc]).transpose()
    na = df.isna().sum().max()
    result = [None] * na
    result.extend(df.max(axis=1)[na:])
    return pd.Series(result, high.index)


def r_tr(tr, high, low, close):
    hl = high.iloc[-1] - low.iloc[-1]
    hc = abs(high.iloc[-1] - close.iloc[-2])
    lc = abs(low.iloc[-1] - close.iloc[-2])
    tr_value = pd.Series(
        max(hl, hc, lc),
        [high.index[-1]]
    )
    result = pd.concat([tr, tr_value])
    return result


def atr(high, low, close, length):
    true_range = tr(high, low, close, True)
    avg_true_range = rma(true_range, length)
    return (true_range, avg_true_range)


def r_atr(true_range, avg_true_range, high, low, close, length):
    true_range = r_tr(true_range, high, low, close)
    avg_true_range = r_rma(avg_true_range, true_range, length)
    return (true_range, avg_true_range)


def supertrend(high, low, close, factor, atr_length):
    hl2 = (high + low) / 2
    avg_true_range = atr(high, low, close, atr_length)
    lower_band = hl2 - factor * avg_true_range[1]
    upper_band = hl2 + factor * avg_true_range[1]

    super_trend = pd.Series([np.nan] * close.shape[0], close.index)
    direction = pd.Series([1] * close.shape[0], close.index)
    prev_super_trend = [np.nan] * close.shape[0]
    prev_lower_band = [0] * close.shape[0]
    prev_upper_band = [0] * close.shape[0]

    for i in range(1, close.shape[0]):
        if not pd.isna(lower_band[i - 1]):
            prev_lower_band[i] = lower_band[i - 1]
        if not pd.isna(upper_band[i - 1]):
            prev_upper_band[i] = upper_band[i - 1]
        if not (lower_band[i] > prev_lower_band[i]
                or close[i - 1] < prev_lower_band[i]):
            lower_band[i] = prev_lower_band[i]
        if not (upper_band[i] < prev_upper_band[i] 
                or close[i - 1] > prev_upper_band[i]):
            upper_band[i] = prev_upper_band[i]
        prev_super_trend[i] = super_trend[i - 1]
        if pd.isna(avg_true_range[1][i - 1]):
            direction[i] = 1
        elif prev_super_trend[i] == prev_upper_band[i]:
            direction[i] = -1 if close[i] > upper_band[i] else 1
        else:
            direction[i] = 1 if close[i] < lower_band[i] else -1
        super_trend[i] = \
            lower_band[i] if direction[i] == -1 else upper_band[i]

    return (
        avg_true_range[0], avg_true_range[1], 
        lower_band, upper_band,
        super_trend, direction
    )


def r_supertrend(
    true_range, avg_true_range, lower_band, upper_band, 
    super_trend, direction, high, low, close, factor, atr_length
 ):
    hl2 = (high.iloc[-1] + low.iloc[-1]) / 2
    avg_true_range = r_atr(
        true_range, avg_true_range, high, low, close, atr_length
    )
    lower_band_value = pd.Series(
        hl2 - factor * avg_true_range[1].iloc[-1],
        [close.index[-1]]
    )
    upper_band_value = pd.Series(
        hl2 + factor * avg_true_range[1].iloc[-1],
        [close.index[-1]]
    )
    lower_band = pd.concat([lower_band, lower_band_value])
    upper_band = pd.concat([upper_band, upper_band_value])
    super_trend_value = pd.Series(
        np.nan,
        [close.index[-1]]
    )
    direction_value = pd.Series(
        1,
        [close.index[-1]]
    )
    super_trend = pd.concat([super_trend, super_trend_value])
    direction = pd.concat([direction, direction_value])
    prev_super_trend = np.nan
    prev_lower_band = 0
    prev_upper_band = 0

    if not pd.isna(lower_band.iloc[-2]):
        prev_lower_band = lower_band.iloc[-2]
    if not pd.isna(upper_band.iloc[-2]):
        prev_upper_band = upper_band.iloc[-2]
    if not (lower_band.iloc[-1] > prev_lower_band
            or close.iloc[-2] < prev_lower_band):
        lower_band.iloc[-1] = prev_lower_band
    if not (upper_band.iloc[-1] < prev_upper_band
            or close.iloc[-2] > prev_upper_band):
        upper_band.iloc[-1] = prev_upper_band
    prev_super_trend = super_trend.iloc[-2]
    if pd.isna(avg_true_range[1].iloc[-2]):
        direction.iloc[-1] = 1
    elif prev_super_trend == prev_upper_band:
        direction.iloc[-1] = \
            -1 if close.iloc[-1] > upper_band.iloc[-1] else 1
    else:
        direction.iloc[-1] = \
            1 if close.iloc[-1] < lower_band.iloc[-1] else -1
    super_trend.iloc[-1] = \
        lower_band.iloc[-1] \
            if direction.iloc[-1] == -1 else upper_band.iloc[-1]

    return (
        avg_true_range[0], avg_true_range[1], 
        lower_band, upper_band,
        super_trend, direction
    )