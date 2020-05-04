from datetime import date, timedelta, datetime
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

def retrieveDataForAGivenPeriod(client, container, period):
    if config['endpoint'] != "":
        s = ObjectStorageApi(config["AccountClientNamespace"], endpoint=config['endpoint'])
    else:
        s = ObjectStorageApi(config["AccountClientNamespace"])
    objects = []
    t = timedelta(days=period)

    today = datetime.today()

    for element in s.object_list(client, container)['objects']:
        meta, stream = s.object_fetch(client, container, element['name'])
        creationDate = datetime.fromtimestamp(
            int(meta['ctime']))
        duration = today - t
        if(creationDate >= duration):
            objects.append(meta)

    print(objects)

ac = AccountClient({"namespace": config["AccountClientNamespace"]})


parser = argparse.ArgumentParser(
    description='Prints a list of files for a given period in the container you desire and for a specific account for a client.')

parser.add_argument('container', type=str, nargs='?',
                    help='The container you want to check the file in')

parser.add_argument('client', type=str, nargs='?',
                    help='The name of the client you want to associate these file')

parser.add_argument('period', type=int, nargs='?',
                    help='The period you want to check the files in')

args = parser.parse_args()

retrieveDataForAGivenPeriod(args.client, args.container, args.period)
