# OPENSPECIMEN FAIR Toolbox application

This container can be installed as [BIBBOX APP](https://bibbox.readthedocs.io/en/latest/) or standalone. 


* initial user: ** admin **
* initial password: ** Login@123 **
* After the installation follow these [instructions](INSTALL-APP.md)


## Docker Images Used 

 * [mySQL](https://hub.docker.com/_/mysql/), offical mySQL container
 * [openspecimen](https://hub.docker.com/r/bibbox/openspecimen/tags)
 

## Standalone Installation 
Clone the github repsoitory. If necessary change the ports and volume mounts in `docker-compose.yml`.

```
git clone https://github.com/bibbox/app-openspecimen-fair
cd app-openspecimen-fair
mkdir data
docker-compose up -d
```

The main app can be opened at 

```
http://localhost:9000/openspecimen
```


## Install Environment Variables

  * MYSQL_ROOT_PASSWORD = password, only used within the docker container
  * MYSQL_DATABASE = name of the mysql database, typical *openspecimen*. The DB file is stored in the mounted volume
  * MYSQL_USER = name of the mysql user, typical *openspecimen*
  * MYSQL_PASSWORD = mysql user password used for Openspecimen DB

------------------------------------------------------------------------------------------
## Troubleshooting
### In case the installation process reccurently shows the following information message

INFO  liquibase.executor.jvm.JdbcExecutor- SELECT `LOCKED` FROM openspecimen.DATABASECHANGELOGLOCK WHERE ID=1
INFO  liquibase.lockservice.StandardLockService- Waiting for changelog lock....

and the installationis not proceeding, do the following:
* Enter your mysql:8.0.26 container (Attach Shell to it) and execute the commands listed below:
------------------------------------------------------------------------------------------
mysql -uroot -p'openspecimen'

USE openspecimen

SELECT * from DATABASECHANGELOGLOCK;

UPDATE DATABASECHANGELOGLOCK SET LOCKED=FALSE, LOCKGRANTED=null, LOCKEDBY=null where ID=1;

------------------------------------------------------------------------------------------
* and rerun **docker-compose up** in the root folder of the project.  

