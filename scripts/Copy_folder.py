# from oio import ObjectStorageApi
# from oio.account.client import AccountClient
#
#
# s = ObjectStorageApi("OPENIO")
# ac = AccountClient({"namespace": "OPENIO"})
#
# with open('./Move/Halloween.mp3', 'rb') as f:
#
#     s.object_create("my_ac1", "node1", obj_name="Halloween.mp3", data=f)
#     meta, stream = s.object_fetch("my_ac1", "node1", "Halloween.mp3")
#
#     with open('./newfile.mp3', 'w+b') as e:
#         e.write(b"".join(stream))

import boto3

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)
