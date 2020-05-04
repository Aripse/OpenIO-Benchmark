

import fonctions

try:
    import argparse
except ImportError:
        input("Cannot load module argparse. Press enter to install the package argparse or Ctrl+c to quit the program")
        os.system("pip3 install --user argparse")
        import argparse

parser = argparse.ArgumentParser(description='call the function you want : add to add a file in the container, delete to delete a file in the container, copy to copy an entire folder in the container, list to list all data inside a container, retrieve to retrieve all data from a container')

parser.add_argument('method',type=str, nargs='?')

parser.add_argument('--container', type=str, nargs='?',
                    help='The container you want to put the file in')

parser.add_argument('--client', type=str, nargs='?',
                    help='The client you for whom you want to add the file')

parser.add_argument('--path', type=str, nargs='?',
                    help='The path of the file you want to put inside the cluster')

parser.add_argument('--period', type=int, nargs='?', 
			help='The period of the retrieved data')

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

