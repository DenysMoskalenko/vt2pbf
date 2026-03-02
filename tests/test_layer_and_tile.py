import pytest

from tests.data import VECTOR_TILE
from vt2pbf import parse_from_string, vt2pbf
from vt2pbf.exceptions import InvalidFeatureError, LayerExistError
from vt2pbf.service.layer import Layer
from vt2pbf.service.tile import Tile


def test_layer_validate_feature_missing_field():
    # Missing 'tags'
    invalid_feature = {
        'geometry': [[0, 0], [1, 1]],
        'type': 2,
    }
    with pytest.raises(InvalidFeatureError):
        Layer._validate_feature(invalid_feature)


def test_tile_add_layer_duplicate_raises():
    tile = Tile()
    tile.add_layer('roads', features=[])
    with pytest.raises(LayerExistError):
        tile.add_layer('roads', features=[])


def test_round_trip_encode_and_parse():
    pbf = vt2pbf(VECTOR_TILE)
    tile = parse_from_string(pbf)
    assert isinstance(tile, Tile)
    assert len(tile.tile_pbf.layers) == 1
    assert tile.tile_pbf.layers[0].name == 'geojsonLayer'
