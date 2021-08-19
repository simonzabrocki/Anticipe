
import os
from processing.indicator_computation import compute_from_path, indicators_computations

# from data.indicator.GE3.process import GE3_computation_config
# from data.indicator.GE2.process import GE2_computation_config
# from data.indicator.GE1.process import GE1_computation_config
# from data.indicator.GB2.process import GB2_WB_computation_config, GB2_SDG_computation_config
# from data.indicator.BE1.process import BE1_computation_config
# from data.indicator.SE2.process import SE2_WB_computation_config, SE2_SDG_computation_config
# from data.indicator.SE1.process import SE1_computation_config
# #from data.indicator.AB3.process import AB3_computation_config
# #from data.indicator.AB2.process import AB2_SDG_computation_config, AB2_WB_computation_config
# from data.indicator.AB1.process import AB1_SDG_computation_config, AB1_WB_computation_config


# indicators_computations = {
#     'GE3': [('GE3.csv', GE3_computation_config)],
#     'GE2': [('GE2.csv', GE2_computation_config)],
#     'GE1': [('GE1.csv', GE1_computation_config)],
#     'GB2': [('GB2_WB.csv', GB2_WB_computation_config), ('GB2_SDG.csv', GB2_SDG_computation_config)],
#     'BE1': [('BE1.csv', BE1_computation_config)],
#     'SE2': [('SE2_WB.csv', SE2_WB_computation_config), ('SE2_SDG.csv', SE2_SDG_computation_config)],
#     'SE1': [('SE1.csv', SE1_computation_config)],
#     #'AB3': [('AB3.csv', AB3_computation_config)],
#     #'AB2': [('AB2_SDG.csv', AB2_SDG_computation_config), ('AB2_WB.csv', AB2_WB_computation_config)],
#     'AB1': [('AB1_SDG.csv', AB1_SDG_computation_config), ('AB1_WB.csv', AB1_WB_computation_config)],
# }


def compute_indicator(indicator):
    computations_list = indicators_computations.get(indicator)
    for file, computation in computations_list:
                print(f'Computing {indicator} for {file}: ', end='')
                try:
                    df = compute_from_path(computation, f'data/indicator/{indicator}/preprocessed')
                    os.makedirs(f'data/indicator/{indicator}/computed', exist_ok=True)
                    df.to_csv(f'data/indicator/{indicator}/computed/{file}', index=False)
                    print('DONE')
                except Exception as e:
                    print(e)

def compute_indicators():
    for indicator in indicators_computations.keys():
        compute_indicator(indicator)