from vt2pbf.service.feature import command, Feature
from vt2pbf.service.layer import Layer
from vt2pbf.service.tile import Tile


def build_layer():
    tile = Tile()
    layer = Layer(tile.tile_pbf, 'test')
    return layer


def test_point_geometry_encoding():
    layer = build_layer()
    feature = Feature(layer=layer, feature_type=1, feature_id=1)
    # For point features, geometry must be a list of points: [[x, y], ...]
    feature.add_geometry([[10, 15]])
    encoded = list(feature.feature.geometry)
    assert encoded[0] == command(1, 1)
    # MoveTo + two coords
    assert len(encoded) == 3


def test_linestring_geometry_encoding_contains_lineto():
    layer = build_layer()
    feature = Feature(layer=layer, feature_type=2, feature_id=2)
    feature.add_geometry([[[0, 0], [5, 5]]])
    encoded = list(feature.feature.geometry)
    assert command(2, 1) in encoded


def test_polygon_geometry_encoding_ends_with_closepath():
    layer = build_layer()
    feature = Feature(layer=layer, feature_type=3, feature_id=3)
    # Simple square ring
    ring = [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]
    feature.add_geometry([ring])
    encoded = list(feature.feature.geometry)
    assert encoded[-1] == command(7, 1)
