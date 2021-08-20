import pandas as pd


# To add later
new_IND_CAT_DIM = pd.DataFrame([['AB1', 'AB', 'SI'],
                                ['AB2', 'AB', 'SI'],
                                ['AB3', 'AB', 'SI'],
                                ['BE1', 'BE', 'NCP'],
                                ['BE2', 'BE', 'NCP'],
                                ['BE3', 'BE', 'NCP'],
                                ['CV1', 'CV', 'NCP'],
                                ['CV2', 'CV', 'NCP'],
                                ['CV3', 'CV', 'NCP'],
                                ['EE1', 'EE', 'ESRU'],
                                ['EE2', 'EE', 'ESRU'],
                                ['EE3', 'EE', 'ESRU'],
                                ['EQ1', 'EQ', 'NCP'],
                                ['EQ2', 'EQ', 'NCP'],
                                ['EQ3', 'EQ', 'NCP'],
                                ['EW1', 'EW', 'ESRU'],
                                ['EW2', 'EW', 'ESRU'],
                                ['EW3', 'EW', 'ESRU'],
                                ['GB1', 'GB', 'SI'],
                                ['GB2', 'GB', 'SI'],
                                ['GB3', 'GB', 'SI'],
                                ['GE1', 'GE', 'NCP'],
                                ['GE2', 'GE', 'NCP'],
                                ['GE3', 'GE', 'NCP'],
                                ['GJ1', 'GJ', 'GEO'],
                                ['GJ2', 'GJ', 'GEO'],
                                ['GN1', 'GN', 'GEO'],
                                ['GN2', 'GN', 'GEO'],
                                ['GT1', 'GT', 'GEO'],
                                ['GT2', 'GT', 'GEO'],
                                ['GV1', 'GV', 'GEO'],
                                ['GV2', 'GV', 'GEO'],
                                ['ME1', 'ME', 'ESRU'],
                                ['ME2', 'ME', 'ESRU'],
                                ['ME3', 'ME', 'ESRU'],
                                ['SE1', 'SE', 'SI'],
                                ['SE2', 'SE', 'SI'],
                                ['SE3', 'SE', 'SI'],
                                ['SL1', 'SL', 'ESRU'],
                                ['SL2', 'SL', 'ESRU'],
                                ['SL3', 'SL', 'ESRU'],
                                ['SP1', 'SP', 'SI'],
                                ['SP2', 'SP', 'SI'],
                                ['SP3', 'SP', 'SI']],
                                columns=['Indicator', 'Category', 'Dimension'])

class GreenGrowthStuff():
    '''
    A class to wrap all the useful attributes and functions of the GreenGrowthIndex

    Attributes
    ----------
    '''

    def __init__(self):
        IND_CAT_DIM = new_IND_CAT_DIM
        # IND_CAT_DIM = pd.DataFrame([['AB1', 'AB', 'SI'],
        #                             ['AB2', 'AB', 'SI'],
        #                             ['AB3', 'AB', 'SI'],
        #                             ['BE1', 'BE', 'NCP'],
        #                             ['BE2', 'BE', 'NCP'],
        #                             ['BE3', 'BE', 'NCP'],
        #                             ['CV1', 'CV', 'NCP'],
        #                             ['CV2', 'CV', 'NCP'],
        #                             ['CV3', 'CV', 'NCP'],
        #                             ['EE1', 'EE', 'ESRU'],
        #                             ['EE2', 'EE', 'ESRU'],
        #                             ['EQ1', 'EQ', 'NCP'],
        #                             ['EQ2', 'EQ', 'NCP'],
        #                             ['EQ3', 'EQ', 'NCP'],
        #                             ['EW1', 'EW', 'ESRU'],
        #                             ['EW2', 'EW', 'ESRU'],
        #                             ['GB1', 'GB', 'SI'],
        #                             ['GB2', 'GB', 'SI'],
        #                             ['GB3', 'GB', 'SI'],
        #                             ['GE1', 'GE', 'NCP'],
        #                             ['GE2', 'GE', 'NCP'],
        #                             ['GE3', 'GE', 'NCP'],
        #                             ['GJ1', 'GJ', 'GEO'],
        #                             ['GN1', 'GN', 'GEO'],
        #                             ['GT1', 'GT', 'GEO'],
        #                             ['GV1', 'GV', 'GEO'],
        #                             ['ME1', 'ME', 'ESRU'],
        #                             ['ME2', 'ME', 'ESRU'],
        #                             ['SE1', 'SE', 'SI'],
        #                             ['SE2', 'SE', 'SI'],
        #                             ['SE3', 'SE', 'SI'],
        #                             ['SL2', 'SL', 'ESRU'],
        #                             ['SL1', 'SL', 'ESRU'],
        #                             ['SP1', 'SP', 'SI'],
        #                             ['SP2', 'SP', 'SI'],
        #                             ['SP3', 'SP', 'SI']],
        #                            columns=['Indicator', 'Category', 'Dimension'])

        self.IND_CAT_DIM = IND_CAT_DIM
        self.dimension_names = IND_CAT_DIM.Dimension.unique()
        self.category_names = IND_CAT_DIM.Category.unique()
        self.indicator_names = IND_CAT_DIM.Indicator.unique()

    def get_dimensions_from_categories(self, categories):
        dims = self.IND_CAT_DIM[['Dimension', 'Category']].drop_duplicates().set_index('Category')['Dimension']
        return dims.loc[categories].values

    def get_dimensions(self):
        return self.IND_CAT_DIM['Dimension'].unique()
