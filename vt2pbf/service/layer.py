from vt2pbf.config import EXTEND, VERSION
from vt2pbf.exceptions import InvalidFeatureError
from vt2pbf.service.feature import Feature


class Layer:
    def __init__(self, tile_pbf, name: str, extend: int = EXTEND):
        self._tile_pbf = tile_pbf
        self.extend = extend
        self.layer_pbf = self._create_layer(name)
        self.last_key_idx = 0
        self.last_value_idx = 0
        self.key_indices = {}
        self.value_indices = {}

    def _create_layer(self, name: str):
        layer = self._tile_pbf.layers.add()
        layer.name = name
        layer.version = VERSION
        layer.extent = self.extend
        return layer

    def add_feature(self, feature_info: dict, feature_id: int = None):
        self._validate_feature(feature_info)
        feature = Feature(
            layer=self, feature_type=feature_info['type'], feature_id=feature_id or feature_info.get('id')
        )
        feature.add_tags(tags=feature_info['tags'])
        feature.add_geometry(geometry=feature_info['geometry'])

    @staticmethod
    def _validate_feature(feature_info: dict):
        if not Feature.REQUIRED_FIELDS.issubset(feature_info):
            raise InvalidFeatureError(f'Feature must provide all required fields: {Feature.REQUIRED_FIELDS}')
