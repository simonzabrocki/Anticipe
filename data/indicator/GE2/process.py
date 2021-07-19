GE2_computation_config = {
    'Variable': 'GE2',
    'files': ['GE2.0_CW.csv', 'GE2.1_WB.csv'],
    'From': ['CW API', 'WB API'],
    'function': lambda df, var: df[var[0]] / df[var[1]],
    'sub_variables': ['CH4 N2O F-Gas Total excluding LUCF and excluding Agriculture Tons',
                      'Population, total'],
    'Description': lambda var: f"{var[0]} / {var[1]}"
}
