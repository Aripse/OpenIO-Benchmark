from oio import ObjectStorageApi
from oio.account.client import AccountClient
import argparse
import os
from addFileInContainer.py import addFileInContainer

parser = argparse.ArgumentParser(description='call the function you want : add to add a file in the container, delete to delete a file in the container, copy to copy an entire folder in the container, list to list all data inside a container, retrieve to retrieve all data from a container')

parser.add_argument('method',type=str, nargs='?')

parser.add_argument('container', type=str, nargs='?',
                    help='The container you want to put the file in')

parser.add_argument('path', type=str, nargs='?',
                    help='The path of the file you want to put inside the cluster')

args=parser.parse_args()

if(args.method == "add"){

    addFileInContainer()
}

