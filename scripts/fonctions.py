#script containing the different functions with OpenIO

#import of natives modules and script containing ElasticSearch
import os
from datetime import timedelta, datetime
import pytz


# import elasticWithAgrs

#import of OpenIO, ElasticSearch and other modules with import test
try:
    import eventlet
except ImportError:
    input("Cannot load module eventlet. Press enter to install the package eventlet or Ctrl+c to quit the program")
    os.system("pip3 install --user eventlet")
    import eventlet

#try:
#    import urllib3
#except ImportError:
#        input("Cannot load module urllib3. Press enter to install the package urllib3 or Ctrl+c to quit the program")
#        os.system(" pip3 install --user urllib3")
#        import urllib3

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

try:
    import boto3
except ImportError:
    input("Cannot load module ObjectStorageApi from oio. Press enter to install the package oio or Ctrl+c to quit the program")
    os.system("pip3 install --user boto3")
    import boto3

#read variables from configuration file
with open("./config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile,  Loader=yaml.FullLoader)

session = boto3.Session()
s3_client = session.client(service_name='s3', aws_access_key_id=config['awsAccessKeyId'], aws_secret_access_key =config['awsSecretKey'] , endpoint_url=config["awsEndpointUrl"])

#function to add a file in the container
def addFileInContainer(container, path, retention=0):
    """Function called to add a file (thanks to the path parameter) in a defined container"""
    fileName = os.path.basename(path)

    #try/except
    s3_client.upload_file(Filename= path, Bucket=container, Key= fileName)
    if retention !=0 :
    	s3_client.put_object_retention(Bucket=container, Key= fileName, 
    	Retention={
        	'Mode': 'GOVERNANCE',
       		'RetainUntilDate': datetime.today()+timedelta(retention)
    	}
)

def test_connection( client):
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

#function to delete a file in the container
def deleteFileInContainer(container, fileName):
    """Function called to delete a certain file (thanks to its name) in a defined container"""
    s3_client.delete_object(Bucket=container, Key= fileName)

#function to copy an entire folder from sever to the OpenIO container
def uploadFolder( container, folder_path, retention=0):
    """Function called to upload an entire folder (thanks to its path) from your computer to a defined container"""
    for file_name_ext in os.listdir(folder_path):
        file_path_ext=str(folder_path)+'/'+file_name_ext
        s3_client.upload_file(Filename= file_path_ext, Bucket= container, Key=file_name_ext)
        if retention !=0 :
                s3_client.put_object_retention(Bucket=container, Key=file_name_ext, 
    		Retention={
        		'Mode': 'GOVERNANCE',
       			'RetainUntilDate': datetime.today()+timedelta(retention)
    		}
	)

#function to list all data inside a container
def listDataForAGivenPeriod( container, period):
    """Function called to list all data that a container has for a given period of time in days"""
    objects = []
    t = timedelta(days=period)
    utc=pytz.UTC
    today = utc.localize(datetime.today())
    for element in s3_client.list_objects(Bucket=container)['Contents']:
        creationDate = element['LastModified'].replace(tzinfo=utc)
        duration = today - t
        if(creationDate >= duration):
            objects.append(element)

    print(objects)

#function to retrieve all data from a container
def retrieveAllDataFromContainer(container):
    """Function called to retrieve and copy in the folder of the python executable all the files contained in a
    certain container """
    for element in s3_client.list_objects(Bucket=container)['Contents']:
        s3_client.download_file(Bucket=container, Key=element['Key'], Filename= element['Key'])

#function to copy an entire folder from ElasticSearch to the OpenIO container
def elasticUploadFolder(container, index, retention=0):
    """Function called to copy an entire folder  """
    if os.name == 'posix':
        slash = "/" # for Linux and macOS
    else:
        slash = chr(92) # '\' for Windows
    host = str(config['elasticsearchDomain']) + ":" + str(config['elasticsearchPort'])
    client = Elasticsearch(host)
    test_connection(client)
    response = client.search(index=index, body={}, size=100)
    elastic_docs = response["hits"]["hits"]
    for num, doc in enumerate(elastic_docs):
        # get _source data dict from document
        source_data = doc["_source"]
        s3_client.upload_file(Filename= source_data[config['elasticsearchFilenameAttribut']],Bucket=container, Key= source_data[config['elasticsearchFilenameAttribut']])
        if retention !=0 :
                s3_client.put_object_retention(Bucket=container, Key= source_data[config['elasticsearchFilenameAttribut']], 
    		Retention={
        		'Mode': 'GOVERNANCE',
       			'RetainUntilDate': datetime.today()+timedelta(retention)
    		}
	)

#function to create a container
def addContainer(container, newACL='private'):
    s3_client.create_bucket(ACL=newACL, Bucket=container)


#function to get the Acess Control List policy of a container
def getBucketACL(container):
    bucket_acl = s3_client.get_bucket_acl(Bucket=container)
    print(bucket_acl)

#function to modify the Acess Control List policy of a container
def putBucketACL(container,newACL):
    bucket_acl = s3_client.put_bucket_acl(ACL=newACL, Bucket=container)

#function to get the Acess Control List policy of a file
def getObjectACL(container,filename):
    bucket_acl = s3_client.get_object_acl(Bucket=container, Key= filename)
    print(bucket_acl)

#function to modify the Acess Control List policy of a file
def putObjectACL(container,filename, newACL):
    bucket_acl = s3_client.put_object_acl(ACL=newACL, Bucket=container, Key= filename)

#function to get the retention policy of an object
def getRetention(container, filename):
    bucket_retention = s3_client.get_object_retention(Bucket=container, Key= filename)
    print(bucket_retention)

#function to modify the retention policy of an object
def putRetention(container, filename, retention):
    bucket_retention = s3_client.put_object_retention(Bucket=container, Key= filename,
    Retention={
        'Mode': 'GOVERNANCE',
        'RetainUntilDate': datetime.today()+timedelta(retention)
    }

)

