AB3_computation_config = {
    'Variable': 'AB3',
    'From': ['WB API'],
    'files': ['AB3.0_WB.csv', 'AB3.1_WB.csv'],
    'function': lambda df, var: (df[var[0]] + df[var[1]]) / 2,
    'sub_variables': ['Fixed broadband subscriptions (per 100 people)',
                      'Mobile cellular subscriptions (per 100 people)'
                      ],
    'Description': lambda var: f"[({var[0]}) + ({var[1]})] / 2"
}
