class EncodeVectorTileError(Exception):
    pass


class LayerExistError(EncodeVectorTileError):
    pass


class InvalidFeatureError(EncodeVectorTileError):
    pass


class WrongFeatureTypeError(InvalidFeatureError):
    pass
