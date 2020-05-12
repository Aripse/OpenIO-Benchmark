#script containing the different functions with OpenIO

#import of natives modules and script containing ElasticSearch
import os
from datetime import date, timedelta, datetime
import elasticWithAgrs

#import of OpenIO, ElasticSearch and other modules with import test
try:
    import eventlet
except ImportError:
    input("Cannot load module eventlet. Press enter to install the package eventlet or Ctrl+c to quit the program")
    os.system("pip3 install --user eventlet")
    import eventlet

try:
    import urllib3
except ImportError:
        input("Cannot load module urllib3. Press enter to install the package urllib3 or Ctrl+c to quit the program")
        os.system(" pip3 install --user urllib3")
        import urllib3

try:
    import yaml
except ImportError:
        input("Cannot load module yaml. Press enter to install the package yaml or Ctrl+c to quit the program")
        os.system("pip3 install --user pyyaml")
        import yaml

try:
    from oio import ObjectStorageApi
except ImportError:
        input("Cannot load module ObjectStorageApi from oio. Press enter to install the package oio or Ctrl+c to quit the program")
        os.system("pip3 install --user git+https://github.com/open-io/oio-sds.git@6.1.0.0a0")
        from oio import ObjectStorageApi

try:
    from elasticsearch import Elasticsearch, helpers
except ImportError:
    input("Cannot load module Elasticsearch. Press enter to install the package Elasticsearch or Ctrl+c to quit the program")
    os.system("pip3 install --user Elasticsearch")
    from elasticsearch import Elasticsearch, helpers

from oio.account.client import AccountClient

#read variables from configuration file
with open("./config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile,  Loader=yaml.FullLoader)

#fonction to add a file in the container
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

#fonction to delete a file in the container
def deleteFileInContainer(client, container, fileName):
    if config['endpoint'] != "":
        s = ObjectStorageApi(config["AccountClientNamespace"], endpoint=config['endpoint'])
    else:
        s = ObjectStorageApi(config["AccountClientNamespace"])
    s.object_delete(client, container, fileName)

#fonction to copy an entire folder from sever to the OpenIO container
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

#fonction to list all data inside a container
def listDataForAGivenPeriod(client, container, period):
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

#fonction to retrieve all data from a container
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

#fonction to copy an entire folder from ElasticSearch to the OpenIO container
def elasticUploadFolder(container, index):
    if os.name == 'posix':
        slash = "/" # for Linux and macOS
    else:
        slash = chr(92) # '\' for Windows
    host = str(config['elasticsearchDomain']) + ":" + str(config['elasticsearchPort'])
    client = Elasticsearch(host)
    elasticWithAgrs.test_connection(config['elasticsearchDomain'], config['elasticsearchPort'], client)
    elasticWithAgrs.extract_save_file(client, container, index)

#fonction to create a container
def addContainer(container):
    if config['endpoint'] != "":
        s = ObjectStorageApi(config["AccountClientNamespace"], endpoint=config['endpoint'])
    else:
        s = ObjectStorageApi(config["AccountClientNamespace"])
    s.container_create(config["client"],container)

