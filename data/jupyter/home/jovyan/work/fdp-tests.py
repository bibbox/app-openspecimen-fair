from fdpclient.fdpclient import FDPClient
import fdpclient
from importlib import reload
reload(fdpclient.fdpclient)
import logging
import requests
from requests.auth import HTTPBasicAuth


#my_headers = {'Accept' : 'application/json','Content-Type':'application/json'}
client=FDPClient("http://localhost:8080","albert.einstein@example.com","password")
client.headers

# create metadata
with open('test-data/test_cat02.ttl') as f:
    data = f.read()

id=client.create(type='catalog',data=data)
client.read(type='catalog',id=id)
client.delete(type='catalog',id=id)
id='b01c85a9-aad5-45e7-9ec7-d6a59437de37'

client.delete(type='catalog',id='815e5aae-44e9-4f16-a76c-f395b6e82ab5')

#test_data={"email": "albert.einstein@example.com", "password": "password"}

#requests.post("http://localhost:8080/tokens", data='{ "email": "albert.einstein@example.com", "password": "password" }',headers=my_headers)
#r=requests.post("http://localhost:8080/tokens", data=json.dumps(test_data),headers=my_headers)
#r.json()['token']
#requests.post("http://localhost:8080/tokens", auth=HTTPBasicAuth('albert.einstein@example.com', 'password'),headers=my_headers).content
