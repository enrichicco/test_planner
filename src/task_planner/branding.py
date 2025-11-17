"""
Co-branding configuration for the Task Planner application.

Supports multiple brands with different color schemes and logos.
Brand detection is based on:
1. Session cookie (highest priority)
2. URL/domain (fallback)
"""

from dataclasses import dataclass
from typing import Literal


BrandName = Literal["plugin", "mcr"]


@dataclass
class BrandConfig:
    """Brand configuration."""

    name: str
    display_name: str
    primary_color: str
    primary_color_dark: str
    primary_color_light: str
    logo_path: str
    favicon_path: str
    website_url: str
    domains: list[str]


# Brand configurations
BRANDS: dict[BrandName, BrandConfig] = {
    "plugin": BrandConfig(
        name="plugin",
        display_name="Plug-in",
        primary_color="#ed5400",
        primary_color_dark="#c94700",
        primary_color_light="#ff6a1a",
        logo_path="/static/img/logo-plugin.png",
        favicon_path="/static/img/favicon-plugin.ico",
        website_url="https://www.plug-in.it",
        domains=["plugin.local", "plugin.com", "plug-in.it"],
    ),
    "mcr": BrandConfig(
        name="mcr",
        display_name="MCR",
        primary_color="#ed1c23",
        primary_color_dark="#c91820",
        primary_color_light="#ff3038",
        logo_path="/static/img/logo-mcr.png",
        favicon_path="/static/img/favicon-mcr.ico",
        website_url="https://www.gruppomcr.com",
        domains=["mcr.local", "mcr.com", "gruppomcr.com"],
    ),
}

# Default brand
DEFAULT_BRAND: BrandName = "plugin"


def get_brand_from_domain(host: str) -> BrandName:
    """
    Determine brand from domain/host.

    Args:
        host: The host/domain string from the request

    Returns:
        Brand name
    """
    host_lower = host.lower()

    # Check each brand's domains
    for brand_name, config in BRANDS.items():
        for domain in config.domains:
            if domain in host_lower:
                return brand_name  # type: ignore

    return DEFAULT_BRAND


def get_brand_config(brand_name: BrandName | None = None) -> BrandConfig:
    """
    Get brand configuration.

    Args:
        brand_name: Brand name, defaults to DEFAULT_BRAND

    Returns:
        Brand configuration
    """
    if brand_name is None:
        brand_name = DEFAULT_BRAND

    return BRANDS.get(brand_name, BRANDS[DEFAULT_BRAND])
