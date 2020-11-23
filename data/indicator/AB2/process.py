AB2_SDG_computation_config = {
    'Variable': 'AB2',
    'files': ['AB2.0_SDG.csv', 'AB2.1_SDG.csv'],
    'From': ['SDG API'],
    'function': lambda df, var: (df[var[0]] + df[var[1]]) / 2,
    'sub_variables': ['Proportion of population with access to electricity, by urban/rural (%) Location ALLAREA Reporting Type G',
                      'Proportion of population with primary reliance on clean fuels and technology (%) Reporting Type G'
                      ],
    'Description': lambda var: f"[({var[0]}) + ({var[1]})] / 2"
}

AB2_WB_computation_config = {
    'Variable': 'AB2',
    'files': ['AB2.0_WB.csv', 'AB2.1_WB.csv'],
    'From': ['WB API'],
    'function': lambda df, var: (df[var[0]] + df[var[1]]) / 2,
    'sub_variables': ['Access to electricity (% of population)',
                      'Access to clean fuels and technologies for cooking (% of population)'
                      ],
    'Description': lambda var: f"[({var[0]}) + ({var[1]})] / 2"
}
