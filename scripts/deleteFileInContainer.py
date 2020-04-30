from oio import ObjectStorageApi
from oio.account.client import AccountClient
import argparse
import os
import yaml

with open("./config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile,  Loader=yaml.FullLoader)

def deleteFileInContainer(client, container, fileName):
    if config['endpoint'] != "":
        s = ObjectStorageApi(config["AccountClientNamespace"], endpoint=config['endpoint'])
    else:
        s = ObjectStorageApi(config["AccountClientNamespace"])
    s.object_delete(client, container, fileName)

ac = AccountClient({"namespace": ObjectStorageApi(config["AccountClientNamespace"]})


parser = argparse.ArgumentParser(
    description='Delete a file in the container you desire and for a specific account for a client.')

parser.add_argument('container', type=str, nargs='?',
                    help='The container you want to put the file in')

parser.add_argument('client', type=str, nargs='?',
                    help='The name of the client associated with this file')

parser.add_argument('fileName', type=str, nargs='?',
                    help='The name of the file you want to put inside the cluster')

args = parser.parse_args()

deleteFileInContainer(args.client, args.container, args.fileName)
