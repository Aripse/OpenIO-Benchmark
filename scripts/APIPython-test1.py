# create an OBjectStoreAPI object
from oio import ObjectStorageApi
s = ObjectStorageApi("OPENIO", endpoint="http://169.254.205.203:6006")

#creer un compte
from oio.account.client import AccountClient
ac = AccountClient({"namespace": "OPENIO"}, proxy_endpoint="http://169.254.205.203:6006")

# Account creation: Returns true if everything went well.
ac.account_create("admin") 

#create a container
s.container_create(ac, "node1")

#shows the description  of a container
s.container_get_properties(ac,"node1")

#create ano object .text
#data = "My data"
#s.object_create("admin", "node1", obj_name="essai.txt",data=data)

#retrieving object
#meta, stream = s.object_fetch("admin","node1", "essai.txt")
#print (b" ".join(stream))

#deleting objects
#s.object_delete("admin", "node1", "essai.txt")
