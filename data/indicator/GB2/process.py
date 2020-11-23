import pandas as pd
import numpy as np


GB2_WB_computation_config = {
    'Variable': 'GB2',
    'From': ['WB API'],
    'files': ['GB2.0_WB.csv', 'GB2.1_WB.csv'],
    'function': lambda df, var: max_ratio(df[var[0]], df[var[1]]),
    'sub_variables': ['Account ownership at a financial institution or with a mobile-money-service provider, male (% of population ages 15+)',
                      'Account ownership at a financial institution or with a mobile-money-service provider, female (% of population ages 15+)'],
    'Description': lambda var: f"max Ratio ({var[0]}, {var[1]})"
}

GB2_SDG_computation_config = {
    'Variable': 'GB2',
    'files': ['GB2.0_SDG.csv', 'GB2.1_SDG.csv'],
    'From': ['SDG API'],
    'function': lambda df, var: max_ratio(df[var[0]], df[var[1]]),
    'sub_variables': ['Proportion of adults (15 years and older) with an account at a financial institution or mobile-money-service provider, by sex (% of adults aged 15 years and older) Age 15+ Sex FEMALE Reporting Type G',
                      'Proportion of adults (15 years and older) with an account at a financial institution or mobile-money-service provider, by sex (% of adults aged 15 years and older) Age 15+ Sex MALE Reporting Type G'],
    'Description': lambda var: f"max Ratio ({var[0]}, {var[1]})"
}


def max_ratio(num, den):
    return pd.concat([num / den, den / num], axis=1).max(axis=1).replace([np.inf, -np.inf], np.nan)
