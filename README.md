# openspecimen-fair BIBBOX application

This container can be installed as [BIBBOX APP](https://bibbox.readthedocs.io/en/latest/ "BIBBOX App Store") or standalone. 

After the docker installation follow these [instructions](INSTALL-APP.md).

## Standalone Installation 

Clone the github repository. If necessary change the ports in the environment file `.env` and the volume mounts in `docker-compose.yml`.

```
git clone https://github.com/bibbox/app-openspecimen-fair
cd app-openspecimen-fair
docker network create bibbox-default-network
docker-compose up -d
```

The main App can be opened and set up at:
```
http://localhost:9000
```

## Install within BIBBOX

Visit the BIBBOX page and find the App by its name in the store. Click on the symbol and select install. Then fill the parameters below and name your App, click install again.

## Docker Images used
  - [bibbox/openspecimen](https://hub.docker.com/r/bibbox/openspecimen) 
  - [mysql](https://hub.docker.com/r/mysql) 
  - [jupyter/datascience-notebook](https://hub.docker.com/r/jupyter/datascience-notebook) 
  - [fairdata/fairdatapoint](https://hub.docker.com/r/fairdata/fairdatapoint) 
  - [fairdata/fairdatapoint-client](https://hub.docker.com/r/fairdata/fairdatapoint-client) 
  - [mongo](https://hub.docker.com/r/mongo) 
  - [metaphacts/blazegraph-basic](https://hub.docker.com/r/metaphacts/blazegraph-basic) 
  - [neo4j](https://hub.docker.com/r/neo4j) 


 
## Install Environment Variables
  - MYSQL_DATABASE_USER = The User of the DB created for OpenSpecimen
  - MYSQL_DATABASE_PASSWORD = The Password of the DB User created for OpenSpecimen
  - JUPYTER_TOKEN = 
  - FDP_TITLE = 
  - FDP_DESCRIPTION = 
  - CATALOG_TITLE = 
  - CATALOG_DESCRIPTION = 
  - VERSION = 
  - PUBLISHERNAME = 
  - PUBLISHEREMAIL = 
  - PUBLISHERUID = Unique id of Publisher e.g. ORCID
  - LANGUAGE = Language of Catalog and Dataset in IRI format. e.g. http://id.loc.gov/vocabulary/iso639-1/en

  
The default values for the standalone installation are:
  - MYSQL_DATABASE_USER = user
  - MYSQL_DATABASE_PASSWORD = changethisdatabasepasswordinproductionenvironments
  - JUPYTER_TOKEN = token
  - FDP_TITLE = fdp title
  - FDP_DESCRIPTION = enter description
  - CATALOG_TITLE = catalog title
  - CATALOG_DESCRIPTION = catalog description
  - VERSION = enter version
  - PUBLISHERNAME = publisher name
  - PUBLISHEREMAIL = publisher@mail.com
  - PUBLISHERUID = uid
  - LANGUAGE = language

  
## Mounted Volumes
### bibbox/openspecimen Conatiner
  - *./data/os-data:/var/lib/openspecimen/data*
  - *./data/os-plugins:/var/lib/openspecimen/plugins*
  - *./images/openspecimen/configs/openspecimen/ROOT:/var/lib/tomcat9/webapps/ROOT*
  - *./images/openspecimen/configs/openspecimen/scripts/entrypoint.sh:/opt/scripts/entrypoint.sh*
### mysql Conatiner
  - *./data/mysql:/var/lib/mysql*
  - *./images/openspecimen/configs/openspecimen.cnf:/etc/mysql/conf.d/openspecimen.cnf:ro*
### jupyter/datascience-notebook Conatiner
  - *./data/jupyter/home/jovyan/work:/home/jovyan/work*
### fairdata/fairdatapoint Conatiner
  - *./data/application.yml:/fdp/application.yml:ro*
### mongo Conatiner
  - *./data/mongo/data:/data/db*
### metaphacts/blazegraph-basic Conatiner
  - *./data/blazegraph:/blazegraph-data*
### neo4j Conatiner
  - *./data/neo4j/conf:/conf*
  - *./data/neo4j/data:/data*
  - *./data/neo4j/import:/import*
  - *./data/neo4j/logs:/logs*
  - *./data/neo4j/plugins:/plugins*

