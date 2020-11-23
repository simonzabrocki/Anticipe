GE3_computation_config = {
    'Variable': 'GE3',
    'files': ['GE3.1_CW.csv', 'GE3.0_WB.csv'],
    'From': ['CW API', 'WB API'],
    'function': lambda df, var: df[var[0]] / df[var[1]],
    'sub_variables': ['N2O CH4 Agriculture and Land-Use Change and Forestry Tons',
                      'Population, total'],
    'Description': lambda var: f"{var[0]} / {var[1]}"
}
