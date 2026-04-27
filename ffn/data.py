import warnings
from typing import Sequence, Union

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import yfinance
except ImportError:
    yfinance = None

try:
    import ffn
except ImportError:
    ffn = None

from . import utils


@utils.memoize
def get(
    tickers: Sequence[str],
    provider=None,
    common_dates=True,
    forward_fill=False,
    clean_tickers=True,
    column_names=None,
    ticker_field_sep=":",
    mrefresh=False,
    existing=None,
    **kwargs,
) -> pd.DataFrame:
    """
    Helper function for retrieving data as a DataFrame.

    Args:
        * tickers (list, string, csv string): Tickers to download.
        * provider (function): Provider to use for downloading data.
            By default it will be ffn.DEFAULT_PROVIDER if not provided.
        * common_dates (bool): Keep common dates only? Drop na's.
        * forward_fill (bool): forward fill values if missing. Only works
            if common_dates is False, since common_dates will remove
            all nan's, so no filling forward necessary.
        * clean_tickers (bool): Should the tickers be 'cleaned' using
            ffn.utils.clean_tickers? Basically remove non-standard
            characters (^VIX -> vix) and standardize to lower case.
        * column_names (list): List of column names if clean_tickers
            is not satisfactory.
        * ticker_field_sep (char): separator used to determine the
            ticker and field. This is in case we want to specify
            particular, non-default fields. For example, we might
            want: AAPL:Low,AAPL:High,AAPL:Close. ':' is the separator.
        * mrefresh (bool): Ignore memoization.
        * existing (DataFrame): Existing DataFrame to append returns
            to - used when we download from multiple sources
        * kwargs: passed to provider

    """
    pass


def web(ticker: str, field=None, start=None, end=None, mrefresh=False, source="yahoo"):
    """
    Data provider wrapper around pandas.io.data provider. Provides
    memoization.
    """
    pass


@utils.memoize
def yf(ticker: str, field, start=None, end=None, mrefresh=False) -> Union[pd.Series, pd.DataFrame]:
    pass


@utils.memoize
def csv(ticker: str, path="data.csv", field="", mrefresh=False, **kwargs) -> pd.Series:
    """
    Data provider wrapper around pandas' read_csv. Provides memoization.
    """
    pass


DEFAULT_PROVIDER = yf
