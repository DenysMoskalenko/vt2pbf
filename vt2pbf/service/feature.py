from typing import List, Union

from vt2pbf.exceptions import WrongFeatureTypeError


def command(cmd: int, length: int) -> int:
    return (length << 3) | (cmd & 0x7)


def zigzag(delta: Union[int, float]) -> int:
    if isinstance(delta, float):
        delta = int(delta)
    return (delta << 1) ^ (delta >> 31)


class Feature:
    REQUIRED_FIELDS = {'geometry', 'type', 'tags'}

    def __init__(self, layer, feature_type: int, feature_id: int = None):
        """
        Leading the mapbox proto spec, feature type must follow next schema:
             UNKNOWN = 0;
             POINT = 1;
             LINESTRING = 2;
             POLYGON = 3;
        """
        self._layer = layer
        self._layer_pbf = layer.layer_pbf
        self.feature_type = feature_type
        self.feature = self._create_feature(feature_id)

    def _create_feature(self, feature_id: int = None):
        feature = self._layer_pbf.features.add()
        if feature_id is not None:
            feature.id = feature_id
        feature.type = self.feature_type
        return feature

    def add_tags(self, tags: dict):
        for k, v in tags.items():
            if v is None:
                continue

            # as dict keys, False == 0, True == 1
            # see https://stackoverflow.com/q/22275027
            if isinstance(v, bool):
                v_ = str(v)
            else:
                v_ = v

            if k not in self._layer.key_indices:
                self._layer.key_indices[k] = self._layer.last_key_idx
                self._layer.last_key_idx += 1
                self._layer_pbf.keys.append(k)
            self.feature.tags.append(self._layer.key_indices[k])

            if v_ not in self._layer.value_indices:
                self._layer.value_indices[v_] = self._layer.last_value_idx
                self._layer.last_value_idx += 1
                self._write_value(instance=self._layer_pbf.values.add(), value=v)
            self.feature.tags.append(self._layer.value_indices[v_])

    @staticmethod
    def _write_value(instance, value: Union[bool, str, int, float]):
        if isinstance(value, bool):
            instance.bool_value = value
        elif isinstance(value, str):
            instance.string_value = value
        elif isinstance(value, float):
            instance.double_value = value
        elif isinstance(value, int):
            # setattr(instance, 'sint_value' if value < 0 else 'unit_value', value)
            if value < 0:
                instance.sint_value = value
            else:
                instance.uint_value = value
        else:
            raise WrongFeatureTypeError(f'{value} type is not support, must be one of [bool, str, int, float]')

    def add_geometry(self, geometry: Union[List[List[int]], List[List[List[int]]]]):
        geometry = [geometry] if self.feature_type == 1 else geometry
        encoded_geometry = self._encode_feature_geometry(geometry)
        self.feature.geometry.extend(encoded_geometry)

    def _encode_feature_geometry(self, raw_geometry: List[List[List[int]]]) -> List[int]:
        x = 0
        y = 0
        result = []
        for ring in raw_geometry:
            count = len(ring) if self.feature_type == 1 else 1
            result.append(command(1, count))

            line_count = len(ring) - 1 if self.feature_type == 3 else len(ring)
            for i in range(line_count):
                if i == 1 and self.feature_type != 1:
                    result.append(command(2, line_count - 1))
                dx = ring[i][0] - x
                dy = ring[i][1] - y
                result.append(zigzag(dx))
                result.append(zigzag(dy))
                x += dx
                y += dy
            if self.feature_type == 3:
                result.append(command(7, 1))  # closepath
        return result
