from oio import ObjectStorageApi
from oio.account.client import AccountClient
import argparse
import os


def deleteFileInContainer(container, fileName):
    s = ObjectStorageApi("OPENIO")
    client="admin"
    s.object_delete(client, container, fileName)

ac = AccountClient({"namespace": "OPENIO"})

parser = argparse.ArgumentParser(
    description='Delete a file in the container you desire and for a specific account for a client.')

parser.add_argument('container', type=str, nargs='?',
                    help='The container you want to put the file in')

parser.add_argument('fileName', type=str, nargs='?',
                    help='The name of the file you want to put inside the cluster')

args = parser.parse_args()

deleteFileInContainer(args.container, args.fileName)
