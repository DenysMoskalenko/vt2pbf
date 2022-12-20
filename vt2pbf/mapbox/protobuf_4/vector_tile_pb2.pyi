from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf.internal import python_message as _python_message
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Tile(_message.Message):
    __slots__ = ["layers"]
    class GeomType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Feature(_message.Message):
        __slots__ = ["geometry", "id", "tags", "type"]
        GEOMETRY_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        TAGS_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        geometry: _containers.RepeatedScalarFieldContainer[int]
        id: int
        tags: _containers.RepeatedScalarFieldContainer[int]
        type: Tile.GeomType
        def __init__(self, id: _Optional[int] = ..., tags: _Optional[_Iterable[int]] = ..., type: _Optional[_Union[Tile.GeomType, str]] = ..., geometry: _Optional[_Iterable[int]] = ...) -> None: ...
    class Layer(_message.Message):
        __slots__ = ["extent", "features", "keys", "name", "values", "version"]
        EXTENT_FIELD_NUMBER: _ClassVar[int]
        Extensions: _python_message._ExtensionDict
        FEATURES_FIELD_NUMBER: _ClassVar[int]
        KEYS_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        extent: int
        features: _containers.RepeatedCompositeFieldContainer[Tile.Feature]
        keys: _containers.RepeatedScalarFieldContainer[str]
        name: str
        values: _containers.RepeatedCompositeFieldContainer[Tile.Value]
        version: int
        def __init__(self, version: _Optional[int] = ..., name: _Optional[str] = ..., features: _Optional[_Iterable[_Union[Tile.Feature, _Mapping]]] = ..., keys: _Optional[_Iterable[str]] = ..., values: _Optional[_Iterable[_Union[Tile.Value, _Mapping]]] = ..., extent: _Optional[int] = ...) -> None: ...
    class Value(_message.Message):
        __slots__ = ["bool_value", "double_value", "float_value", "int_value", "sint_value", "string_value", "uint_value"]
        BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
        DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
        Extensions: _python_message._ExtensionDict
        FLOAT_VALUE_FIELD_NUMBER: _ClassVar[int]
        INT_VALUE_FIELD_NUMBER: _ClassVar[int]
        SINT_VALUE_FIELD_NUMBER: _ClassVar[int]
        STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
        UINT_VALUE_FIELD_NUMBER: _ClassVar[int]
        bool_value: bool
        double_value: float
        float_value: float
        int_value: int
        sint_value: int
        string_value: str
        uint_value: int
        def __init__(self, string_value: _Optional[str] = ..., float_value: _Optional[float] = ..., double_value: _Optional[float] = ..., int_value: _Optional[int] = ..., uint_value: _Optional[int] = ..., sint_value: _Optional[int] = ..., bool_value: bool = ...) -> None: ...
    Extensions: _python_message._ExtensionDict
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    LINESTRING: Tile.GeomType
    POINT: Tile.GeomType
    POLYGON: Tile.GeomType
    UNKNOWN: Tile.GeomType
    layers: _containers.RepeatedCompositeFieldContainer[Tile.Layer]
    def __init__(self, layers: _Optional[_Iterable[_Union[Tile.Layer, _Mapping]]] = ...) -> None: ...
