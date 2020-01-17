from oio import ObjectStorageApi
from oio.account.client import AccountClient


def deleteFileInContainer(client, container, fileName):
    s = ObjectStorageApi("OPENIO")
    s.object_delete(client, container, filename)


parser = argparse.ArgumentParser(
    description='Delete a file in the container you desire and for a specific account for a client.')

parser.add_argument('client', type=str, nargs='?',
                    help='The name of the client you want to associate this file')

parser.add_argument('container', type=str, nargs='?',
                    help='The container you want to put the file in')

parser.add_argument('fileName', type=str, nargs='?',
                    help='The name of the file you want to put inside the cluster')

args = parser.parse_args()

addFileInContainer(args.client, args.container, args.fileName)
