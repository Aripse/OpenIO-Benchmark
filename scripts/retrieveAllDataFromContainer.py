from oio import ObjectStorageApi
from oio.account.client import AccountClient


def retrieveAllDataFromContainer(client, container):
    s = ObjectStorageApi("OPENIO")
    # print(s.object_list(client, container)['objects'])
    for element in s.object_list(client, container)['objects']:
        meta, stream = s.object_fetch(client, container, element['name'])

        with open(element['name'], 'w+b') as e:
            e.write(b"".join(stream))


parser = argparse.ArgumentParser(
    description='Retrieve all the files from a certain container and a certain client.')

parser.add_argument('client', type=str, nargs='?',
                    help='The name of the client')

parser.add_argument('container', type=str, nargs='?',
                    help='The name of the container')

args = parser.parse_args()

addFileInContainer(args.client, args.container)
