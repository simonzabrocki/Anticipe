GE1_computation_config = {
    'Variable': 'GE1',
    'files': ['GE1.0_CW.csv', 'GE1.1_WB.csv'],
    'From': ['CW API', 'WB API'],
    'function': lambda df, var: df[var[0]] / df[var[1]],
    'sub_variables': ['CO2 Total including LUCF Tons',
                      'Population, total'],
    'Description': lambda var: f"{var[0]} / {var[1]}"
}
