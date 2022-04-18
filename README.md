# geojson2vt
Python port of [JS vt-pbf](https://github.com/mapbox/vt-pbf) to Encode [Mapbox vector tiles](https://github.com/mapbox/vector-tile-spec) to binary protobufs in python.
Right now available only version 2 of mapbox vector tiles spec

### Install
`vt2pbf` is available on [PyPi](https://pypi.org/project/vt2pbf/).  

Install using pip.
```bash
pip install vt2pbf
```

Import `geojson2vt`
```python
from vt2pbf import vt2pbf
```

### Usage
Firstly you need to make a vector tile. You can do it by your own or use some libraries to convert,
for example geojson into vector tiles using python port of [geojson-vt](https://github.com/mapbox/geojson-vt)
library - [geojson2vt](https://github.com/geometalab/geojson2vt)

After you can easily encode your vector tile into pbf:
```python
# build an initial index of tiles
tile_index = geojson2vt(geojson, {})

# request a particular tile
vector_tile = tile_index.get_tile(z, x, y)

# encode vector tile into pbf
pbf = vt2pbf(vector_tile)
print(pbf) # b'\x1a\xfb\x01\n\x0cgeojsonLayer\...'
```

`vt2pbf` takes two additional arguments:
- `layer_name` is a name of encoded layer, `default='geojsonLayer'`,
- `extend` is definition of the extent of the tile, `default=4096`

### Additional usage
You also can encode  any custom information in pbf by [Mapbox vector tiles spec](https://github.com/mapbox/vector-tile-spec)
```python
from vt2pbf import Tile


tile = Tile(extend=extend)
tile.add_layer(layer_name, features=features)  # features in vector_tile format (close to vector_tile['features'])
tile.add_layer(other_layer_name, features=features)
pbf_string = tile.serialize_to_bytestring()
print(pbf_string) # b'\x1a\xfb\x01\n\x0cgeojsonLayer\...'
```

In addition you can parse encoded data from bytestring using:
```python
from vt2pbf import parse_from_string

pbf_string = b'\x1a\xfb\x01\n\x0cgeojsonLayer\...'
tile = parse_from_string(pbf_string)
print(tile.tile_pbf)
# layers {
#   name: "geojsonLayer"
#   features {
#     tags: 0
#     ...
```
Right now you cannot add some additional layers or info to parsed tile, but it will be available in future


## Acknowledgements
All the credit of tile encoding belongs to the collaborators of [JS vt-pbf](https://github.com/mapbox/vt-pbf).
