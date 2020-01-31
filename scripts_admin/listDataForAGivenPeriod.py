from oio import ObjectStorageApi
from oio.account.client import AccountClient
from datetime import date, timedelta, datetime
import argparse
import os


def retrieveDataForAGivenPeriod(container, period):
    s = ObjectStorageApi("OPENIO")
    client="admin"
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

ac = AccountClient({"namespace": "OPENIO"})


parser = argparse.ArgumentParser(
    description='Prints a list of files for a given period in the container you desire and for a specific account for a client.')

parser.add_argument('container', type=str, nargs='?',
                    help='The container you want to check the file in')

parser.add_argument('period', type=int, nargs='?',
                    help='The period you want to check the files in')

args = parser.parse_args()

retrieveDataForAGivenPeriod(args.container, args.period)
