import numpy as np
import pandas as pd


# SE2_WB_computation_config = {
#     'Variable': 'SE2',
#     'files': ['SE2.0_WB.csv', 'SE2.1_WB.csv', 'SE2.2_WB.csv', 'SE2.3_WB.csv', 'SE2.4_WB.csv', 'SE2.5_WB.csv'],
#     'From': ['WB API'],
#     'function': lambda df, var: max_ratio(df[var[0:3]].sum(axis=1), df[var[3:]].sum(axis=1)),
#     'sub_variables': ['People using safely managed drinking water services, urban (% of urban population)',
#                       'Access to electricity, urban (% of urban population)',
#                       'People using safely managed sanitation services, urban (% of urban population)',
#                       'People using safely managed drinking water services, rural (% of rural population)',
#                       'Access to electricity, rural (% of rural population)',
#                       'People using safely managed sanitation services, rural (% of rural population)',
#                       ],
#     'Description': lambda var: f"max Ratio ({var[0]} + {var[1]} + {var[2]}) / ({var[3]} + {var[4]} + {var[5]})"
# }
#
# SE2_SDG_computation_config = {
#     'Variable': 'SE2',
#     'From': ['SDG API'],
#     'files': ['SE2.0_SDG.csv', 'SE2.1_SDG.csv', 'SE2.2_SDG.csv', 'SE2.3_SDG.csv', 'SE2.4_SDG.csv', 'SE2.5_SDG.csv'],
#     'function': lambda df, var: max_ratio(df[var[0:3]].sum(axis=1), df[var[3:]].sum(axis=1)),
#     'sub_variables': ['Proportion of population using safely managed drinking water services, by urban/rural (%) Location URBAN Reporting Type G',
#                       'Proportion of population with access to electricity, by urban/rural (%) Location URBAN Reporting Type G',
#                       'Proportion of population using safely managed sanitation services, by urban/rural (%) Location URBAN Reporting Type G',
#                       'Proportion of population using safely managed drinking water services, by urban/rural (%) Location RURAL Reporting Type G',
#                       'Proportion of population with access to electricity, by urban/rural (%) Location RURAL Reporting Type G',
#                       'Proportion of population using safely managed sanitation services, by urban/rural (%) Location RURAL Reporting Type G',
#                       ],
#     'Description': lambda var: f"max Ratio ({var[0]} + {var[1]} + {var[2]}) / ({var[3]} + {var[4]} + {var[5]})"
# }
SE2_WB_computation_config = {
    'Variable': 'SE2',
    'files': ['SE2.0_WB.csv', 'SE2.1_WB.csv', 'SE2.2_WB.csv', 'SE2.3_WB.csv', 'SE2.4_WB.csv', 'SE2.5_WB.csv'],
    'From': ['WB API'],
    'function': lambda df, var: max_ratio(df[var[0]], df[var[1]]),
    'sub_variables': [
        'Access to electricity, urban (% of urban population)',
        'Access to electricity, rural (% of rural population)',
    ],
    'Description': lambda var: f"max Ratio ({var[0]} / {var[1]})"
}

SE2_SDG_computation_config = {
    'Variable': 'SE2',
    'From': ['SDG API'],
    'files': ['SE2.0_SDG.csv', 'SE2.1_SDG.csv', 'SE2.2_SDG.csv', 'SE2.3_SDG.csv', 'SE2.4_SDG.csv', 'SE2.5_SDG.csv'],
    'function': lambda df, var: max_ratio(df[var[0]], df[var[1]]),
    'sub_variables': [
        'Proportion of population with access to electricity, by urban/rural (%) Location URBAN Reporting Type G',
        'Proportion of population with access to electricity, by urban/rural (%) Location RURAL Reporting Type G',
    ],
    'Description': lambda var: f"max Ratio ({var[0]} / {var[1]})"
}


def max_ratio(num, den):
    return pd.concat([num / den, den / num], axis=1).max(axis=1).replace([np.inf, -np.inf], np.nan)
