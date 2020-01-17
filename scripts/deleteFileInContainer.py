from oio import ObjectStorageApi
from oio.account.client import AccountClient


def deleteFileInContainer(client, container, fileName):
    s = ObjectStorageApi("OPENIO")
    s.object_delete(client, container, filename)
