from tests.data import VECTOR_TILE, VECTOR_TILE_PBF
from vt2pbf import vt2pbf


def test_encode_vt_into_pbf():
    pbf = vt2pbf(VECTOR_TILE)
    assert pbf == VECTOR_TILE_PBF
