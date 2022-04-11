class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


def command(cmd, length):
    return (length << 3) | (cmd & 0x7)


def zigzag(delta):
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

    def add_geometry(self, geometry: list[list[list[int]]]):
        geometry = self._encode_feature_geometry(geometry)
        self.feature.geometry.extend(geometry)

    def _encode_feature_geometry(self, raw_geometry: list[list[list[int]]]) -> list[int]:
        geometry = self._load_geometry(raw_geometry)
        x = 0
        y = 0
        rings = len(geometry)
        geom = []
        for r in range(rings):
            ring = geometry[r]
            count = 1
            if self.feature_type == 1:
                count = len(ring)
            geom.append(command(1, count))
            line_count = len(ring) - 1 if self.feature_type == 3 else len(ring)
            for i in range(line_count):
                if i == 1 and self.feature_type != 1:
                    geom.append(command(2, line_count - 1))
                dx = ring[i].x - x
                dy = ring[i].y - y
                geom.append(zigzag(dx))
                geom.append(zigzag(dy))
                x += dx
                y += dy
            if self.feature_type == 3:
                geom.append(command(7, 1))  # closepath
        return geom

    @staticmethod
    def _load_geometry(raw_geometry: list) -> list[list[Point]]:
        rings = raw_geometry
        geometry = []
        for i in range(len(rings)):
            ring = rings[i]
            new_ring = []
            for j in range(len(ring)):
                new_ring.append(Point(x=ring[j][0], y=ring[j][1]))
            geometry.append(new_ring)
        return geometry

    def add_tags(self, tags: dict):
        for k, v in tags.items():
            if v is None:
                continue

            if k not in self._layer.key_indices:
                self._layer.key_indices[k] = self._layer.last_key_idx
                self._layer.last_key_idx += 1
                self._layer_pbf.keys.append(k)
            self.feature.tags.append(self._layer.key_indices[k])

            if v not in self._layer.value_indices:
                self._layer.value_indices[v] = self._layer.last_value_idx
                self._layer.last_value_idx += 1
                value = self._layer_pbf.values.add()
                if isinstance(v, bool):
                    value.bool_value = v
                elif isinstance(v, str):
                    value.string_value = v
                elif isinstance(v, int):
                    # value.int_value = v
                    if v < 0:
                        value.sint_value = v
                    else:
                        value.uint_value = v
                elif isinstance(v, float):
                    value.double_value = v
            self.feature.tags.append(self._layer.value_indices[v])
