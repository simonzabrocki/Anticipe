import numpy as np
from ggindex.IndexComputation.GreenGrowthIndex import GreenGrowthIndex
from ggindex.utils import ISO_to_Country
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ggindex.GreenGrowthStuff import GreenGrowthStuff


class IndexReport(GreenGrowthStuff):
    '''
    A class to create create reports on a GreenGrowthIndex

    (EXPERIMENTAL STILL NEED CLEANING UP)

    Attributes
    ----------
    data: pd.DataFrame
        A data frame with all in the data to compute the index + additionnal information (long format)
    GGI: GreenGrowthIndex
        The index computed with the data
    '''

    def __init__(self, data, sustainability_targets):
        '''
        Initialization of the report

        Parameters
        ----------
        data: pd.DataFrame
            A data frame with all in the data to compute the index + additionnal information (long format)
        sustainability_targets: pd.DataFrame
            The sustainability targets
        '''
        super(IndexReport, self).__init__()
        self.data = self.add_infos_data(data)
        indicators = self.get_indicator_from_data(data)
        self.GGI = GreenGrowthIndex(indicators, sustainability_targets)

    def add_infos_data(self, data):
        '''
        Add information useful for display in charts

        Parameters
        ----------
        data: pd.DataFrame
            A data frame with all in the data to compute the index + additionnal information (long format)
        '''
        data['Country'] = ISO_to_Country(data.ISO)
        data.loc[:, 'Imputed from Year'] = data['Imputed from Year'].apply(lambda x: str(x).split('.')[0])
        data.loc[data.From == 'IMPUTED', 'From'] = (data['From'] + ' ' + data['Imputed From'] + ' ' + data['Imputed from Year']).fillna('')
        data['Text'] = data['Country'] + '<br>' + data['Source'].apply(lambda x: " ".join(x.split(' ')[0:10]) + ' ...') + '<br>' + data['From'] + '<br>' + data['Year'].astype(str)
        return data

    def get_indicator_from_data(self, data):
        '''
        Format long data into wide to feed the GreenGrowthIndex

        (TO IMPROVE)

        Parameters
        ----------
        data: pd.DataFrame
            A data frame with all in the data to compute the index + additionnal information (long format)
        '''
        Indicators = data.pivot(index='ISO', columns='Indicator', values='Value')
        Indicators.columns.name = None

        inds = set(Indicators.columns)
        ref_inds = set(self.IND_CAT_DIM['Indicator'].values)
        diffs = ref_inds - inds

        for ind in diffs:
            print(f'WARNING: No data for {ind}, adding empty column')
            Indicators[ind] = np.nan
        return Indicators

    def indicators_dimension_contient(self, dimension, continent, save=None):
        '''
        Report on the indicators for a given dimension and continent.

        This is split this way to avoid having too much information on a single chart.

        (To IMPROVE)

        Parameters
        ----------
        dimension: str
            The dimension to display
        continent: str
            The continent to display
        save: str
            The path to save the plotly chart as HTML
        '''

        indicator_names = self.IND_CAT_DIM[self.IND_CAT_DIM.Dimension == dimension]['Indicator'].values
        df = self.data[(self.data.Indicator.isin(indicator_names)) & (self.data.Continent == continent)]
        df = df.pivot(index=['ISO'], columns=["Indicator"], values=['Value', 'Text'])

        value_df = df['Value']
        hover_text = "%{text} <br>%{x}"

        fig = make_subplots(rows=1,
                            cols=value_df.columns.shape[0],
                            subplot_titles=value_df.columns,
                            y_title='ISO')

        for k, col in enumerate(value_df.columns):

            fig.add_trace(go.Bar(y=value_df.index,
                                 x=value_df[col],
                                 orientation='h',
                                 text=df['Text'][col],
                                 marker=dict(opacity=0.5),
                                 hovertemplate=hover_text,
                                 name=col),
                          row=1,
                          col=k + 1)

        fig.update_layout(height=1000, width=value_df.shape[1] * 200,
                          title_text=f"{dimension} indicators {continent}")
        fig.show()

        if save:
            fig.write_html(f"{save}/Report_indicators_{dimension}_{continent}.html")
