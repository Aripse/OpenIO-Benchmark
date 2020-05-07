
import yaml
import fonctions
import os
import elasticWithAgrs

os.system("")

try:
    import argparse
except ImportError:
        input("Cannot load module argparse. Press enter to install the package argparse or Ctrl+c to quit the program")
        os.system("pip3 install --user argparse")
        import argparse

with open("./config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile,  Loader=yaml.FullLoader)

parser = argparse.ArgumentParser(description='call the function you want : add to add a file in the container, delete to delete a file in the container, copy to copy an entire folder in the container, list to list all data inside a container, retrieve to retrieve all data from a container')

parser.add_argument('method',type=str, nargs='?')

parser.add_argument('--container', type=str, nargs='?',
                    help='The container you want to put the file in')

parser.add_argument('--path', type=str, nargs='?',
                    help='The path of the file you want to put inside the cluster')

parser.add_argument('--period', type=int, nargs='?', 
			help='The period of the retrieved data')

parser.add_argument('--filename', type=str, nargs='?',
            help='The name od the file you want to delete from the container')

parser.add_argument("--index", type=str, nargs='?', help="give specific index")

args=parser.parse_args()

if not args.container:
	print("You must have a container parameter for the function to work smoothly.")
elif not config['AccountClientNamespace']:
	print("The AccountClientNamespace attribute does not exist in the configuration file. Please add it.")
else:
	if(args.method == "add"):
		if not args.path:
			print("The function AddFileInContainer needs a path argument to work. Please try again.")
		else:
			print(" ", end="")
			print("Running the function AddFileInContainer with the parameters below :")
			print(" - container : "+ args.container)
			print(" - client : "+ config['client'])
			print(" - path : "+ args.path)
			print(" - namespace : "+ config['AccountClientNamespace'])
			print(" - endpoint : "+ config['endpoint'])
			input("Press Enter to continue...")
			fonctions.addFileInContainer(args.container, args.path, config['client'])

	elif(args.method == "delete"):
		if not args.filename:
			print("The function DeleteFileInContainer needs a filename argument to work. Please try again.")
		else:
			print("Running the function DeleteFileInContainer with the parameters below :")
			print(" - container : "+ args.container)
			print(" - client : "+ config['client'])
			print(" - filename : "+ args.filename)
			print(" - namespace : "+ config['AccountClientNamespace'])
			print(" - endpoint : "+ config['endpoint'])
			input("Press Enter to continue...")
			fonctions.deleteFileInContainer(config['client'], args.container, args.filename)

	elif(args.method == "copy"):
		if not args.path:
			print("The function UploadFolder needs a path argument to work. Please try again.")
		else:
			print("Running the function UploadFolder with the parameters below :")
			print(" - container : "+ args.container)
			print(" - client : "+ config['client'])
			print(" - path : "+ args.path)
			print(" - namespace : "+ config['AccountClientNamespace'])
			print(" - endpoint : "+ config['endpoint'])
			input("Press Enter to continue...")
			fonctions.uploadFolder(config['client'], args.container, args.path)

	elif(args.method == "list"):
		if not args.period:
			print("The function ListDataForAGivenPeriod needs a period argument to work. Please try again.")
		else:
			print("Running the function ListDataForAGivenPeriod with the parameters below :")
			print(" - container : "+ args.container)
			print(" - client : "+ config['client'])
			print(" - period : "+ str(args.period))
			print(" - namespace : "+ config['AccountClientNamespace'])
			print(" - endpoint : "+ config['endpoint'])
			input("Press Enter to continue...")
			fonctions.listDataForAGivenPeriod(config['client'], args.container, args.period)

	elif(args.method == "retrieve"):
		print("Running the function RetrieveAllDataFromContainer with the parameters below :")
		print(" - container : "+ args.container)
		print(" - client : "+ config['client'])
		print(" - namespace : "+ config['AccountClientNamespace'])
		print(" - endpoint : "+ config['endpoint'])
		input("Press Enter to continue...")
		fonctions.retrieveAllDataFromContainer(config['client'], args.container)

	elif(args.method == "elastic"):
		print("Running the function RetrieveAllDataFromContainer with the parameters below :")
		print(" - container : "+ args.container)
		print(" - client : "+ config['client'])
		print(" - namespace : "+ config['AccountClientNamespace'])
		print(" - endpoint : "+ config['endpoint'])
		print(" - elasticsearchDomain :" + config["elasticsearchDomain"])
		print(" - elasticsearchPort :" + config["elasticsearchPort"])
		input("Press Enter to continue...")
		fonctions.elasticUploadFolder(args.container, args.index)

	elif(args.method.length == 0):
		print("An argument method must be thrown.")

	else:
		print("Invalid argument" + args.method+ "for method. Please try with one of the below possibilities :")
		print("- add : to add a specific file in a container")
		print("- delete : to delete a specific file inside a container")
		print("- copy : to copy an entire folder inside a container")
		print("- list : to list every items inside a container for a given period")
		print("- retrieve : to get every file from a container outside the container")