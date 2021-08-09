import pandas as pd
import numpy as np
from index.utils import ISO_to_Everything, geometric_mean
from index.GreenGrowthStuff import GreenGrowthStuff
CAPPING_PRIOR_NORMALIZATION = ['EE1', 'EW2', 'ME2', 'EQ1', 'EQ2', 'EQ3', 'GE1',
                               'GE2', 'GE3', 'GV1', 'SE2', 'SL1'
                               ]


class GreenGrowthIndex(GreenGrowthStuff):
    """
    A class used to represent the Green Growth Index.
    (See technical report for complete methods)
    To improve: Clean up and standardize normalize step !
    Attributes
    ----------
    indicators : pd.DataFrame
        Raw indicators used to compute index
    sustainability_targets : pd.DataFrame
        Sustainability targets as defined in the report
    categories : pd.DataFrame
        Sub categories of index
    dimensions : pd.DataFrame
        sub dimensions of index
    GGI : pd.Series
        Green growth index
    """

    def __init__(self, indicators, sustainability_targets):
        super(GreenGrowthIndex, self).__init__()
        self.compute(indicators, sustainability_targets)
        return None

    def compute(self, indicators, sustainability_targets):
        """
        Performs the whole pipeline to compute the Green Growth Index
        Saves the intermediate steps into the class attributes
        Parameters
        ----------
        indicators : pd.DataFrame
            Raw indicators
        sustainability_targets : pd.DataFrame
            sustainability targets
        Returns
        -------
        GGI: pd.Series
            a series containing green growth index
        """

        indicators = indicators.copy(deep=True)

        preprocessor = GreenGrowthPreProcessor()

        # Computing stats  on the indicators (min, max, 25th percentile, 75th percentile)
        statistics = preprocessor.compute_statistics(indicators)

        # Taking out outliers from the indicators
        indicators_fenced = preprocessor.cap_indicators(
            indicators, statistics, CAPPING_PRIOR_NORMALIZATION)

        # Normalizing the indicators using sustainability targets
        indicators_normed = GreenGrowthScaler().normalize(indicators_fenced, sustainability_targets)

        # Aggregating indicators into categories
        categories = IndicatorsAggregation().compute(indicators_normed)

        # Aggregating categories into dimensions
        dimensions = CategoriesAggregation().compute(categories)

        # Aggregating dimensions into the green growth index
        Index = DimensionsAggregation().compute(dimensions)

        self.indicators = indicators#.round(2)
        self.statistics = statistics
        self.indicators_normed = indicators_normed#.round(2)
        self.sustainability_targets = sustainability_targets
        self.categories = categories#.round(2)
        self.dimensions = dimensions#.round(2)
        self.Index = pd.DataFrame(Index, columns=['Index'])#.round(2)

        return self

    def to_excel(self, path='GreenIndex.xlsx'):
        '''
        Export all the data into an excel file
        Parameters
        ----------
        path: str
            Path to the excel file
        '''

        xls_info = [
            ('Index', self.Index),
            ('sustainability_targets', self.sustainability_targets),
            ('statistics', self.statistics),
            ('indicators', self.indicators),
            ('indicators_normed', self.indicators_normed),
            ('categories', self.categories),
            ('dimensions', self.dimensions),
        ]

        with pd.ExcelWriter(path) as writer:

            for sheet_name, df in xls_info:
                if sheet_name not in ['sustainability_targets', 'statistics']:
                    df = ISO_to_Everything(df)
                    df.set_index(['Country', 'Continent', 'UNregion', 'Region',
                                  'IncomeLevel'], append=True, inplace=True)
                df.to_excel(writer, sheet_name=sheet_name)

        return None

    def to_long(self):
        names_dfs = [
            ('Index', self.Index),
            ('Indicator', self.indicators),
            ('Indicator_normed', self.indicators_normed),
            ('Category', self.categories),
            ('Dimension', self.dimensions),
        ]
        long_dfs = []
        for name, df in names_dfs:
            df = df.reset_index().melt(id_vars=['ISO'], value_name='Value', var_name='Variable')
            df['Aggregation'] = name
            long_dfs.append(df)
        return pd.concat(long_dfs, axis=0).set_index('ISO')


class GreenGrowthPreProcessor():
    '''Process the indicators before computing the index.

    Attributes:
        indicators_to_cap(List): list of indicators to cap.
    '''

    def __init__(self):
        return None

    def compute_statistics(self, indicators):
        """
        Computes the meta data of the indicators table.
        Parameters
        ----------
        indicators : pd.DataFrame
            Raw indicators
        Returns
        -------
        meta_indicators: pd.DataFrame
            a datafame containing for indicator:
                 - minimum
                 - maximum
                 - Lower fence = 25th percentile - μ x IQR
                 - Upper fence = 75th percentile + μ x IQR
            (IQR = 75th percentile - 25th percentile, with μ = 3.0 the multiplier)
        """
        # Compute stats
        q_75 = indicators.quantile(0.75)
        q_25 = indicators.quantile(0.25)
        indicator_max = indicators.max()
        indicator_min = indicators.min()

        # Store in dataframe
        stats = pd.concat([q_75, q_25, indicator_max, indicator_min], axis=1)
        stats.columns = ['75%', '25%', 'max', 'min']

        # Compute fences
        IQR = stats["75%"] - stats["25%"]
        stats['lower fence'] = stats["25%"] - 3 * IQR
        stats['upper fence'] = stats["75%"] + 3 * IQR

        return stats

    def cap_indicators(self, indicators, statistics, indicators_to_cap):
        """Remove outliers by caping their values.
        (indicators over the upper fence and under the lower fence are replaced by the fences)
        Parameters
        ----------
        indicators : pd.DataFrame
            Raw indicators
        meta_indicators: pd.DataFrame
            output of compute_meta
        Returns
        -------
        indicators: pd.DataFrame
            a datafame containing for indicators without outliers
        """
        indicators = indicators.copy(deep=True)

        upper_fence, lower_fence = statistics["upper fence"], statistics["lower fence"]

        indicators.loc[:, indicators_to_cap] = indicators[indicators_to_cap].apply(lambda x: x.mask(
            x >= upper_fence[x.name], upper_fence[x.name]))
        indicators.loc[:, indicators_to_cap] = indicators[indicators_to_cap].apply(lambda x: x.mask(
            x <= lower_fence[x.name], lower_fence[x.name]))

        return indicators


class GreenGrowthScaler():
    """Scale the Green Growth Indicators.

    Attributes
    ----------
        None
    """

    def __init__(self):
        return None

    def scale_min_max(self, X, maximum, minimum, b, a=1):
        return a + (X - minimum) / (maximum - minimum) * (b - a)

    def normalize_single_target_case(self, X, Xt):
        Xmax = X.max()
        Xmin = X.min()

        max_of_Xt_Xmax = pd.concat((Xt, Xmax), axis=1).max(axis=1)
        min_of_Xt_Xmax = pd.concat((Xt, Xmax), axis=1).min(axis=1)

        b1 = Xmax - Xmin
        b2 = max_of_Xt_Xmax - Xmin
        b = b1 / b2 * 100

        X_norm = self.scale_min_max(X, min_of_Xt_Xmax, Xmin, b)
        X_norm[X_norm > 100] = 100

        return X_norm

    def normalize_double_target_case(self, X, Xt_max, Xt_min):

        X_norm = self.scale_min_max(X, Xt_min, Xt_max, b=100)

        X_norm[X_norm < 1] = 1
        X_norm[X_norm > 100] = 100

        return X_norm

    def normalize(self, indicators, ST):
        """ TO IMPROVE
        Normalize the table of indicators.
        (Wrapper for pandas dataframe apply method)
        Parameters
        ----------
        indicators : pd.DataFrame
            indicators without outliers
        ST : pd.DataFrame
            Sustainability targets as defined in the report
        Returns
        -------
        normalized_indicators: pd.DataFrame
            a datafame containing normalized indicators
        """
        normalized_indicators = indicators.copy(deep=True)

        cases = [('negative', 1, ['Target 1'], lambda X, Xt: GreenGrowthScaler().normalize_single_target_case(-X, -Xt)),  # Case 1
                 ('positive', 1, ['Target 2'], lambda X, Xt: GreenGrowthScaler(
                 ).normalize_single_target_case(X, Xt)),  # Case 2
                 ]

        for case in cases:
            relation = case[0]
            targets = case[2]
            normalize_function = case[3]

            Xt = ST[ST.Relation == relation][targets]
            X = indicators[Xt.index]
            normalized_indicators.loc[:, Xt.index] = normalize_function(X, Xt)

        # Case 3
        Xt = ST[(ST.Relation == "negative") & (
            ST['Number of targets'] == 2)][['Target 1', 'Target 2']]
        X = indicators[Xt.index]

        Xt_min = Xt['Target 1']
        Xt_max = Xt['Target 2']
        normalized_indicators.loc[:, Xt.index] = GreenGrowthScaler(
        ).normalize_double_target_case(X, Xt_max, Xt_min)

        return normalized_indicators


class IndicatorsAggregation(GreenGrowthStuff):
    def __init__(self):
        super(IndicatorsAggregation, self).__init__()

    def compute(self, indicators):
        """ TO IMPROVE
        Aggregates the indicators into 16 categories, using arithmetic mean. Remove the categories not fit for aggregation
        Parameters
        ----------
        indicators : pd.DataFrame
            Normalized indicators
        Returns
        -------
        categories: pd.DataFrame
            a datafame containing indicators aggregated into categories
        """

        # Auxiliary dataframe to aggregate by column name
        transposed = indicators.T.reset_index()
        transposed['index'] = [indic[0:2] for indic in transposed['index'].values]

        # Aggregate the categories
        categories = transposed.copy()
        categories = categories.groupby('index').mean().T
        categories.columns.name = None

        # Select the complete categories
        categories = self.select_complete_categories(categories, transposed)

        return categories

    def select_complete_categories(self, categories, transposed_indicators):
        """
        Parameters
        ----------
        categories : pd.DataFrame
            Categories
        transposed_indicators : pd.DataFrame
            Transposed indicators DataFrame
        Returns
        -------
        categories: pd.DataFrame
            a datafame containing categories fit for next steps
        """
        categories = categories.copy()

        missing_values = transposed_indicators.set_index('index').isnull().groupby(level=0).sum().T
        n_indicators_per_cat = self.IND_CAT_DIM.groupby('Category')['Indicator'].count()

        # Categories with more than 2 indicators (1 missing value allowed)
        select_1 = missing_values[n_indicators_per_cat[(n_indicators_per_cat > 2)].index] <= 1

        # Categories with 2 indicators (0 missing values)
        select_2 = missing_values[n_indicators_per_cat[(n_indicators_per_cat == 2)].index] == 0

        # Categories with 1 indicators (do nothing, will be filtered at next stage)
        select_3 = missing_values[n_indicators_per_cat[(n_indicators_per_cat == 1)].index] >= 0

        select = pd.concat([select_1, select_2, select_3], axis=1)

        return categories[select]


class CategoriesAggregation(GreenGrowthStuff):
    def __init__(self):
        super(CategoriesAggregation, self).__init__()

    def compute(self, categories):
        """ TO IMPROVE
        Aggregates the categories into 4 dimensions using a geometric mean.
        Parameters
        ----------
        categories : pd.DataFrame
            categories (output of aggregate indicators)
        Returns
        -------
        dimensions: pd.DataFrame
            a datafame containing categories aggregated into 4 dimensions
        """

        categories[categories < 1e-7] = np.nan

        transposed = categories.T
        transposed['Dimension'] = self.get_dimensions_from_categories(transposed.index)

        dimensions = []
        for dimension in self.get_dimensions():  # For some reason for loop quicker than groupby apply ?
            df = transposed[transposed.Dimension == dimension].drop(columns='Dimension').T
            dimensions.append(geometric_mean(df, axis=1))
        dimensions = pd.concat(dimensions, axis=1)
        dimensions.columns = self.get_dimensions()

        dimensions = self.select_complete_dimensions(dimensions, transposed)

        return dimensions

    def select_complete_dimensions(self, dimensions, transposed_categories):
        missing_values = transposed_categories.set_index('Dimension').isnull().groupby(level=0).sum().T

        # Allow one or less missing value in a given category
        select = missing_values <= 1

        return dimensions[select]


class DimensionsAggregation(GreenGrowthStuff):
    def __init__(self):
        super(DimensionsAggregation, self).__init__()

    def compute(self, dimensions):
        """
        Aggregates the dimensions into the Green Growth Index using a geometric mean.
        Parameters
        ----------
        dimensions : pd.DataFrame
            dimensions (output of aggregate categories)
        Returns
        -------
        GGI: pd.Series
            a series containing green growth index
        """
        dimensions = dimensions.dropna()  # No missing values allowed final aggregation
        GGI = np.exp(np.log(dimensions.prod(axis=1)) / (dimensions.notna().sum(1)))
        return GGI


class NewCategoriesAggregation(GreenGrowthStuff):
    def __init__(self):
        super(NewCategoriesAggregation, self).__init__()

    def compute(self, categories):
        """ TO IMPROVE
        Aggregates the categories into 4 dimensions using a geometric mean.
        Parameters
        ----------
        categories : pd.DataFrame
            categories (output of aggregate indicators)
        Returns
        -------
        dimensions: pd.DataFrame
            a datafame containing categories aggregated into 4 dimensions
        """

        categories[categories < 1e-7] = np.nan

        transposed = categories.T
        transposed['Dimension'] = self.get_dimensions_from_categories(transposed.index)

        dimensions = []
        for dimension in ['ESRU', 'NCP', 'SI']:
            df = transposed[transposed.Dimension == dimension].drop(columns='Dimension').T
            dimensions.append(geometric_mean(df, axis=1))

        for dimension in ['GEO']:
            df = transposed[transposed.Dimension == dimension].drop(columns='Dimension').T
            df = df.apply(lambda x: x.nlargest(2), axis=1)  # New aggregation method
            dimensions.append(geometric_mean(df, axis=1))

        dimensions = pd.concat(dimensions, axis=1)
        dimensions.columns = ['ESRU', 'NCP', 'SI', 'GEO']
        dimensions[['ESRU', 'NCP', 'SI']] = self.select_complete_dimensions(
            dimensions[['ESRU', 'NCP', 'SI']], transposed)

        # dimensions = self.select_complete_dimensions(dimensions, transposed)

        return dimensions

    def select_complete_dimensions(self, dimensions, transposed_categories):
        missing_values = transposed_categories.set_index('Dimension').isnull().groupby(level=0).sum().T

        # Allow one or less missing value in a given category
        select = missing_values <= 1

        return dimensions[select]


class NewGreenGrowthIndex(GreenGrowthIndex):

    def __init__(self, indicators, sustainability_targets):
        super(NewGreenGrowthIndex, self).__init__(indicators, sustainability_targets)

    def compute(self, indicators, sustainability_targets):
        """
        Performs the whole pipeline to compute the Green Growth Index
        Saves the intermediate steps into the class attributes
        Parameters
        ----------
        indicators : pd.DataFrame
            Raw indicators
        sustainability_targets : pd.DataFrame
            sustainability targets
        Returns
        -------
        GGI: pd.Series
            a series containing green growth index
        """

        indicators = indicators.copy(deep=True)

        preprocessor = GreenGrowthPreProcessor()

        # Computing stats  on the indicators (min, max, 25th percentile, 75th percentile)
        statistics = preprocessor.compute_statistics(indicators)

        # Taking out outliers from the indicators
        indicators_fenced = preprocessor.cap_indicators(
            indicators, statistics, CAPPING_PRIOR_NORMALIZATION)

        # Normalizing the indicators using sustainability targets
        indicators_normed = GreenGrowthScaler().normalize(indicators_fenced, sustainability_targets)

        # Aggregating indicators into categories
        categories = IndicatorsAggregation().compute(indicators_normed)

        # Aggregating categories into dimensions
        dimensions = NewCategoriesAggregation().compute(categories)  # THIS IS THE NEW AGGREGATION !!!

        # Aggregating dimensions into the green growth index
        Index = DimensionsAggregation().compute(dimensions)

        self.indicators = indicators.round(2)
        self.statistics = statistics
        self.indicators_normed = indicators_normed.round(2)
        self.sustainability_targets = sustainability_targets
        self.categories = categories.round(2)
        self.dimensions = dimensions.round(2)
        self.Index = pd.DataFrame(Index, columns=['Index']).round(2)

        return self
