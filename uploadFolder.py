#script permettant de mettre l'ensemble des fichiers d'un dossier sur le cluster

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
    from urllib.parse import unquote
except ImportError:
        input("Cannot load module unquote from urlib.parse. Press enter to install the package oio or Ctrl+c to quit the program")
        os.system("pip3 install urllib3")
        from urllib.parse import unquote

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

def uploadFolder(client, container, folder_path):
    if config['endpoint'] != "":
        s = ObjectStorageApi(config["AccountClientNamespace"], endpoint=config['endpoint'])
    else:
        s = ObjectStorageApi(config["AccountClientNamespace"])
    for file_name_ext in os.listdir(folder_path):
        file_path_ext=str(folder_path)+'/'+file_name_ext
        file_name, file_extension = os.path.splitext(file_name_ext)
        with open(file_path_ext, 'rb') as f:
            data = f.read()
            s.object_create(client, container, obj_name=file_name_ext, data=data)
            meta, stream = s.object_fetch(client, container, file_name_ext)
        with open('./'+file_name+file_extension, 'w+b') as e:
            e.write(b"".join(stream))


ac = AccountClient({"namespace": config["AccountClientNamespace"]})

parser = argparse.ArgumentParser(
    description='Upload all files of a folder in the container you desire and for a specific account for a client.')

parser.add_argument('container', type=str, nargs='?',
                    help='The container you want to put the file in')

parser.add_argument('client', type=str, nargs='?',
                    help='The name of the client you want to associate this file')

parser.add_argument('path', type=str, nargs='?',
                    help='The path of the file you want to put inside the cluster')

args = parser.parse_args()

uploadFolder(args.client, args.container, args.path)
