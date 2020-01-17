from oio import ObjectStorageApi
from oio.account.client import AccountClient


def addFileInContainer(client, container, path, fileName):
    s = ObjectStorageApi("OPENIO")

    with open(path, 'rb') as f:

        s.object_create(client, container, obj_name=fileName,
                        data=f)
        meta, stream = s.object_fetch(client, container, fileName)
