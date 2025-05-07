# -*- coding: utf-8 -*-
from __future__ import annotations

from functools import lru_cache

from ._register_font import (
    RegisteredFont,
    _fc_register_font,
    _fc_unregister_font,
    _list_fonts,
    _register_font,
    _unregister_font,
)

__all__ = [
    "fc_register_font",
    "fc_unregister_font",
    "list_fonts",
    "register_font",
    "unregister_font",
    "registered_fonts",
    "RegisteredFont",
]

# An set of all registered font paths
registered_fonts: set[RegisteredFont] = set()


def fc_register_font(font_path: str) -> None:
    """This function registers the font file using ``fontconfig`` so that
    it is available for use by Pango. On Linux it is aliased to
    :func:`register_font` and on Windows and macOS this would work only when
    using ``fontconfig`` backend.

    Parameters
    ==========
    font_path : :class:`str`
        Relative or absolute path to font file.

    Returns
    =======
    :class:`bool`
            True means it worked without any error.
            False means there was an unknown error

    Examples
    ========
    >>> register_font("/home/roboto.tff")
    True

    Raises
    ======
    AssertionError
        The :param:`font_path` specified doesn't exist.
    """
    return _fc_register_font(registered_fonts, font_path)


def fc_unregister_font(font_path: str) -> None:
    """This function unregister (removes) the font file using
    ``fontconfig``. It is mostly optional to call this.
    Mainly used in tests. On Linux it is aliased to
    :func:`unregister_font` and on Windows and macOS this
    would work only when using ``fontconfig`` backend.

    Parameters
    ==========
    font_path: :class:`str`
        For compatibility with the windows function.

    Returns
    =======
    :class:`bool`
            True means it worked without any error.
            False means there was an unknown error

    """
    return _fc_unregister_font(registered_fonts, font_path)


def register_font(font_path: str) -> None:
    """This function registers the font file using native OS API
    to make the font available for use by Pango. On Linux it is
    aliased to :func:`fc_register_font` and on Windows and macOS
    it uses the native API.

    Parameters
    ==========
    font_path: :class:`str`
        Relative or absolute path to font file.

    Returns
    =======
    :class:`bool`
            True means it worked without any error.
            False means there was an unknown error

    Examples
    ========
    >>> register_font("C:/home/roboto.tff")
    True

    Raises
    ======
    AssertionError
        The :param:`font_path` specified doesn't exist.
    """
    return _register_font(registered_fonts, font_path)


def unregister_font(font_path: str) -> None:
    """This function unregister (removes) the font file using native OS API.
    It is mostly optional to call this. Mainly used in tests. On Linux it is
    aliased to :func:`fc_unregister_font` and on Windows and macOS it uses
    the native API.

    Parameters
    ==========
    font_path: :class:`str`
        Relative or absolute path to font file.

    Returns
    =======
    :class:`bool`
            True means it worked without any error.
            False means there was an unknown error

    Examples
    ========
    >>> unregister_font("C:/home/roboto.tff")
    True

    Raises
    ======
    AssertionError
        The :param:`font_path` specified doesn't exist.

    """
    return _unregister_font(registered_fonts, font_path)


def list_fonts() -> list:
    """Lists the fonts available to Pango.
    This is usually same as system fonts but it also
    includes the fonts added through :func:`register_font`
    or :func:`fc_register_font`.

    Returns
    -------

    :class:`list` :
        List of fonts sorted alphabetically.
    """
    return lru_cache(maxsize=None)(_list_fonts)(
        tuple(sorted(registered_fonts, key=lambda x: x.path))
    )
