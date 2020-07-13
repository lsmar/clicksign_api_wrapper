class Batch:
    def __init__(self, metadata):
        self.metadata = metadata

        for key, item in metadata["batch"].items():
            setattr(self, key, item)