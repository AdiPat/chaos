import warnings
from .order import Order
from .version import Version


warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings:",
    category=UserWarning,
    module="pydantic.main",
)

__version__ = Version.CURRENT_VERSION
__author__ = "Aditya Patange (AdiPat)"
__license__ = "MIT"
__description__ = "Chaos is a minimal, AI-based entropy analyzer for Python developers."
__url__ = "https://www.github.com/AdiPat/chaos"

__all__ = ["Order"]
