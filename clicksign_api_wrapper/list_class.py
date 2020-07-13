class ListClass:
    def __init__(self, metadata):
        self.metadata = metadata

        for key, item in metadata["list"].items():
            setattr(self, key, item)