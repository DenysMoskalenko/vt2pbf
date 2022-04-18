from vt2pbf.service.tile import Tile


def vt2pbf(vector_tile: dict, layer_name: str = 'geojsonLayer', extend: int = None) -> bytes:
    tile = Tile(extend=extend)
    tile.add_layer(layer_name, features=vector_tile['features'])
    pbf_string = tile.serialize_to_bytestring()
    return pbf_string
