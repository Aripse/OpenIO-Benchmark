from oio import ObjectStorageApi
from oio.account.client import AccountClient


def retrieveAllDataFromContainer(client, container):
    s = ObjectStorageApi("OPENIO")
    # print(s.object_list(client, container)['objects'])
    for element in s.object_list(client, container)['objects']:
        meta, stream = s.object_fetch(client, container, element['name'])

        with open(element['name'], 'w+b') as e:
            e.write(b"".join(stream))
