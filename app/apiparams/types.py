"""Definitions of types used to cast incoming query parameters to the desired db-compatible format. If the input
parameter is of an invalid format then exceptions should be raised. """
import iso8601
from rdflib import URIRef, Literal

from app.clients.sparql.namespaces import namespaces as NS


class BoolFromString:
    """Converts string to Python boolean."""
    def __new__(cls, bool_str):
        if bool_str not in ['true', 'True', 'false', 'False']:
            raise ValueError(f'"{bool_str}" is not a valid boolean string')
        real_bool = True if bool_str in ['true', 'True'] else False
        return real_bool


class MediaUriRef(URIRef):
    """Convert 'video'/'audio' to DCMI term."""
    def __new__(cls, media_str):
        if media_str == 'video':
            uriref = NS['dct'].MovingImage
        elif media_str == 'audio':
            uriref = NS['dct'].Sound
        else:
            raise ValueError('Invalid media type')
        return URIRef(uriref)


class LowercaseLiteral(Literal):
    """Convert string to a lower case Literal."""
    def __new__(cls, str_lit):
        return Literal(str_lit.lower())


class ValidatedDatetime(str):
    """Check that datetime is valid by parsing it, if valid then return the input string."""
    def __new__(cls, datetime: str):
        datetime = datetime[1:] if datetime.startswith('P') else datetime
        iso8601.parse_date(datetime)
        return datetime


class StrictlyPositiveInt(int):
    """Raise exception if int < 1."""
    def __new__(cls, integer):
        integer = int(integer)
        if integer < 1:
            raise ValueError('Integer must be greater than 0')
        return integer


class URIStr(str):
    """Raise exception if URI cannot be cast as and rdflib URIRef."""
    def __new__(cls, uri_str):
        u = URIRef(uri_str)
        try:
            u.n3()
        except Exception:
            raise ValueError(f'{uri_str} does not look like a valid URI')
        return uri_str


class LowercaseStr(str):
    def __new__(cls, string):
        if not isinstance(string, str):
            raise TypeError(f'"{string}" is not a string')
        return string.lower()
