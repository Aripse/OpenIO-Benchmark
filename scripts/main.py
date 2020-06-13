#main script: launch the different functions with OpenIO

#import of natives modules and script containing functions
import yaml
import fonctions 
import os
import elasticWithAgrs

os.system("")

#import of OpenIO and other modules with error management
try:
    import argparse
except ImportError:
        input("Cannot load module argparse. Press enter to install the package argparse or Ctrl+c to quit the program")
        os.system("pip3 install --user argparse")
        import argparse
try:
    from oio import ObjectStorageApi
except ImportError:
        input("Cannot load module ObjectStorageApi from oio. Press enter to install the package oio or Ctrl+c to quit the program")
        os.system("pip3 install --user git+https://github.com/open-io/oio-sds.git@6.1.0.0a0")
        from oio import ObjectStorageApi
from oio.account.client import AccountClient

#read variables from configuration file
with open("./config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile,  Loader=yaml.FullLoader)

#configuring command line arguments
parser = argparse.ArgumentParser(description='call the function you want : add to add a file in the container, delete to delete a file in the container, copy to copy an entire folder in the container, list to list all data inside a container, retrieve to retrieve all data from a container')

#name of the function to call (add, delete, copy, list, retrieve, elastic, create_container) 
parser.add_argument('method',type=str, nargs='?')

#name of the container
parser.add_argument('--container', type=str, nargs='?',
                    help='The container you want to put the file in')
#path of the file
parser.add_argument('--path', type=str, nargs='?',
                    help='The path of the file you want to put inside the cluster')

#time period (in days since today)
parser.add_argument('--period', type=int, nargs='?', 
			help='The period of the retrieved data')
#name of the fle
parser.add_argument('--filename', type=str, nargs='?',
            help='The name od the file you want to delete from the container')

#name of the subscriber index from ElasticSearch 
parser.add_argument("--index", type=str, nargs='?', help="give specific index")

#The Access Control List you want to put on a container/object.
parser.add_argument("--ACL", type=str, nargs='?',
help="The Access Control List you want to put on a container/object. It must be 'private'|'public-read'|'public-read-write'|'authenticated-read' for a container. It must be 'private'|'public-read'|'public-read-write'|'authenticated-read'|'bucket-owner-read'|'bucket-owner-full-control' for an object.")

#The number of days from today until this Object Lock Retention will expire
parser.add_argument("--retention", type=int, nargs='?',
help="The number of days from today until this Object Lock Retention will expire.")

args=parser.parse_args()

#verification of the presence of the argument "container" and the configuration variable "AccountClientNamespace" then launching of the function according to the argument "method"
if not args.container:
	print("You must have a container parameter for the function to work smoothly.")
elif not config['AccountClientNamespace']:
	print("The AccountClientNamespace attribute does not exist in the configuration file. Please add it.")
else:
	if(args.method == "add"):
		if not args.path:
			print("The function AddFileInContainer needs a path argument to work. Please try again.")
		else:
			print("Running the function AddFileInContainer with the parameters below :")
			print(" - container : "+ args.container)
			print(" - path : "+ args.path)
			if args.retention:
				print(" - retention :"+ str(args.retention))
			print(" - namespace : "+ config['AccountClientNamespace'])
			input("Press Enter to continue...")
			if args.retention:
				fonctions.addFileInContainer(args.container, args.path, args.retention)
			else:
				fonctions.addFileInContainer(args.container, args.path)

	elif(args.method == "delete"): #delete a file in the container
		if not args.filename:
			print("The function DeleteFileInContainer needs a filename argument to work. Please try again.")
		else:
			print("Running the function DeleteFileInContainer with the parameters below :")
			print(" - container : "+ args.container)
			print(" - client : "+ config['client'])
			print(" - filename : "+ args.filename)
			print(" - namespace : "+ config['AccountClientNamespace'])
			print(" - endpoint : "+ config['awsEndpointUrl'])
			input("Press Enter to continue...")
			fonctions.deleteFileInContainer(args.container, args.filename)

	elif(args.method == "copy"): #copy an entire folder from sever to the OpenIO container
		if not args.path:
			print("The function UploadFolder needs a path argument to work. Please try again.")
		else:
			print("Running the function UploadFolder with the parameters below :")
			print(" - container : "+ args.container)
			print(" - client : "+ config['client'])
			print(" - path : "+ args.path)
			if args.retention:
				print(" - retention :"+ str(args.retention))
			print(" - namespace : "+ config['AccountClientNamespace'])
			print(" - endpoint : "+ config['awsEndpointUrl'])
			input("Press Enter to continue...")
			if args.retention:
				fonctions.uploadFolder(args.container, args.path, args.retention)
			else:
				fonctions.uploadFolder(args.container, args.path)

	elif(args.method == "list"): #list all data inside a container
		if not args.period:
			print("The function ListDataForAGivenPeriod needs a period argument to work. Please try again.")
		else:
			print("Running the function ListDataForAGivenPeriod with the parameters below :")
			print(" - container : "+ args.container)
			print(" - client : "+ config['client'])
			print(" - period : "+ str(args.period))
			print(" - namespace : "+ config['AccountClientNamespace'])
			print(" - endpoint : "+ config['awsEndpointUrl'])
			input("Press Enter to continue...")
			fonctions.listDataForAGivenPeriod( args.container, args.period)

	elif(args.method == "retrieve"): #retrieve all data from a container
		print("Running the function RetrieveAllDataFromContainer with the parameters below :")
		print(" - container : "+ args.container)
		print(" - client : "+ config['client'])
		print(" - namespace : "+ config['AccountClientNamespace'])
		print(" - endpoint : "+ config['awsEndpointUrl'])
		input("Press Enter to continue...")
		fonctions.retrieveAllDataFromContainer( args.container)

	elif(args.method == "elastic"): #copy an entire folder from ElasticSearch to the OpenIO container
		print("Running the function elasticUploadFolder with the parameters below :")
		print(" - container : "+ args.container)
		print(" - index : "+ args.index)
		print(" - client : "+ config['client'])
		if args.retention:
				print(" - retention :"+ str(args.retention))
		print(" - namespace : "+ config['AccountClientNamespace'])
		print(" - endpoint : "+ config['awsEndpointUrl'])
		print(" - elasticsearchDomain :" + config["elasticsearchDomain"])
		print(" - elasticsearchPort :" + config["elasticsearchPort"])
		input("Press Enter to continue...")
		if args.retention:
			fonctions.elasticUploadFolder(args.container, args.index, args.retention)
		else:
			fonctions.elasticUploadFolder(args.container, args.index)

	elif(args.method=="create_container"): #create a container
		print("Running the function addContainer with the parameters below :")
		print(" - container : "+ args.container)
		if args.ACL:
				print(" - ACL :"+ args.ACL)
		print(" - client : "+ config['client'])
		print(" - namespace : "+ config['AccountClientNamespace'])
		print(" - endpoint : "+ config['awsEndpointUrl'])
		input("Press Enter to continue...")
		if args.ACL:
			fonctions.addContainer(args.container,args.ACL)
		else:
			fonctions.addContainer(args.container)

	elif(args.method=="get_container_ACL"): #get the Access Control List of a container
		print("Running the function GetBucketACL with the parameters below :")
		print(" - container : "+ args.container)
		print(" - client : "+ config['client'])
		print(" - namespace : "+ config['AccountClientNamespace'])
		print(" - endpoint : "+ config['awsEndpointUrl'])
		input("Press Enter to continue...")
		fonctions.getBucketACL(args.container)

	elif(args.method=="put_container_ACL"): #modify the Access Control List of a container
		print("Running the function PutBucketACL with the parameters below :")
		print(" - container : "+ args.container)
		print(" - ACL : "+ args.ACL)
		print(" - client : "+ config['client'])
		print(" - namespace : "+ config['AccountClientNamespace'])
		print(" - endpoint : "+ config['awsEndpointUrl'])
		input("Press Enter to continue...")
		fonctions.putBucketACL(args.container,args.ACL)

	elif(args.method=="get_file_ACL"): #get the Access Control List of a file
		print("Running the function GetObjectACL with the parameters below :")
		print(" - container : "+ args.container)
		print(" - filename : "+ args.filename)
		print(" - client : "+ config['client'])
		print(" - namespace : "+ config['AccountClientNamespace'])
		print(" - endpoint : "+ config['awsEndpointUrl'])
		input("Press Enter to continue...")
		fonctions.getObjectACL(args.container,args.filename)

	elif(args.method=="put_file_ACL"): #modify the Access Control List of a file
		print("Running the function PutObjectACL with the parameters below :")
		print(" - container : "+ args.container)
		print(" - filename : "+ args.filename)
		print(" - ACL : "+ args.ACL)
		print(" - client : "+ config['client'])
		print(" - namespace : "+ config['AccountClientNamespace'])
		print(" - endpoint : "+ config['awsEndpointUrl'])
		input("Press Enter to continue...")
		fonctions.putObjectACL(args.container,args.filename, args.ACL)

	elif(args.method=="get_retention"): #get the retention policy of an object
		print("Running the function GetRetention with the parameters below :")
		print(" - container : "+ args.container)
		print(" - client : "+ config['client'])
		print(" - filename : "+ args.filename)
		print(" - namespace : "+ config['AccountClientNamespace'])
		print(" - endpoint : "+ config['awsEndpointUrl'])
		input("Press Enter to continue...")
		fonctions.getRetention(args.container,args.filename)

	elif(args.method=="put_retention"): #modify the retention policy of an object
		print("Running the function GetRetention with the parameters below :")
		print(" - container : "+ args.container)
		print(" - client : "+ config['client'])
		print(" - filename : "+ args.filename)
		print(" - retention :"+ str(args.retention))
		print(" - namespace : "+ config['AccountClientNamespace'])
		print(" - endpoint : "+ config['awsEndpointUrl'])
		input("Press Enter to continue...")
		fonctions.putRetention(args.container,args.filename,args.retention)


	elif(args.method.length == 0): #error handling: no method argument
		print("An argument method must be thrown.")

	else: #display of the "help" menu
		print("Invalid argument" + args.method+ "for method. Please try with one of the below possibilities :")
		print("- add : to add a specific file in a container")
		print("- delete : to delete a specific file inside a container")
		print("- copy : to copy an entire folder inside a container")
		print("- list : to list every items inside a container for a given period")
		print("- retrieve : to get every file from a container outside the container")
		print("- elastic : to put every file from an elastic index inside the container")
		print("- create_container : to create an empty container")
		print("- get_container_ACL : to get the Access Control List of a container")
		print("- put_container_ACL : to modify the Access Control List of a container")
		print("- get_file_ACL : to get the Access Control List of a file")
		print("- put_file_ACL : to modify the Access Control List of a file")
		print("- get_retention : to get the retention policy of an object")
		print("- put_retention : to modify the retention policy of an object")
