from oio import ObjectStorageApi
from oio.account.client import AccountClient
import argparse
import os
import yaml

with open("./config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile,  Loader=yaml.FullLoader)

def retrieveAllDataFromContainer(client, container):
    if config['endpoint'] != "":
        s = ObjectStorageApi(config["AccountClientNamespace"], endpoint=config['endpoint'])
    else:
        s = ObjectStorageApi(config["AccountClientNamespace"])
    # print(s.object_list(client, container)['objects'])
    for element in s.object_list(client, container)['objects']:
        meta, stream = s.object_fetch(client, container, element['name'])

        with open(element['name'], 'w+b') as e:
            e.write(b"".join(stream))

ac = AccountClient({"namespace": config["AccountClientNamespace"]})

parser = argparse.ArgumentParser(
    description='Retrieve all the files from a certain container and a certain client.')

parser.add_argument('container', type=str, nargs='?',
                    help='The name of the container')

parser.add_argument('client', type=str, nargs='?',
                    help='The name of the client')

args = parser.parse_args()

retrieveAllDataFromContainer(args.client, args.container)
