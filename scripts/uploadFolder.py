#script permettant de mettre l'ensemble des fichiers d'un dossier sur le cluster

from urllib.parse import unquote
from oio import ObjectStorageApi
from oio.account.client import AccountClient
import os

s = ObjectStorageApi("OPENIO")
ac = AccountClient({"namespace": "OPENIO"})

#chemin du dossier
folder_path='./To_save'

#lister tous les fichier

for file_name_ext in os.listdir(folder_path):
    file_path_ext=folder_path+'/'+file_name_ext
    file_name, file_extension = os.path.splitext(file_name_ext)
    with open(file_path_ext, 'rb') as f:
    	data = f.read()

    	s.object_create("my_ac1", "node1", obj_name=file_name_ext, data=data)
    	meta, stream = s.object_fetch("my_ac1", "node1", file_name_ext)

    with open('./newfile'+file_extension, 'w+b') as e:
        e.write(b"".join(stream))
