from dataclasses import dataclass

from ._const import REGION


@dataclass(frozen=True, kw_only=True)
class AuthData:
    """Authentication data necessary for authenticated API requests."""

    token: str
    region: REGION


@dataclass(frozen=True, kw_only=True)
class Device:
    """Device information."""

    id: int
    name: str
    key: str
    product_key: str
