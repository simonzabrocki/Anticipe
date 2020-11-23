BE1_computation_config = {
    'Variable': 'BE1',
    'From': ['SDG API'],
    'files': ['BE1.0_SDG.csv', 'BE1.1_SDG.csv', 'BE1.2_SDG.csv', 'BE1.3_SDG.csv'],
    'function': lambda df, var: df[var].mean(axis=1),
    'sub_variables': ['Average proportion of Mountain Key Biodiversity Areas (KBAs) covered by protected areas (%) Reporting Type G',
                      'Average proportion of Marine Key Biodiversity Areas (KBAs) covered by protected areas (%) Reporting Type G',
                      'Average proportion of Freshwater Key Biodiversity Areas (KBAs) covered by protected areas (%) Reporting Type G',
                      'Average proportion of Terrestrial Key Biodiversity Areas (KBAs) covered by protected areas (%) Reporting Type G',

                      ],
    'Description': lambda var: f"[({var[0]}) + ({var[1]}) + ({var[2]}) + ({var[3]}) ] / 4"
}
