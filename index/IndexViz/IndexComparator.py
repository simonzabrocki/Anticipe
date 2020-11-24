import pandas as pd
from ggindex.utils import ISO_to_Country
from ggindex.GreenGrowthStuff import GreenGrowthStuff
import plotly.express as px


class IndexComparator(GreenGrowthStuff):
    '''
    A class to compare two GreenGrowthIndex.

    For now it is used as a debbuging tool to find problem within the data. Later it will be expended to fit the need for analysis.

    Attributes
    ----------
    GGI_1: GreenGrowthIndex
        The first GreenGrowthIndex
    GG1_2: GreenGrowthIndex
        The second GreenGrowthIndex
    name_GGI_1: str
        Name of the first GreenGrowthIndex
    name_GGI_2: str
        Name of the second GreenGrowthIndex
    hover_text: str
        Text to be displayed on graphs
    '''
    def __init__(self, GGI_1, GGI_2, name_GGI_1='_ref', name_GGI_2='_new'):
        '''
        Initialization

        Parameters
        ----------
        GGI_1: GreenGrowthIndex
            The first GreenGrowthIndex
        GG1_2: GreenGrowthIndex
            The second GreenGrowthIndex
        name_GGI_1: str
            Name of the first GreenGrowthIndex
        name_GGI_2: str
            Name of the second GreenGrowthIndex
        '''
        super(IndexComparator, self).__init__()

        self.GGI_1 = GGI_1
        self.GGI_2 = GGI_2
        self.name_GGI_1, self.name_GGI_2 = name_GGI_1, name_GGI_2

        self.hover_text = "%{text}<br>" + f"{self.name_GGI_1}: " + \
            "%{x}</br>" + f"{self.name_GGI_2}: " + "%{y}"

        self.data = self.merge_data()

    def format_data(self, GGI, name_GGI):
        '''
        Format the data from GGI to be plotable

        Parameters
        ----------
        GGI: GreenGrowthIndex
            A GreenGrowthIndex object
        name_GGI: str
            Name of the GreenGrowthIndex
        '''
        data = GGI.to_long().rename(columns={'Value': f'Value{name_GGI}'})
        data[f'Rank{name_GGI}'] = data.groupby(['Variable'])[f'Value{name_GGI}'].rank(ascending=False)
        data.set_index(['Aggregation', 'Variable'], inplace=True, append=True)
        return data

    def merge_data(self):
        '''
        Merge the data from the two GreenGrowthIndex to allow for plotting
        '''
        data_1 = self.format_data(self.GGI_1, self.name_GGI_1)
        data_2 = self.format_data(self.GGI_2, self.name_GGI_2)
        data = pd.concat([data_1, data_2], axis=1).reset_index()
        data['Country'] = ISO_to_Country(data['ISO'])
        return data.set_index('ISO')

    def make_plot(self, df, to_plot='Value'):
        '''
        Core function to make correlation plots

        Parameters
        ----------
        df: pd.DataFrame
            A DataFrame fromatted in the format_data function way.
        to_plot: str
            Value or Rank to plot either ranks or values
        '''

        col1 = f"{to_plot}{self.name_GGI_1}"
        col2 = f"{to_plot}{self.name_GGI_2}"
        n_col = 2
        n_variables = df.Variable.unique().shape[0]
        n_rows = n_variables // n_col

        fig = px.scatter(df,
                         x=col1, y=col2,
                         color='Variable',
                         facet_col="Variable",
                         facet_col_wrap=n_col,
                         hover_name='Country',
                         hover_data=[col1, col2],
                         facet_col_spacing=0.05,
                         )

        if n_variables == 1:
            fig.update_layout(height=800, width=800)

        else:
            fig.update_layout(height=n_rows * 400, width=n_col * 400)

        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_traces(marker=dict(opacity=0.5))
        fig.update_layout(showlegend=False)

        return fig

    def compare_index(self, by='Value'):
        '''
        Correlation plot of Index 1 and Index 2

        Parameters
        ----------
        by: str
            Value or Rank to plot either ranks or values
        '''
        df = self.data[self.data['Aggregation'] == 'Index']
        fig = self.make_plot(df, to_plot=by)
        fig.update_layout(title=f'Index ({by})')
        return fig

    def compare_dimensions(self, by='Value'):
        '''
        Correlation plot of Dimensions 1 and Dimensions 2

        Parameters
        ----------
        by: str
            Value or Rank to plot either ranks or values
        '''
        df = self.data[self.data['Aggregation'] == 'Dimension']
        fig = self.make_plot(df, to_plot=by)
        fig.update_layout(title=f'Dimensions ({by})')
        return fig

    def compare_categories(self, by='Value'):
        '''
        Correlation plot of Categories 1 and Categories 2

        Parameters
        ----------
        by: str
            Value or Rank to plot either ranks or values
        '''
        df = self.data[self.data['Aggregation'] == 'Category']
        fig = self.make_plot(df, to_plot=by)
        fig.update_layout(title=f'Categories ({by})')
        return fig

    def compare_indicators_in_dimension(self, dimension, by):
        '''
        Correlation plot of Indicators 1 and Indicators 2 in Dimension

        Parameters
        ----------
        dimension: str
            A dimension of the Index
        by: str
            Value or Rank to plot either ranks or values
        '''
        indicator_names = self.IND_CAT_DIM.set_index('Dimension').loc[dimension]['Indicator'].values
        df = self.data[(self.data['Aggregation'] == 'Indicator') & (self.data.Variable.isin(indicator_names))]
        fig = self.make_plot(df, to_plot=by)
        fig.update_yaxes(showticklabels=True)
        fig.update_xaxes(showticklabels=True)
        fig.update_layout(title=f'Indicators in {dimension} ({by})')
        return fig

    def compare_normalized_indicators_in_dimension(self, dimension, by):
        '''
        Correlation plot of NORMALIZED Indicators 1 and NORMALIZED Indicators 2 in Dimension

        Parameters
        ----------
        dimension: str
            A dimension of the Index
        by: str
            Value or Rank to plot either ranks or values
        '''
        indicator_names = self.IND_CAT_DIM.set_index('Dimension').loc[dimension]['Indicator'].values
        df = self.data[(self.data['Aggregation'] == 'Indicator_normed') & (self.data.Variable.isin(indicator_names))]
        fig = self.make_plot(df, to_plot=by)
        fig.update_layout(title=f'Normalized Indicators in {dimension} ({by})')
        return fig
