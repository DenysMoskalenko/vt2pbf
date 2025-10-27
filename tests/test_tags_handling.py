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
        "str_True": "True",
        "str_False": "False",
    })
    # all these tags should be separate keys and values
    keys = feature.feature.tags[::2]
    values = feature.feature.tags[1::2]
    print(keys, values)
    assert len(set(keys)) == 8
    assert len(set(values)) == 8

def test_only_one_numeric_type():
    tile = Tile()
    layer = Layer(tile.tile_pbf, 'tags')
    feature = Feature(layer=layer, feature_type=2, feature_id=10)
    feature.add_tags({
        "int_1": 1,
        "int_0": 0,
        "float_1": 1.0,
        "float_0": 0.0,
    })
    # numeric values are stored in one type, only, int 1 and float 1.0 are equal
    # total number of tags should be 4 keys + 2 value tags
    keys = feature.feature.tags[::2]
    values = feature.feature.tags[1::2]
    assert len(set(keys)) == 4
    assert len(set(values)) == 2
