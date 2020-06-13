#script containing the different functions with OpenIO

#import of natives modules and script containing ElasticSearch
import os
from datetime import timedelta, datetime
import pytz


#import elasticWithAgrs

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


#function to delete a file in the container
def deleteFileInContainer(container, fileName):
    s3_client.delete_object(Bucket=container, Key= fileName)

#function to copy an entire folder from sever to the OpenIO container
def uploadFolder( container, folder_path, retention=0):
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
    for element in s3_client.list_objects(Bucket=container)['Contents']:
        s3_client.download_file(Bucket=container, Key=element['Key'], Filename= element['Key'])

#function to copy an entire folder from ElasticSearch to the OpenIO container
def elasticUploadFolder(container, index, retention=0):
    if os.name == 'posix':
        slash = "/" # for Linux and macOS
    else:
        slash = chr(92) # '\' for Windows
    host = str(config['elasticsearchDomain']) + ":" + str(config['elasticsearchPort'])
    client = Elasticsearch(host)
    # elasticWithAgrs.test_connection(config['elasticsearchDomain'], config['elasticsearchPort'], client)
    response = client.search(index=index, body={}, size=100)
    elastic_docs = response["hits"]["hits"]
    for num, doc in enumerate(elastic_docs):
        # get _source data dict from document
        source_data = doc["_source"]
        s3_client.upload_file(Filename= source_data["file_name"],Bucket=container, Key= source_data["file_name"])
        if retention !=0 :
                s3_client.put_object_retention(Bucket=container, Key= source_data["file_name"], 
    		Retention={
        		'Mode': 'GOVERNANCE',
       			'RetainUntilDate': datetime.today()+timedelta(retention)
    		}
	)

#function to create a container
def addContainer(container, newACL='private'):
    if newACL=='private' or newACL=='public-read' or newACL=='public-read-write' or newACL=='authenticated-read':
          s3_client.create_bucket(ACL=newACL, Bucket=container)
    else:
          print("ACL argument is not valid. It must be 'private'|'public-read'|'public-read-write'|'authenticated-read' for a container.")


#function to get the Acess Control List policy of a container
def getBucketACL(container):
    bucket_acl = s3_client.get_bucket_acl(Bucket=container)
    print(bucket_acl)

#function to modify the Acess Control List policy of a container
def putBucketACL(container,newACL):
    if newACL=='private' or newACL=='public-read' or newACL=='public-read-write' or newACL=='authenticated-read':
          bucket_acl = s3_client.put_bucket_acl(ACL=newACL, Bucket=container)
    else:
          print("ACL argument is not valid. It must be 'private'|'public-read'|'public-read-write'|'authenticated-read' for a container.")


#function to get the Acess Control List policy of a file
def getObjectACL(container,filename):
    object_acl = s3_client.get_object_acl(Bucket=container, Key= filename)
    print(object_acl)

#function to modify the Acess Control List policy of a file
def putObjectACL(container,filename, newACL):
    if newACL=='private' or newACL=='public-read' or newACL=='public-read-write' or newACL=='authenticated-read' or newACL=='bucket-owner-read' or newACL=='bucket-owner-full-control':
          object_acl = s3_client.put_object_acl(ACL=newACL, Bucket=container, Key= filename)
    else:
          print("ACL argument is not valid. It must be 'private'|'public-read'|'public-read-write'|'authenticated-read'|'aws-exec-read'|'bucket-owner-read'|'bucket-owner-full-control' for an object.")

#function to get the retention policy of an object
def getRetention(container, filename):
    object_retention = s3_client.get_object_retention(Bucket=container, Key= filename)
    print(object_retention)

#function to modify the retention policy of an object
def putRetention(container, filename, retention):
    object_retention = s3_client.put_object_retention(Bucket=container, Key= filename,
    Retention={
        'Mode': 'GOVERNANCE',
        'RetainUntilDate': datetime.today()+timedelta(retention)
    }

)

