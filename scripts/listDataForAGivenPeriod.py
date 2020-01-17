from oio import ObjectStorageApi
from oio.account.client import AccountClient
from datetime import date, timedelta, datetime


def retrieveDataForAGivenPeriod(client, container, period):
    s = ObjectStorageApi("OPENIO")
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
