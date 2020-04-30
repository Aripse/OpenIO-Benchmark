from oio import ObjectStorageApi
from oio.account.client import AccountClient
import argparse
import os
import yaml

with open("./config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile,  Loader=yaml.FullLoader)

def addFileInContainer(container, path, client):
    if config['endpoint'] != "":
        s = ObjectStorageApi(config["AccountClientNamespace"], endpoint=config['endpoint'])
    else:
        s = ObjectStorageApi(config["AccountClientNamespace"])
    fileName = os.path.basename(path)

    #try/except
    with open(path, 'rb') as f:
        s.object_create(client, container, obj_name=fileName, data=f)
        meta, stream = s.object_fetch(client, container, fileName)

ac = AccountClient({"namespace": config["AccountClientNamespace"]})


parser = argparse.ArgumentParser(
    description='Put a file in the container you desire and for a specific account for a client.')

parser.add_argument('container', type=str, nargs='?',
                    help='The container you want to put the file in')

parser.add_argument('client', type=str, nargs='?',
                    help='The client you for whom you want to add the file')

parser.add_argument('path', type=str, nargs='?',
                    help='The path of the file you want to put inside the cluster')



args = parser.parse_args()

addFileInContainer(args.container, args.path, args.client)
