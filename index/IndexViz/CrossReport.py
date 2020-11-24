import pandas as pd
from ggindex.IndexViz.IndexReport import IndexReport
from ggindex.IndexViz.IndexComparator import IndexComparator
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from ggindex.GreenGrowthStuff import GreenGrowthStuff


class IndexCrossReport(GreenGrowthStuff):
    '''
    A class to compare two GreenGrowthIndex AND the data used to compute them.
    It is more general than the IndexComparator which only compare the GreenGrowthIndex with looking at the data.

    Attributes
    ----------
    Report_1: IndexReport
        The IndexReport of the first GreenGrowthIndex using first data
    name_1: str
        Name of the first Report
    Report_2: IndexReport
        The IndexReport of the second GreenGrowthIndex using first data
    name_2: str
        Name of the second Report
    IndexComparator: IndexComparator
        The comparison of first and second GreenGrowthIndex
    data: pd.DataFrame
        The full data of the first and second Index
    '''

    def __init__(self, data_1, ST_1, name_1, data_2, ST_2, name_2):
        '''
        Initialization

        Parameters
        ----------
        data_1: pd.DataFrame
            The data to compute the first GreenGrowthIndex
        ST_1: DataFrame
            The sustainable targets to compute the first GreenGrowthIndex
        name_1: str
            Name of the first GreenGrowthIndex and Data
        data_2: pd.DataFrame
            The data to compute the second GreenGrowthIndex
        ST_2: DataFrame
            The sustainable targets to compute the second GreenGrowthIndex
        name_2: str
            Name of the second GreenGrowthIndex and Data
        '''
        super(IndexCrossReport, self).__init__()

        self.Report_1 = IndexReport(data_1, ST_1)
        self.Report_2 = IndexReport(data_2, ST_2)
        self.name_1 = name_1
        self.name_2 = name_2
        self.IndexComparator = IndexComparator(self.Report_1.GGI,
                                               self.Report_2.GGI,
                                               name_GGI_1=name_1,
                                               name_GGI_2=name_2)

        self.data = self.merge_data(data_1, data_2, name_1, name_2)

    def add_normalized_to_data(self, data, GGI):
        '''
        Add the normalized value to the dataframe
        '''
        data = data.copy().set_index(['ISO', 'Indicator'])
        value_normed = GGI.to_long()
        value_normed = value_normed[value_normed.Aggregation == 'Indicator_normed'].drop(columns=['Aggregation']).dropna().set_index('Variable', append=True)
        data['Value_normalized'] = value_normed['Value']
        return data.reset_index()

    def merge_data(self, data_1, data_2, name_1, name_2):
        '''
        TO DO
        '''
        data_1['name'] = name_1
        data_2['name'] = name_2
        data_1 = self.add_normalized_to_data(data_1, self.Report_1.GGI)
        data_2 = self.add_normalized_to_data(data_2, self.Report_2.GGI)
        df = pd.concat([data_1, data_2], axis=0)
        return df

    def cross_indicators_dimension_continent(self, dimension, continent, normalized=True, save=None):
        '''
        TO DO
        '''
        if normalized:
            value = 'Value_normalized'
            title = f"{dimension} indicators normalized {continent}: {self.name_1} and {self.name_2}"
            save_name = f'CrossReport_indicators_normalized_{dimension}_{continent}'
        else:
            value = 'Value'
            title = f"{dimension} indicators {continent}: {self.name_1} and {self.name_2}"
            save_name = f'CrossReport_indicators_{dimension}_{continent}'

        indicator_names = self.IND_CAT_DIM[self.IND_CAT_DIM.Dimension ==
                                           dimension]['Indicator'].values
        df = self.data[(self.data.Indicator.isin(indicator_names))
                       & (self.data.Continent == continent)]
        hover_text = "%{text} <br>%{x}"

        fig = make_subplots(rows=1,
                            cols=len(indicator_names),
                            subplot_titles=indicator_names,
                            y_title='ISO')

        for k, ind in enumerate(indicator_names):
            tmp_df = df[df.Indicator == ind].set_index('name')
            fig.add_trace(go.Bar(y=tmp_df.loc[self.name_1]['ISO'],
                                 x=tmp_df.loc[self.name_1][value],
                                 orientation='h',
                                 marker=dict(opacity=0.5),
                                 marker_color='red',
                                 hovertemplate=hover_text,
                                 text=tmp_df.loc[self.name_1]['Text'],
                                 name=self.name_1,
                                 width=0.4,
                                 ),
                          row=1,
                          col=k + 1)

            fig.add_trace(go.Bar(y=tmp_df.loc[self.name_2]['ISO'],
                                 x=tmp_df.loc[self.name_2][value],
                                 orientation='h',
                                 marker=dict(opacity=0.5),
                                 hovertemplate=hover_text,
                                 text=tmp_df.loc[self.name_2]['Text'],
                                 marker_color='blue',
                                 width=0.4,
                                 name=self.name_2,
                                 ),
                          row=1,
                          col=k + 1)

        fig.update_layout(height=1000, width=len(indicator_names) * 200,
                          title_text=title,
                          hoverlabel_align='right',
                          showlegend=False,
                          barmode='group')

        if save:
            fig.write_html(f"{save}/{save_name}.html")

        return fig

    def cross_indicators_ISO(self, ISO, normalized=True, save=None):
        '''
        TO DO
        '''
        if normalized:
            value = 'Value_normalized'
        else:
            value = 'Value'

        df = self.data[(self.data.ISO == ISO)]

        country = df['Country'].unique()[0]

        indicator_names = self.IND_CAT_DIM['Indicator'].to_numpy().reshape(18, 2)
        hover_text = "%{text} <br>%{x}"

        fig = make_subplots(rows=18, cols=2,
                            subplot_titles=indicator_names.flatten())

        for (x, y), ind in np.ndenumerate(indicator_names):
            row = x + 1
            col = y + 1
            tmp_df = df[df.Indicator == ind]
            fig.add_trace(go.Bar(x=tmp_df[value],
                                 y=tmp_df['name'],
                                 width=0.1,
                                 marker=dict(opacity=0.5),
                                 orientation='h',
                                 marker_color=['red', 'blue'],
                                 ),
                          row=row,
                          col=col)
            fig.add_trace(go.Scatter(x=tmp_df[value],
                                     y=tmp_df['name'],
                                     marker=dict(opacity=0.99, size=10),
                                     marker_color=['red', 'blue'],
                                     mode='markers',
                                     text=tmp_df['Text'],
                                     hovertemplate=hover_text,
                                     ),
                          row=row,
                          col=col)
            # hover text goes here
        fig.update_layout(height=100 * 18, width=2 * 400,
                          title_text=f"indicators {country} {ISO}",
                          showlegend=False,
                          hoverlabel_align='right', barmode='group')

        if save:
            fig.write_html(f"{save}/CrossReport_indicators_{ISO}.html")

        return fig
