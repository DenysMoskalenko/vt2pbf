from vt2pbf.service.feature import Feature
from vt2pbf.service.layer import Layer
from vt2pbf.service.tile import Tile


def test_none_tag_values_are_ignored():
    tile = Tile()
    layer = Layer(tile.tile_pbf, 'tags')
    feature = Feature(layer=layer, feature_type=2, feature_id=10)
    feature.add_tags({'a': 1, 'b': None, 'c': 'x'})
    # Only 'a' and 'c' should be encoded -> 2 keys and 2 values = 4 tag indices
    assert len(feature.feature.tags) == 4

def test_correct_type_encoded():
    tile = Tile()
    layer = Layer(tile.tile_pbf, 'tags')
    feature = Feature(layer=layer, feature_type=2, feature_id=10)
    feature.add_tags({
        "boolean_True": True,
        "boolean_False": False,
        "int_1": 1,
        "int_0": 0,
        "str_1": "1",
        "str_0": "0",
    })
    # all these tags should be separate keys and values
    assert len(feature.feature.tags) == 12
