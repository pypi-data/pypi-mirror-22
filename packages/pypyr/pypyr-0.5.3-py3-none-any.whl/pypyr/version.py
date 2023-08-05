"""Version information."""

import platform

__version__ = '0.5.3'


def get_version():
    return (f'pypyr {__version__} '
            f'python {platform.python_version()}')
