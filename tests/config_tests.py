import os

import functools

from typing import Callable
from typing import ParamSpec
from typing import TypeVar

TEST_RESULTS_DIR = os.path.abspath("test_figs")

if not os.path.exists(TEST_RESULTS_DIR): 
    os.makedirs(TEST_RESULTS_DIR, exist_ok = True)

T = TypeVar("T")
R = ParamSpec("R")

SCREEN_WIDTH, SCREEN_HEIGHT = 20, 20


def test_wrapper(f: Callable[R, T]) -> Callable[R, T]:
    @functools.wraps(f)
    def inner(*args: R.args, **kwargs: R.kwargs) -> T:
        print(f"INFO:\tTesting {f.__class__.__name__} in {__file__}")
        return f(*args, **kwargs)
    return inner

