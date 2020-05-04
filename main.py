from oio import ObjectStorageApi
from oio.account.client import AccountClient
import argparse
import os

import fonctions

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

parser = argparse.ArgumentParser(description='call the function you want : add to add a file in the container, delete to delete a file in the container, copy to copy an entire folder in the container, list to list all data inside a container, retrieve to retrieve all data from a container')

parser.add_argument('method',type=str, nargs='?')

parser.add_argument('container', type=str, nargs='?',
                    help='The container you want to put the file in')

parser.add_argument('client', type=str, nargs='?',
                    help='The client you for whom you want to add the file')

parser.add_argument('path', type=str, nargs='?',
                    help='The path of the file you want to put inside the cluster')

args=parser.parse_args()

if(args.method == "add"):
   print("add")
   fonctions.addFileInContainer(args.container, args.path, args.client)

elif(args.method == "delete"):
   print("delete")
   fonctions.deleteFileInContainer(args.client, args.container, args.path)

elif(args.method == "copy"):
   print("copy")
   fonctions.uploadFolder(args.client, args.container, args.path)

elif(args.method == "list"):
   print("list")
   fonctions.retrieveDataForAGivenPeriod(args.client, args.container, args.period)

else:
   print("retrieve")
   fonctions.retrieveAllDataFromContainer(args.client, args.container)

