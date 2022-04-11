class ParseVectorTileError(Exception):
    pass


class LayerExistError(ParseVectorTileError):
    pass


class InvalidFeatureError(ParseVectorTileError):
    pass
