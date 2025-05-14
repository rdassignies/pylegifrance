"""Utility functions for the PyLegifrance package.

This module provides utility functions used across the package.
"""

import requests
from pylegifrance.config import ApiConfig


def configure_session_timeouts(session: requests.Session, config: ApiConfig) -> None:
    """
    Configure default timeouts for all requests in a session.

    This function modifies the session's request method to include default timeouts
    based on the provided configuration.

    Parameters
    ----------
    session : requests.Session
        The session to configure.
    config : ApiConfig
        The configuration containing timeout values.
    """
    original_request = session.request
    session.request = lambda method, url, **kwargs: original_request(
        method=method,
        url=url,
        timeout=kwargs.pop("timeout", (config.connect_timeout, config.read_timeout)),
        **kwargs,
    )
