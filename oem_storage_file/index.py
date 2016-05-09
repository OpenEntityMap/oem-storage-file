from oem_framework.models.core import ModelRegistry
from oem_framework.plugin import Plugin
from oem_framework.storage import IndexStorage
from oem_storage_file.core.base import BaseFileStorage
from oem_storage_file.metadata import MetadataFileStorage

import os


class IndexFileStorage(IndexStorage, BaseFileStorage, Plugin):
    __key__ = 'file/index'

    def __init__(self, parent):
        super(IndexFileStorage, self).__init__()

        self.parent = parent

        self.path = None

    @classmethod
    def open(cls, parent):
        storage = cls(parent)
        storage.initialize(parent._client)
        return storage

    def initialize(self, client):
        super(IndexFileStorage, self).initialize(client)

        self.path = os.path.join(self.parent.path, 'index.%s' % self.format.__extension__)

    def load(self, collection):
        return self.main.format.from_path(
            collection, ModelRegistry['Index'], self.path,
            children=False,
            storage=self
        )

    def parse_metadata(self, collection, key, value):
        return self.main.format.from_dict(
            collection, ModelRegistry['Metadata'], value,
            key=str(key),
            storage=MetadataFileStorage.open(self.parent, key)
        )
