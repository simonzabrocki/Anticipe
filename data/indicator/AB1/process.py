AB1_SDG_computation_config = {
    'Variable': 'AB1',
    'From': ['SDG API'],
    'files': ['AB1.0_SDG.csv', 'AB1.1_SDG.csv'],
    'function': lambda df, var: (df[var[0]] + df[var[1]]) / 2,
    'sub_variables': ['Proportion of population using safely managed sanitation services, by urban/rural (%) Location ALLAREA Reporting Type G',
                      'Proportion of population using safely managed drinking water services, by urban/rural (%) Location ALLAREA Reporting Type G'
                      ],
    'Description': lambda var: f"[ ({var[0]}) + ({var[1]}) ] / 2"
}

AB1_WB_computation_config = {
    'Variable': 'AB1',
    'From': ['WB API'],
    'files': ['AB1.0_WB.csv', 'AB1.1_WB.csv'],
    'function': lambda df, var: (df[var[0]] + df[var[1]]) / 2,
    'sub_variables': ['People using safely managed drinking water services (% of population)',
                      'People using safely managed sanitation services (% of population)'
                      ],
    'Description': lambda var: f"[ ({var[0]}) + ({var[1]}) ] / 2"
}
