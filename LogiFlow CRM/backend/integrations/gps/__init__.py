"""
Integrações GPS
"""

from .sascar import SascarClient
from .autotrac import AutotracClient
from .onixsat import OnixsatClient

__all__ = ["SascarClient", "AutotracClient", "OnixsatClient"]
