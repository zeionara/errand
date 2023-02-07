import scipy.stats
from pandas import DataFrame

import numpy as np
import ctypes


def encode_list(items: tuple):
    return np.array(items).ctypes.data_as(ctypes.POINTER(ctypes.c_long))
    # return np.array(items).__array_interface__['data'][0]


def compare_execution_time(df: DataFrame, lhs_label: str, rhs_label: str):
    lhs_vs_rhs_quotients = df[(lhs_label, 'mean')].divide(df[(rhs_label, 'mean')])

    return lhs_vs_rhs_quotients.mean(), lhs_vs_rhs_quotients.std()


def compare_distributions(df: DataFrame, lhs_label: str, rhs_label: str, alpha: float = 0.05):
    assert 0 < alpha < 1, 'Alpha parameter accepts value in the interval (0; 1)'

    numerator = df[(lhs_label, 'mean')].sub(df[(rhs_label, 'mean')])
    denominator = df[(lhs_label, 'std')].pow(2).divide(df[(lhs_label, 'sample size')]).add(
        df[(rhs_label, 'std')].pow(2).divide(df[(rhs_label, 'sample size')])
    ).pow(0.5)

    df = df.copy()

    df['t-score'] = numerator.divide(denominator)

    df['p-value'] = p_value = df.apply(
        lambda x: scipy.stats.t.sf(
            abs(
                x.at['t-score'].iloc[0]
            ), df = int(
                x.loc[[[lhs_label, 'sample size']]].iloc[0]
            ) - 1
        ) * 2, axis = 1
    )

    df['is significant'] = p_value.le(alpha)

    return df


def drop_outliers(x, y, z, max_median_multiplier: float = 20):
    y_median = np.median(y)

    for x_element, y_element, z_element in zip(x, y, z):
        if np.abs(y_element - y_median) / y_median < max_median_multiplier:
            yield x_element, y_element, z_element
