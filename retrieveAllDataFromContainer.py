import os

try:
    from oio import ObjectStorageApi
except ImportError:
        input("Cannot load module ObjectStorageApi from oio. Press enter to install the package oio or Ctrl+c to quit the program")
        os.system("pip3 install git+https://github.com/open-io/oio-sds.git@6.1.0.0a0")
        from oio import ObjectStorageApi

try:
    from oio.account.client import AccountClient
except ImportError:
        input("Cannot load module AccountClient from oio.account.client. Press enter to install the package oio or Ctrl+c to quit the program")
        os.system("pip3 install git+https://github.com/open-io/oio-sds.git@6.1.0.0a0")
        from oio.account.client import AccountClient

try:
    import argparse
except ImportError:
        input("Cannot load module argparse. Press enter to install the package argparse or Ctrl+c to quit the program")
        os.system("pip3 install argparse")
        import argparse

try:
    import os.path
except ImportError:
        input("Cannot load module os.path. Press enter to install the package os.path or Ctrl+c to quit the program")
        os.system("pip3 install --user os.path")
        import os.path

try:
    import yaml
except ImportError:
        input("Cannot load module yaml. Press enter to install the package yaml or Ctrl+c to quit the program")
        os.system("pip3 install pyyaml")
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
