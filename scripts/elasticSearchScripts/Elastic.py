from datetime import datetime
import os
import json, time
try:
    import os.path
except ImportError:
        input("Cannot load module os.path. Press enter to install the package os.path or Ctrl+c to quit the program")
        os.system("pip3 install --user os.path")
        import os.path

try:
    import numpy as np
except ImportError:
        input("Cannot load module numpy. Press enter to install the package numpy or Ctrl+c to quit the program")
        os.system("pip3 install --user numpy")
        import numpy as np
try:
    import requests
except ImportError:
        input("Cannot load module requests. Press enter to install the package requests or Ctrl+c to quit the program")
        os.system("pip install --user requests")
        import requests
try:
    import glob
except ImportError:
        input("Cannot load module glob. Press enter to install the package glob or Ctrl+c to quit the program")
        os.system("pip3 install --user glob")
        import glob
try:
    import gzip
except ImportError:
        input("Cannot load module gzip. Press enter to install the package gzip or Ctrl+c to quit the program")
        os.system("pip3 install --user gzip")
        import gzip
try:
    from elasticsearch import Elasticsearch, helpers
except ImportError:
        input("Cannot load module Elasticsearch. Press enter to install the package Elasticsearch or Ctrl+c to quit the program")
        os.system("pip3 install --user Elasticsearch")
        from elasticsearch import Elasticsearch, helpers

#script permettant de mettre l'ensemble des fichiers d'un dossier sur le cluster
from urllib.parse import unquote
from oio import ObjectStorageApi
from oio.account.client import AccountClient
import os
import argparse

def uploadFolder(container, folder_path):
    s = ObjectStorageApi("OPENIO", endpoint="http://169.254.205.203:6006")
    client="admin"
    for file_name_ext in os.listdir(folder_path):
        file_path_ext=str(folder_path)+'/'+file_name_ext
        file_name, file_extension = os.path.splitext(file_name_ext)
        with open(file_path_ext, 'rb') as f:
            data = f.read()
            s.object_create(client, container, obj_name=file_name_ext, data=data)
            meta, stream = s.object_fetch(client, container, file_name_ext)

def current_path():
    return os.path.dirname(os.path.realpath( __file__ ))

def test_connection(DOMAIN, PORT, client):
    try:
        # use the JSON library's dump() method for indentation
        info = client.info()
        # pass client object to info() method
        print ("Elasticsearch client info():", info)
    except ConnectionError as err:
        # print ConnectionError for Elasticsearch
        print ("\nElasticsearch info() ERROR:", err)
        print ("\nThe client host:", host, "is invalid or cluster is not running")
        # change the client's value to 'None' if ConnectionError
        client = None

def get_files_in_dir(self=current_path()):
    # declare empty list for files
    file_list = []
    # put a slash in dir name if needed
    if self[-1] != slash:
        self = self + slash
    # iterate the files in dir using glob
    for filename in glob.glob(self + '*.gz'):
        # add each file to the list
        file_list += [filename]
    # return the list of filenames
    return file_list

def get_data_from_file(file):
     # declare an empty list for the data
    data = []
    # get the data line-by-line using os.open()
    for line in open(file, encoding="utf8", errors='ignore'):
        # append each line of data to the list
        data += [ str(line) ]
    # return the list of data
    return data

# define a function that yields an Elasticsearch document from file data
def yield_docs(all_files):
    # iterate over the list of files
    for _id, _file in enumerate(all_files):
        # use 'rfind()' to get last occurence of slash
        file_name = _file[ _file.rfind(slash)+1:]
        # get the file's statistics
        stats = os.stat( _file )
        # timestamps for the file
        create_time = datetime.fromtimestamp( stats.st_birthtime )
        modify_time = datetime.fromtimestamp( stats.st_mtime )
        # get the data inside the file
        data = get_data_from_file( _file )
        # join the list of data into one string using return
        data = "".join( data )
        # create the _source data for the Elasticsearch doc
        doc_source = {
            "file_name": file_name,
            "create_time": create_time,
            "modify_time": modify_time,
            "data": data  #(pour lire le contenu des fichiers).
        }
        # use a yield generator so that the doc data isn't loaded into memory
        yield {
            "_index": "my_files",
            "_type": "some_type",
            "_id": _id + 1, # number _id for each iteration
            "_source": doc_source
        }

#retrieve documents
def extract_save_file(save_path, client):
    response = client.search(index='my_files', body={}, size=100)
    # total num of Elasticsearch documents to get with API call
    elastic_docs = response["hits"]["hits"]
    for num, doc in enumerate(elastic_docs):
        # get _source data dict from document
        source_data = doc["_source"]
        complete_name = os.path.join(save_path, source_data["file_name"])
        file = open(complete_name, "w+")
        try:
            file.write(source_data["data"])
        finally:
            file.close()

if __name__ == "__main__":
    #Initialize variables
    DOMAIN="169.254.205.133"
    PORT=9200
    start_time = time.time()
     # posix uses "/", and Windows uses ""
    if os.name == 'posix':
         slash = "/" # for Linux and macOS
    else:
        slash = chr(92) # '\' for Windows
    host = str(DOMAIN) + ":" + str(PORT)
    client = Elasticsearch(host)
    test_connection(DOMAIN, PORT, client)
   # all_files = get_files_in_dir("/Users/macbookpro/Desktop/ClusterOpenIO/test")
   # try:
   #     # make the bulk call using 'actions' and get a response
   #     resp = helpers.bulk(
   #         client,
   #         yield_docs( all_files )
   #     )
   #     print ("\nhelpers.bulk() RESPONSE:", resp)
   #     print ("RESPONSE TYPE:", type(resp))
   # except Exception as err:
   #     print("\nhelpers.bulk() ERROR:", err)
    extract_save_file("/home/morgane/Bureau/cluster", client)
    # total number of files to index
   # print ("TOTAL FILES:", len( all_files ))
    print ("\n\ntime elapsed:", time.time()-start_time)

    parser = argparse.ArgumentParser(
    description='Upload all files of a folder in the container you desire and for a specific account for a client.')

    parser.add_argument('container', type=str, nargs='?',
                    help='The container you want to put the file in')

    parser.add_argument('path', type=str, nargs='?',
                    help='The path of the file you want to put inside the cluster')

    args = parser.parse_args()

    uploadFolder(args.container, args.path)
