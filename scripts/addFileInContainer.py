from oio import ObjectStorageApi
from oio.account.client import AccountClient
import argparse
import os


def addFileInContainer(container, path):
    s = ObjectStorageApi("OPENIO", endpoint="http://169.254.205.203:6006")
    client="admin"
    fileName = os.path.basename(path)
    #print(client)
    #print(container)
    #print(path)
    with open(path, 'rb') as f:
        s.object_create(client, container, obj_name=fileName, data=f)
        meta, stream = s.object_fetch(client, container, fileName)

ac = AccountClient({"namespace": "OPENIO"})


parser = argparse.ArgumentParser(
    description='Put a file in the container you desire and for a specific account for a client.')

parser.add_argument('container', type=str, nargs='?',
                    help='The container you want to put the file in')

parser.add_argument('path', type=str, nargs='?',
                    help='The path of the file you want to put inside the cluster')

args = parser.parse_args()

addFileInContainer(args.container, args.path)
