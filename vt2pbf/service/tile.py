from typing import List

from vt2pbf.config import EXTEND
from vt2pbf.exceptions import LayerExistError
from vt2pbf.service.layer import Layer

from google import protobuf
if int(protobuf.__version__.split(".")[0]) < 4:
    from vt2pbf.mapbox.protobuf_3 import vector_tile_pb2
else:
    from vt2pbf.mapbox.protobuf_4 import vector_tile_pb2


class Tile:
    def __init__(self, extend: int = None):
        self.tile_pbf = vector_tile_pb2.Tile()
        self.extend = extend or EXTEND
        self._layers = {}

    def serialize_to_bytestring(self) -> bytes:
        return self.tile_pbf.SerializeToString()

    def add_layer(self, name: str, features: List[dict]):
        if name in self._layers:
            raise LayerExistError('Layer with this name already exist in the tile')

        layer = Layer(self.tile_pbf, name, extend=self.extend)
        for feature in features:
            layer.add_feature(feature)

        self._layers[name] = layer


def parse_from_string(pbf_string: bytes) -> Tile:
    tile = Tile()
    tile.tile_pbf.ParseFromString(pbf_string)
    return tile.tile_pbf
