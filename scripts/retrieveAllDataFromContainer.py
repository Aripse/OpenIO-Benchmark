from oio import ObjectStorageApi
from oio.account.client import AccountClient
import argparse
import os


def retrieveAllDataFromContainer(container):
    s = ObjectStorageApi("OPENIO",endpoint="http://169.254.205.203:6006")
    client="admin"
    # print(s.object_list(client, container)['objects'])
    for element in s.object_list(client, container)['objects']:
        meta, stream = s.object_fetch(client, container, element['name'])

        with open(element['name'], 'w+b') as e:
            e.write(b"".join(stream))

parser = argparse.ArgumentParser(
    description='Retrieve all the files from a certain container and a certain client.')

parser.add_argument('container', type=str, nargs='?',
                    help='The name of the container')

args = parser.parse_args()

retrieveAllDataFromContainer(args.container)
