import random

try:
    import matplotlib
    from matplotlib import pyplot as plt  # noqa
except ImportError:
    matplotlib = None
    plt = None

try:
    import numpy as np
except ImportError:
    np = None

try:
    import pandas as pd
    from pandas.core.base import PandasObject
except ImportError:
    pd = None
    PandasObject = object

try:
    import scipy.stats
    from scipy.optimize import minimize
    from scipy.stats import t
except ImportError:
    scipy = None
    minimize = None
    t = None

try:
    import sklearn.cluster
    import sklearn.covariance
    import sklearn.manifold
    from sklearn.utils import resample
except ImportError:
    sklearn = None
    resample = None

try:
    from packaging.version import Version
except ImportError:
    Version = None

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None

from . import utils
from .utils import fmtn, fmtp, fmtpn, get_freq_name

_PANDAS_TWO = Version(pd.__version__) >= Version("2")
_PANDAS_TWO_TWO = Version(pd.__version__) >= Version("2.2")

if _PANDAS_TWO_TWO:
    _MonthEnd = "ME"
    _YearEnd = "YE"
else:
    _MonthEnd = "M"
    _YearEnd = "Y"

# module level variable, can be different for non traditional markets (eg. crypto - 360)
TRADING_DAYS_PER_YEAR = 252


class PerformanceStats(object):
    """
    PerformanceStats is a convenience class used for the performance
    evaluation of a price series. It contains various helper functions
    to help with plotting and contains a large amount of descriptive
    statistics.

    Args:
        * prices (Series): A price series.
        * rf (float, Series): `Risk-free rate <https://www.investopedia.com/terms/r/risk-freerate.asp>`_ used in various calculation. Should be
            expressed as a yearly (annualized) return if it is a float. Otherwise
            rf should be a price series.

    Attributes:
        * name (str): Name, derived from price series name
        * return_table (DataFrame): A table of monthly returns with
            YTD figures as well.
        * lookback_returns (Series): Returns for different
            lookback periods (1m, 3m, 6m, ytd...)
        * stats (Series): A series that contains all the stats
        * annualization_factor (float): `Annualization factor` used in various calculations; aka `nperiods`, `252`

    """

    def __init__(self, prices, rf=0.0, annualization_factor=None):
        super(PerformanceStats, self).__init__()
        self.prices = prices
        self.name = self.prices.name
        self._start = self.prices.index[0]
        self._end = self.prices.index[-1]

        self.rf = rf
        # None means "infer from data"; a numeric value means "user-provided"
        self._annualization_factor_override = annualization_factor
        self.annualization_factor = TRADING_DAYS_PER_YEAR if annualization_factor is None else annualization_factor

        self._update(self.prices)

    def set_riskfree_rate(self, rf):
        """
        Set annual risk-free rate property and calculate properly annualized
        monthly and daily rates. Then performance stats are recalculated.
        Affects only this instance of the PerformanceStats.

        Args:
            * rf (float): Annual `risk-free rate <https://www.investopedia.com/terms/r/risk-freerate.asp>`_
        """
        pass

    def _update(self, obj):
        # calc
        pass

    def _calculate(self, obj):
        # default values
        pass

    def _stats(self):
        pass

    def set_date_range(self, start=None, end=None):
        """
        Update date range of stats, charts, etc. If None then
        the original date is used. So to reset to the original
        range, just call with no args.

        Args:
            * start (date): start date
            * end (end): end date

        """
        pass

    def display(self):
        """
        Displays an overview containing descriptive stats for the Series
        provided.
        """
        pass

    def display_monthly_returns(self):
        """
        Display a table containing monthly returns and ytd returns
        for every year in range.
        """
        pass

    def display_lookback_returns(self):
        """
        Displays the current lookback returns.
        """
        pass

    def _get_default_plot_title(self, name, freq, kind):
        pass

    def plot(self, freq=None, figsize=(15, 5), title=None, logy=False, **kwargs):
        """
        Helper function for plotting the series.

        Args:
            * freq (str): Data frequency used for display purposes.
                Refer to pandas docs for valid freq strings.
            * figsize ((x,y)): figure size
            * title (str): Title if default not appropriate
            * logy (bool): log-scale for y axis
            * kwargs: passed to pandas' plot method
        """
        pass

    def plot_histogram(self, freq=None, figsize=(15, 5), title=None, bins=20, **kwargs):
        """
        Plots a histogram of returns given a return frequency.

        Args:
            * freq (str): Data frequency used for display purposes.
                This will dictate the type of returns
                (daily returns, monthly, ...)
                Refer to pandas docs for valid period strings.
            * figsize ((x,y)): figure size
            * title (str): Title if default not appropriate
            * bins (int): number of bins for the histogram
            * kwargs: passed to pandas' hist method
        """
        pass

    def _get_series(self, freq):
        pass

    def _create_stats_series(self):
        pass

    def to_csv(self, sep=",", path=None):
        """
        Returns a CSV string with appropriate formatting.
        If path is not None, the string will be saved to file
        at path.

        Args:
            * sep (char): Separator
            * path (str): If None, CSV string returned. Else file written
                to specified path.
        """
        pass


class GroupStats(dict):
    """
    GroupStats enables one to compare multiple series side by side.
    It is a wrapper around a dict of {price.name: PerformanceStats} and
    provides many convenience methods.

    The order of the series passed in will be preserved.
    Individual PerformanceStats objects can be accessed via index
    position or name via the [] accessor.

    Args:
        * prices (Series): Multiple price series to be compared.

    Attributes:
        * stats (DataFrame): Dataframe containing stats for each
            series provided.  Stats in rows, series in columns.
        * lookback_returns (DataFrame): Returns for diffrent
            lookback periods (1m, 3m, 6m, ytd...)
            Period in rows, series in columns.
        * prices (DataFrame): The merged and rebased prices.

    """

    def __init__(self, *prices):
        names = []
        for p in prices:
            if isinstance(p, pd.DataFrame):
                names.extend(p.columns)
            elif isinstance(p, pd.Series):
                names.append(p.name)
            else:
                print("else")
                names.append(getattr(p, "name", "n/a"))
        self._names = names

        # store original prices
        self._prices = merge(*prices).dropna()

        # proper ordering
        self._prices = self._prices[self._names]

        # check for duplicate columns
        if len(self._prices.columns) != len(set(self._prices.columns)):
            raise ValueError(
                "One or more data series provided",
                "have same name! Please provide unique names",
            )

        self._start = self._prices.index[0]
        self._end = self._prices.index[-1]
        # calculate stats for entire series
        self._update(self._prices)

    def __getitem__(self, key):
        if isinstance(key, int):
            # if type(key) == int:
            return self[self._names[key]]
        else:
            return self.get(key)

    def _update(self, data):
        pass

    def _calculate(self, data):
        pass

    def _stats(self):
        pass

    def _update_stats(self):
        # lookback returns dataframe
        pass

    def _get_default_plot_title(self, freq, kind):
        pass

    def set_riskfree_rate(self, rf):
        """
        Set annual `risk-free rate <https://www.investopedia.com/terms/r/risk-freerate.asp>`_ property and calculate properly annualized
        monthly and daily rates. Then performance stats are recalculated.
        Affects only those instances of PerformanceStats that are children of
        this GroupStats object.

        Args:
            * rf (float, Series): Annual risk-free rate or risk-free rate price series
        """
        pass

    def set_date_range(self, start=None, end=None):
        """
        Update date range of stats, charts, etc. If None then
        the original date range is used. So to reset to the original
        range, just call with no args.

        Args:
            * start (date): start date
            * end (end): end date
        """
        pass

    def display(self):
        """
        Display summary stats table.
        """
        pass

    def display_lookback_returns(self):
        """
        Displays the current lookback returns for each series.
        """
        pass

    def plot(self, freq=None, figsize=(15, 5), title=None, logy=False, **kwargs):
        """
        Helper function for plotting the series.

        Args:
            * freq (str): Data frequency used for display purposes.
                Refer to pandas docs for valid freq strings.
            * figsize ((x,y)): figure size
            * title (str): Title if default not appropriate
            * logy (bool): log-scale for y axis
            * kwargs: passed to pandas' plot method

        """
        pass

    def plot_scatter_matrix(self, freq=None, title=None, figsize=(10, 10), **kwargs):
        """
        Wrapper around pandas' scatter_matrix.

        Args:
            * freq (str): Data frequency used for display purposes.
                Refer to pandas docs for valid freq strings.
            * figsize ((x,y)): figure size
            * title (str): Title if default not appropriate
            * kwargs: passed to pandas' scatter_matrix method

        """
        pass

    def plot_histograms(self, freq=None, title=None, figsize=(10, 10), **kwargs):
        """
        Wrapper around pandas' hist.

        Args:
            * freq (str): Data frequency used for display purposes.
                Refer to pandas docs for valid freq strings.
            * figsize ((x,y)): figure size
            * title (str): Title if default not appropriate
            * kwargs: passed to pandas' hist method

        """
        pass

    def plot_correlation(self, freq=None, title=None, figsize=(12, 6), **kwargs):
        """
        Utility function to plot correlations.

        Args:
            * freq (str): Pandas data frequency alias string
            * title (str): Plot title
            * figsize (tuple (x,y)): figure size
            * kwargs: passed to Pandas' plot_corr_heatmap function

        """
        pass

    def _get_series(self, freq):
        pass

    def to_csv(self, sep=",", path=None):
        """
        Returns a CSV string with appropriate formatting.
        If path is not None, the string will be saved to file
        at path.

        Args:
            * sep (char): Separator
            * path (str): If None, CSV string returned. Else file
                written to specified path.

        """
        pass


def to_returns(prices):
    """
    Calculates the simple arithmetic returns of a price series.

    Formula is: (t1 / t0) - 1

    Args:
        * prices: Expects a price series

    """
    pass


def to_log_returns(prices):
    """
    Calculates the log returns of a price series.

    Formula is: ln(p1/p0)

    Args:
        * prices: Expects a price series

    """
    pass


def to_price_index(returns, start=100):
    """
    Returns a price index given a series of returns.

    Args:
        * returns: Expects a return series
        * start (number): Starting level

    Assumes arithmetic returns.

    The first value of the returned price index is always ``start``.
    When the return series begins with NaN (as produced by
    :func:`to_returns`), the NaN position is replaced by ``start`` and
    the output length equals the input length.  Otherwise ``start`` is
    prepended so that every return is reflected in the prices and the
    round-trip ``to_returns(to_price_index(r))`` recovers *r*.

    Formula is: start, start * cumprod(1+r)
    """
    pass


def rebase(prices, value=100):
    """
    Rebase all series to a given intial value.

    This makes comparing/plotting different series
    together easier.

    Args:
        * prices: Expects a price series
        * value (number): starting value for all series.

    """
    pass


def calc_perf_stats(prices, risk_free_rate=0.0, annualization_factor=252):
    """
    Calculates the performance statistics given an object.
    The object should be a Series of prices.

    A PerformanceStats object will be returned containing all the stats.

    Args:
        * prices (Series): Series of prices
        * risk_free_rate (float, Series): Annual risk-free rate or risk-free rate price series
        * annualization_factor (int): Annualizing factor. Default is 252 (trading days)

    """
    pass


def calc_stats(prices):
    """
    Calculates performance stats of a given object.

    If object is Series, a PerformanceStats object is
    returned. If object is DataFrame, a GroupStats object
    is returned.

    Args:
        * prices (Series, DataFrame): Set of prices
    """
    pass


def to_drawdown_series(prices):
    """
    Calculates the `drawdown <https://www.investopedia.com/terms/d/drawdown.asp>`_ series.

    This returns a series representing a drawdown.
    When the price is at all time highs, the drawdown
    is 0. However, when prices are below high water marks,
    the drawdown series = current / hwm - 1

    The max drawdown can be obtained by simply calling .min()
    on the result (since the drawdown series is negative)

    Method ignores all gaps of NaN's in the price series.

    Args:
        * prices (Series or DataFrame): Series of prices.

    """
    pass


def calc_mtd(daily_prices, monthly_prices):
    """
    Calculates mtd return of a price series.
    Use daily_prices if prices are only available from same month
    else use monthly_prices
    """
    pass


def calc_ytd(daily_prices, yearly_prices):
    """
    Calculates ytd return of a price series.
    Use daily_prices if prices are only available from same year
    else use yearly_prices
    """
    pass


def calc_max_drawdown(prices):
    """
    Calculates the max drawdown of a price series. If you want the
    actual drawdown series, please use to_drawdown_series.
    """
    pass


def drawdown_details(drawdown, index_type=pd.DatetimeIndex):
    """
    Returns a data frame with start, end, days (duration) and
    drawdown for each drawdown in a drawdown series.

    .. note::

        days are actual calendar days, not trading days

    Args:
        * drawdown (pandas.Series): A drawdown Series
            (can be obtained w/ drawdown(prices).
    Returns:
        * pandas.DataFrame -- A data frame with the following
            columns: start, end, days, drawdown.

    """
    pass


def calc_cagr(prices):
    """
    Calculates the `CAGR (compound annual growth rate) <https://www.investopedia.com/terms/c/cagr.asp>`_ for a given price series.

    Args:
        * prices (pandas.Series): A Series of prices.
    Returns:
        * float -- cagr.

    """
    pass


def calc_risk_return_ratio(returns):
    """
    Calculates the return / risk ratio. Basically the
    `Sharpe ratio <https://www.investopedia.com/terms/s/sharperatio.asp>`_ without factoring in the `risk-free rate <https://www.investopedia.com/terms/r/risk-freerate.asp>`_.
    """
    pass


def calc_sharpe(returns, rf=0.0, nperiods=None, annualize=True):
    """
    Calculates the `Sharpe ratio <https://www.investopedia.com/terms/s/sharperatio.asp>`_
    (see `Sharpe vs. Sortino <https://www.investopedia.com/ask/answers/010815/what-difference-between-sharpe-ratio-and-sortino-ratio.asp>`_).

    If rf is non-zero and a float, you must specify nperiods. In this case, rf is assumed
    to be expressed in yearly (annualized) terms.

    Args:
        * returns (Series, DataFrame): Input return series
        * rf (float, Series): `Risk-free rate <https://www.investopedia.com/terms/r/risk-freerate.asp>`_ expressed as a yearly (annualized) return or return series
        * nperiods (int): Frequency of returns (252 for daily, 12 for monthly,
            etc.)

    """
    pass


def calc_information_ratio(returns, benchmark_returns):
    """
    Calculates the `Information ratio <https://www.investopedia.com/terms/i/informationratio.asp>`_ (or `from Wikipedia <http://en.wikipedia.org/wiki/Information_ratio>`_).
    """
    pass


def calc_prob_mom(returns, other_returns):
    """
    `Probabilistic momentum <http://cssanalytics.wordpress.com/2014/01/28/are-simple-momentum-strategies-too-dumb-introducing-probabilistic-momentum/>`_ (see `momentum investing <https://www.investopedia.com/terms/m/momentum_investing.asp>`_)

    Basically the "probability or confidence that one asset
    is going to outperform the other".

    Source:
        http://cssanalytics.wordpress.com/2014/01/28/are-simple-momentum-strategies-too-dumb-introducing-probabilistic-momentum/ # NOQA
    """
    pass


def calc_total_return(prices):
    """
    Calculates the total return of a series.

    last / first - 1
    """
    pass


def year_frac(start, end):
    """
    Similar to excel's yearfrac function. Returns
    a year fraction between two dates (i.e. 1.53 years).

    Approximation using the average number of seconds
    in a year.

    Args:
        * start (datetime): start date
        * end (datetime): end date

    """
    pass


def merge(*series):
    """
    Merge Series and/or DataFrames together.

    Returns a DataFrame.
    """
    pass


def drop_duplicate_cols(df):
    """
    Removes duplicate columns from a dataframe
    and keeps column w/ longest history
    """
    pass


def to_monthly(series, method="ffill", how="end"):
    """
    Convenience method that wraps asfreq_actual
    with 'M' param (method='ffill', how='end').
    """
    pass


def asfreq_actual(series, freq, method="ffill", how="end", normalize=False):
    """
    Similar to pandas' asfreq but keeps the actual dates.
    For example, if last data point in Jan is on the 29th,
    that date will be used instead of the 31st.
    """
    pass


def calc_inv_vol_weights(returns):
    """
    Calculates weights proportional to inverse volatility of each column.

    Returns weights that are inversely proportional to the column's
    volatility resulting in a set of portfolio weights where each position
    has the same level of volatility.

    Note, that assets with returns all equal to NaN or 0 are excluded from
    the portfolio (their weight is set to NaN).

    Returns:
        Series {col_name: weight}
    """
    pass


def calc_mean_var_weights(returns, weight_bounds=(0.0, 1.0), rf=0.0, covar_method="ledoit-wolf", options=None):
    """
    Calculates the mean-variance weights given a DataFrame of returns.

    Args:
        * returns (DataFrame): Returns for multiple securities.
        * weight_bounds ((low, high)): Weigh limits for optimization.
        * rf (float): `Risk-free rate <https://www.investopedia.com/terms/r/risk-freerate.asp>`_ used in utility calculation
        * covar_method (str): Covariance matrix estimation method.
            Currently supported:
                - `ledoit-wolf <http://www.ledoit.net/honey.pdf>`_
                - standard
        * options (dict): options for minimizing, e.g. {'maxiter': 10000 }

    Returns:
        Series {col_name: weight}

    """
    pass


def _erc_weights_slsqp(x0, cov, b, maximum_iterations, tolerance):
    """
    Calculates the equal risk contribution / risk parity weights given
        a DataFrame of returns.

    Args:
    * x0 (np.array): Starting asset weights.
    * cov (np.array): covariance matrix.
    * b (np.array): Risk target weights. By definition target total risk contributions are all equal which makes this redundant.
    * maximum_iterations (int): Maximum iterations in iterative solutions.
    * tolerance (float): Tolerance level in iterative solutions.

    Returns:
    np.array {weight}

    You can read more about ERC at
    http://thierry-roncalli.com/download/erc.pdf

    """
    pass


def _erc_weights_ccd(x0, cov, b, maximum_iterations, tolerance):
    """
    Calculates the equal risk contribution / risk parity weights given
    a DataFrame of returns.

    Args:
        * x0 (np.array): Starting asset weights.
        * cov (np.array): covariance matrix.
        * b (np.array): Risk target weights.
        * maximum_iterations (int): Maximum iterations in iterative solutions.
        * tolerance (float): Tolerance level in iterative solutions.

    Returns:
        np.array {weight}

    Reference:
        Griveau-Billion, Theophile and Richard, Jean-Charles and Roncalli,
        Thierry, A Fast Algorithm for Computing High-Dimensional Risk Parity
        Portfolios (2013).
        Available at SSRN: https://ssrn.com/abstract=2325255

    """
    pass


def calc_erc_weights(
    returns,
    initial_weights=None,
    risk_weights=None,
    covar_method="ledoit-wolf",
    risk_parity_method="ccd",
    maximum_iterations=100,
    tolerance=1e-8,
):
    """
    Calculates the equal risk contribution / risk parity weights given a
    DataFrame of returns.

    Args:
        * returns (DataFrame): Returns for multiple securities.
        * initial_weights (list): Starting asset weights [default inverse vol].
        * risk_weights (list): Risk target weights [default equal weight].
        * covar_method (str): Covariance matrix estimation method.
            Currently supported:
                - `ledoit-wolf <http://www.ledoit.net/honey.pdf>`_ [default]
                - standard
        * risk_parity_method (str): Risk parity estimation method.
            Currently supported:
                - ccd (cyclical coordinate descent)[default]
                - slsqp (scipy's implementation of sequential least squares programming)
        * maximum_iterations (int): Maximum iterations in iterative solutions.
        * tolerance (float): Tolerance level in iterative solutions.

    Returns:
        Series {col_name: weight}

    """
    pass


def get_num_days_required(offset, period="d", perc_required=0.90, annualization_factor=252):
    """
    Estimates the number of days required to assume that data is OK.

    Helper function used to determine if there are enough "good" data
    days over a given period.

    Args:
        * offset (DateOffset): Offset (lookback) period.
        * period (str): Period string.
        * perc_required (float): percentage of number of days
            expected required.

    """
    pass


def calc_clusters(returns, n=None, plot=False):
    """
    Calculates the clusters based on k-means
    clustering.

    Args:
        * returns (pd.DataFrame): DataFrame of returns
        * n (int): Specify # of clusters. If None, this
            will be automatically determined
        * plot (bool): Show plot?

    Returns:
        * dict with structure: {cluster# : [col names]}
    """
    pass


def calc_ftca(returns, threshold=0.5):
    """
    Implementation of David Varadi's `Fast Threshold Clustering Algorithm (FTCA) <http://cssanalytics.wordpress.com/2013/11/26/fast-threshold-clustering-algorithm-ftca/>`_.

    http://cssanalytics.wordpress.com/2013/11/26/fast-threshold-clustering-algorithm-ftca/  # NOQA

    More stable than k-means for clustering purposes.
    If you want more clusters, use a higher threshold.

    Args:
        * returns - expects a pandas dataframe of returns where
            each column is the name of a given security.
        * threshold (float): Threshold parameter - use higher value
            for more clusters. Basically controls how similar
            (correlated) series have to be.
    Returns:
        dict of cluster name (a number) and list of securities in cluster

    """
    pass


def limit_weights(weights, limit=0.1):
    """
    Limits weights and redistributes excedent amount
    proportionally.

    ex:
        - weights are {a: 0.7, b: 0.2, c: 0.1}
        - call with limit=0.5
        - excess 0.2 in a is ditributed to b and c
            proportionally.
            - result is {a: 0.5, b: 0.33, c: 0.167}

    Args:
        * weights (Series): A series describing the weights
        * limit (float): Maximum weight allowed
    """
    pass


def random_weights(n, bounds=(0.0, 1.0), total=1.0):
    """
    Generate pseudo-random weights.

    Returns a list of random weights that is of length
    n, where each weight is in the range bounds, and
    where the weights sum up to total.

    Useful for creating random portfolios when benchmarking.

    Args:
        * n (int): number of random weights
        * bounds ((low, high)): bounds for each weight
        * total (float): total sum of the weights

    """
    pass


def plot_heatmap(data, title="Heatmap", show_legend=True, show_labels=True, label_fmt=".2f", vmin=None, vmax=None, figsize=None, label_color="w", cmap="RdBu", **kwargs):
    """
    Plot a heatmap using matplotlib's pcolor.

    Args:
        * data (DataFrame): DataFrame to plot. Usually small matrix (ex.
            correlation matrix).
        * title (string): Plot title
        * show_legend (bool): Show color legend
        * show_labels (bool): Show value labels
        * label_fmt (str): Label format string
        * vmin (float): Min value for scale
        * vmax (float): Max value for scale
        * cmap (string): Color map
        * kwargs: Passed to matplotlib's pcolor

    """
    pass


def plot_corr_heatmap(data, **kwargs):
    """
    Plots the correlation heatmap for a given DataFrame.
    """
    pass


def rollapply(data, window, fn):
    """
    Apply a function fn over a rolling window of size window.

    Args:
        * data (Series or DataFrame): Series or DataFrame
        * window (int): Window size
        * fn (function): Function to apply over the rolling window.
            For a series, the return value is expected to be a single
            number. For a DataFrame, it shuold return a new row.

    Returns:
        * Object of same dimensions as data
    """
    pass


def _winsorize_wrapper(x, limits):
    """
    Wraps scipy winsorize function to drop na's
    """
    pass


def winsorize(x, axis=0, limits=0.01):
    """
    `Winsorize <https://en.wikipedia.org/wiki/Winsorizing>`_ values based on limits
    """
    pass


def rescale(x, min=0.0, max=1.0, axis=0):
    """
    Rescale values to fit a certain range [min, max]
    """
    pass


def annualize(returns, durations, one_year=365.0):
    """
    Annualize returns using their respective durations.

    Formula used is:
        (1 + returns) ** (1 / (durations / one_year)) - 1

    """
    pass


def deannualize(returns, nperiods):
    """
    Convert return expressed in annual terms on a different basis.

    Args:
        * returns (float, Series, DataFrame): Return(s)
        * nperiods (int): Target basis, typically 252 for daily, 12 for
            monthly, etc.

    """
    pass


def infer_freq(data):
    """
        Infer the most likely frequency given the input index. If the frequency is
    uncertain or index is not DateTime like, just return None
        Args:
            * data (DataFrame, Series): Any timeseries dataframe or series
    """
    pass


def _whole_periods_str_to_nperiods(freq, annualization_factor=None):
    pass


def infer_nperiods(data, annualization_factor=None):
    pass


def calc_sortino_ratio(returns, rf=0.0, nperiods=None, annualize=True):
    """
    Calculates the `Sortino ratio <https://www.investopedia.com/terms/s/sortinoratio.asp>`_ given a series of returns
    (see `Sharpe vs. Sortino <https://www.investopedia.com/ask/answers/010815/what-difference-between-sharpe-ratio-and-sortino-ratio.asp>`_).

    Args:
        * returns (Series or DataFrame): Returns
        * rf (float, Series): `Risk-free rate <https://www.investopedia.com/terms/r/risk-freerate.asp>`_ expressed in yearly (annualized) terms or return series.
        * nperiods (int): Number of periods used for annualization. Must be
            provided if rf is non-zero and rf is not a price series

    """
    pass


def to_excess_returns(returns, rf, nperiods=None):
    """
    Given a series of returns, it will return the excess returns over rf.

    Args:
        * returns (Series, DataFrame): Returns
        * rf (float, Series): `Risk-Free rate(s) <https://www.investopedia.com/terms/r/risk-freerate.asp>`_ expressed in annualized term or return series
        * nperiods (int): Optional. If provided, will convert rf to different
            frequency using deannualize only if rf is a float
    Returns:
        * excess_returns (Series, DataFrame): Returns - rf

    """
    pass


def calc_calmar_ratio(prices):
    """
    Calculates the `Calmar ratio <https://www.investopedia.com/terms/c/calmarratio.asp>`_ given a series of prices

    Args:
        * prices (Series, DataFrame): Price series

    """
    pass


def to_ulcer_index(prices):
    """
    Calculates the Ulcer Index for a series of investment returns.

    Converts from prices -> `Ulcer index <https://www.investopedia.com/terms/u/ulcerindex.asp>`_

    See https://en.wikipedia.org/wiki/Ulcer_index

    Args:
        prices (pandas.Series or numpy.ndarray): A series of investment returns.

    Returns:
        float: The Ulcer Index.
    """
    pass


def to_ulcer_performance_index(prices, rf=0.0, nperiods=None):
    """
    Converts from prices -> `ulcer performance index <https://www.investopedia.com/terms/u/ulcerindex.asp>`_.

    See https://en.wikipedia.org/wiki/Ulcer_index

    Args:
        * prices (Series, DataFrame): Prices
        * rf (float, Series): `Risk-free rate of return <https://www.investopedia.com/terms/r/risk-freerate.asp>`_. Assumed to be expressed in
            yearly (annualized) terms or return series
        * nperiods (int): Used to deannualize rf if rf is provided (non-zero)

    """
    pass


def resample_returns(returns, func, seed=0, num_trials=100):
    """
    Resample the returns and calculate any statistic on every new sample.

    https://en.wikipedia.org/wiki/Resampling_(statistics)

    :param returns (Series, DataFrame): Returns
    :param func: Given the resampled returns calculate a statistic
    :param seed: Seed for random number generator
    :param num_trials: Number of times to resample and run the experiment
    :return: Series of resampled statistics
    """
    pass


def extend_pandas():
    """
    Extends pandas' PandasObject (Series, Series,
    DataFrame) with some functions defined in this file.

    This facilitates common functional composition used in quant
    finance.

    Ex:
        prices.to_returns().dropna().calc_clusters()
        (where prices would be a DataFrame)
    """
    pass
