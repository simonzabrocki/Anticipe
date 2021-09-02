AB1_SDG_computation_config = {
    'Variable': 'AB1',
    'From': ['SDG API'],
    'files': ['AB1.0_SDG.csv', 'AB1.1_SDG.csv', 'AB1.2_SDG.csv', 'AB1.3_SDG.csv'],
    #'function': lambda df, var: (df[var[0]] + df[var[1]]) / 2,
    'function': lambda df, var: df.mean(axis=1),
    'sub_variables': ['Proportion of population using safely managed sanitation services, by urban/rural (%) Location ALLAREA Reporting Type G',
                      'Proportion of population using safely managed drinking water services, by urban/rural (%) Location ALLAREA Reporting Type G',
                      'Proportion of population with access to electricity, by urban/rural (%) Location ALLAREA Reporting Type G',
                      'Proportion of population with primary reliance on clean fuels and technology (%) Reporting Type G'
                      ],
    'Description': lambda var: f"[ ({var[0]}) + ({var[1]}) + ({var[2]}) + ({var[3]})] / 4"
}