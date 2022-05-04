import datetime

from fdpclient.fdpclient import FDPClient
import fdpclient
from importlib import reload
reload(fdpclient.fdpclient)
import logging
import requests
from requests.auth import HTTPBasicAuth
import rdflib
from pprint import pprint
import datetime


#my_headers = {'Accept' : 'application/json','Content-Type':'application/json'}
client=FDPClient("http://localhost:8080","albert.einstein@example.com","password",publicurl="http://localhost:8080")
client.headers
client.catalog_template

pprint(client.read().serialize(format="turtle"))
pprint(client.read(type="meta").serialize(format="turtle"))

newcat=client.createCatalogRDF(DESCRIPTION="test",title="Test02",version="1.0.0",ispartof=client.publicurl,publisher="ICH")
id=client.create(type='catalog',data=newcat)

newdat=client.createDatasetRDF(title="COVAC-DM Study",
                               version="1.0.0",
                               catalogid=id,
                               publisher="Projektmanagementteam",
                               ISSUED=datetime.datetime.now(),
                               MODIFIED=datetime.datetime.now(),
                               LANGUAGE='http://id.loc.gov/vocabulary/iso639-1/en',
                               KEYWORDS=["diabetes mellitus type 1","diabetes mellitus type 2","COVID-19"],
                               DESCRIPTION="<https://biobank.medunigraz.at/.../biobank/pdf/Kohorten/5006_21_COVAC-DM_Study.pdf>",
                               CONTACTPOINT = "patrick.nitsche@medunigraz.at",
                               themes_list=["http://www.w3.org/ns/dcat#theme","http://identifiers.org/icd/Q87.8"])
dat_id=client.create(type='dataset',data=newdat)

newdis=client.createDistributionRDF(title="Distribution",
                               version="1.0.0",
                               datasetid=dat_id,
                               publisher="Projektmanagementteam",
                               ISSUED=datetime.datetime.now(),
                               MODIFIED=datetime.datetime.now(),
                               LANGUAGE='http://id.loc.gov/vocabulary/iso639-1/en',
                               mediatype="WSI",
                               FORMAT="SVS",
                               BYTESIZE="10737418240",
                               ACCESSURL="https://youtu.be/dQw4w9WgXcQ",
                               DOWNLOADURL="http://download.url")
dis_id=client.create(type='distribution',data=newdis)

# create metadata
with open('test-data/test_cat02.ttl') as f:
    data = f.read()

id=client.create(type='catalog',data=data)
cat_meta=client.read(type='catalog',id=id)
for r in cat_meta.triples((None, None, None)):
    print(r)

#(rdflib.term.URIRef('http://localhost/catalog/4f6f1e29-a76b-4d7d-9441-f28dcabb3475'), rdflib.term.URIRef('http://purl.org/dc/terms/hasVersion'), rdflib.term.Literal('1'))

qres = cat_meta.query("SELECT ?s ?o WHERE { ?s dcterms:hasVersion ?o }")
for row in qres:
    print(f"{row.s} dcterms:hasVersion {row.o}")

cat_meta.update("""
         DELETE { ?s dcterms:hasVersion '1' }
         INSERT { ?s dcterms:hasVersion '2' }
         WHERE { ?s dcterms:hasVersion '1' }
         """)

qres = cat_meta.query("SELECT ?s ?o WHERE { ?s dcterms:hasVersion ?o }")
for row in qres:
    print(f"{row.s} dcterms:hasVersion {row.o}")

cat_meta.update("""
             INSERT DATA { <http://localhost/catalog/4f6f1e29-a76b-4d7d-9441-f28dcabb3475> dcterms:hasVersion <2> }
             """)
cat_meta.update("""
         DELETE { ?s dcterms:hasVersion <2> }
         WHERE { ?s dcterms:hasVersion <2> }
         """)



client.update(type='catalog', id=id, data=cat_meta.serialize(format="turtle"))
client.delete(type='catalog',id=id)

id='b01c85a9-aad5-45e7-9ec7-d6a59437de37'

client.delete(type='catalog',id='815e5aae-44e9-4f16-a76c-f395b6e82ab5')

#test_data={"email": "albert.einstein@example.com", "password": "password"}

#requests.post("http://localhost:8080/tokens", data='{ "email": "albert.einstein@example.com", "password": "password" }',headers=my_headers)
#r=requests.post("http://localhost:8080/tokens", data=json.dumps(test_data),headers=my_headers)
#r.json()['token']
#requests.post("http://localhost:8080/tokens", auth=HTTPBasicAuth('albert.einstein@example.com', 'password'),headers=my_headers).content



# http://localhost:8088/catalog/d3a7cf95-fef9-44a0-be0b-6cd0e6385712/create-dataset


g = rdflib.Graph()
g.parse(
    data="""
        <x:> a <c:> .
        <y:> a <c:> .
    """,
    format="turtle"
)

# Select all the things (s) that are of type (rdf:type) c:
qres = g.query("""SELECT ?s WHERE { ?s a <c:> }""")

for row in qres:
    print(f"{row.s}")

g.update("""INSERT DATA { <z:> a <c:> }""")

g.update("""
         DELETE { <y:> a <c:> }
         INSERT { <y:> a <d:> }
         WHERE { <y:> a <c:> }
         """)
print("After second update:")
qres = g.query("""SELECT ?s ?o WHERE { ?s a ?o }""")
for row in qres:
    print(f"{row.s} a {row.o}")