SE1_computation_config = {
    'Variable': 'SE1',
    'files': ['SE1.0_WB.csv', 'SE1.1_WB.csv', 'SE1.2_WB.csv'],
    'From': ['WB API'],
    'function': lambda df, var: df[var[0]] / (df[var[1]] + df[var[2]]),
    'sub_variables': ['Income share held by highest 10%',
                      'Income share held by fourth 20%',
                      'Income share held by lowest 20%',
                      ],
    'Description': lambda var: f"({var[0]}) / [({var[1]}) + ({var[2]})]"
}
