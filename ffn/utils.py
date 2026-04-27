import pickle
import re
from typing import List, Sequence, Tuple, Union

try:
    import decorator
except ImportError:
    decorator = None

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    from packaging.version import Version
except ImportError:
    Version = None


def _memoize(func, *args, **kw):
    # should we refresh the cache?
    pass


def memoize(f, refresh_keyword="mrefresh"):
    """
    Memoize decorator. The refresh keyword is the keyword
    used to bypass the cache (in the function call).
    """
    pass


def parse_arg(arg: Union[str, List[str], Tuple[str]]):
    """
    Parses arguments for convenience. Argument can be a
    csv list ('a,b,c'), a string, a list, a tuple.

    Returns a list.
    """
    pass


def clean_ticker(ticker: str) -> str:
    """
    Cleans a ticker for easier use throughout MoneyTree

    Splits by space and only keeps first bit. Also removes
    any characters that are not letters. Returns as lowercase.

    >>> clean_ticker('^VIX')
    'vix'
    >>> clean_ticker('SPX Index')
    'spx'
    """
    pass


def clean_tickers(tickers: Sequence[str]) -> List[str]:
    """
    Maps clean_ticker over tickers.
    """
    pass


def fmtp(number: float) -> str:
    """
    Formatting helper - percent
    """
    pass


def fmtpn(number: float) -> str:
    """
    Formatting helper - percent no % sign
    """
    pass


def fmtn(number: float) -> str:
    """
    Formatting helper - float
    """
    pass


def get_freq_name(period: str) -> Union[str, None]:
    pass


def scale(val: float, src: Sequence[float], dst: Sequence[float]) -> float:
    """
    Scale value from src range to dst range.
    If value outside bounds, it is clipped and set to
    the low or high bound of dst.

    Ex:
        scale(0, (0.0, 99.0), (-1.0, 1.0)) == -1.0
        scale(-5, (0.0, 99.0), (-1.0, 1.0)) == -1.0

    """
    pass


def as_percent(self, digits=2):
    pass


def as_format(item: Union[pd.DataFrame, pd.Series], format_str=".2f") -> Union[pd.DataFrame, pd.Series]:
    """
    Map a format string over a pandas object.
    """
    pass
