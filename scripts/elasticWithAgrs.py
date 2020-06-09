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
        os.system("pip3 install --user requests")
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
try:
    import yaml
except ImportError:
    input("Cannot load module yaml. Press enter to install the package yaml or Ctrl+c to quit the program")
    os.system("pip3 install --user pyyaml")
    import yaml

#script permettant de mettre l'ensemble des fichiers d'un dossier sur le cluster

with open("./config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile,  Loader=yaml.FullLoader)

def test_connection(DOMAIN, PORT, client):
    try:
        # use the JSON library's dump() method for indentation
        info = client.info()
        # pass client object to info() method
        print ("Elasticsearch client info():", info)
    except ConnectionError as err:
        # print ConnectionError for Elasticsearch
        print ("\nElasticsearch info() ERROR:", err)
        print ("\nThe client host:", config['elasticsearchDomain'], "is invalid or cluster is not running")
        # change the client's value to 'None' if ConnectionError
        client = None


#retrieve documents
def extract_save_file(client, container, index):
    response = client.search(index=index, body={}, size=100)
    # total num of Elasticsearch documents to get with API call
    elastic_docs = response["hits"]["hits"]
    for num, doc in enumerate(elastic_docs):
        # get _source data dict from document
        source_data = doc["_source"]

        # s.object_create(config['client'], container, obj_name=source_data["file_name"], data=source_data["data"])


