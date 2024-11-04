# Deploy Presto From a Docker Image

This guide will walk you through the steps to deploy Presto using Docker containers. Presto is a distributed SQL query engine designed for running interactive analytic queries against data sources of all sizes ranging from gigabytes to petabytes.



## Getting started



## Clone the Repository
First, clone the Presto repository from GitLab:

```
git clone https://gitlab.corp.ikala.tv/esther.yang/presto.git
cd presto
git checkout dev

git checkout dev

```
# Configuration

Presto configuration files are provided for the coordinator and worker nodes. You'll need to revise the configuration files according to your specific requirements.



### Coordinator Configuration


├── coordinator
│   ├── config.properties
│   ├── jvm.config
│   ├── log.properties
│   ├── node.properties
│   ├── postgresql.properties
│   ├── elasticsearch.properties
│   └── bigquery.properties
├── worker1
│   ├── config.properties
│   ├── jvm.config
│   ├── node.properties
│   ├── postgresql.properties
│   ├── elasticsearch.properties
│   └── bigquery.properties
├── worker2
│   ├── config.properties
│   ├── jvm.config
│   ├── node.properties
│   ├── postgresql.properties
│   ├── elasticsearch.properties
│   └── bigquery.properties
├── worker2
│   ├── catalog
│   │   └── credential.json


***
Ensure to revise the each catalog properties configuration file for each node according to your PostgreSQL,Elasticsearch, BigQuery setup.

1. Revise the each ```postgresql.properties``` configuration
2. Revise the each ```elasticsearch.properties``` configuration
3. Revise the each ```bigquery.properties``` configuration
   1. Put the bigquery credential into `/path/etc/catalog/[credential].json`
   2. Revise the configuration in the bigquery.properties 

## Test and Deploy

Once you have configured the Presto nodes, you can test and deploy the Presto cluster using Docker.


1. docker compose up 
```
$ docker-compose -f docker-compose.yaml up -d
```
2. use the presto command line to query 
```
$ docker exec -i presto_test presto-cli
presto> 
```
- test the catalog connection 
```
$ docker exec -i presto_test presto-cli
presto>  SELECT * FROM SYSTEM.jdbc.catalogs;
```
- test the worker nodes active
```
$ docker exec -i presto_test presto-cli
presto> SELECT * FROM system.runtime.nodes;
```

- query use docker cli
```
(base) ➜ docker exec -i presto presto-cli --server 127.0.0.1:8080 --catalog postgresql --schema data --execute "select *
from postgresql."data".latest_instagram_post;"
```
- query use docker cli without output
```
(base) ➜ docker exec -i presto presto-cli --server 127.0.0.1:8080 --catalog postgresql --schema data --execute "select *
from postgresql."data".latest_instagram_post;" > /dev/null
```
- query use docker cli to csv
```
(base) ➜ docker exec -i presto presto-cli --server 127.0.0.1:8080 --catalog postgresql --schema data --output-format CSV_HEADER --execute "SELECT * FROM postgresql.data.latest_audience;" > latest_audience.csv
```


3. Open Presto Web GUI
```
http://localhost:8080/
```  

