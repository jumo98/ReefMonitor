# ReefMonitor

[![CircleCI](https://circleci.com/gh/jumo98/ReefMonitor/tree/main.svg?style=svg)](https://circleci.com/gh/jumo98/ReefMonitor/tree/main)

## Deployment

The necessary deployment resources can be found in the directory `deployment`.

As a requirement the a Kubernetes Secret (env) with the name `reefmonitor-config` must be deployed in the namespace `reefmonitor` with the following properties:

|    Environment Variable   	| Description                         	|     Example Value    	|
|-------------------------	|-------------------------------------	|--------------------	|
| HOST                      	| Hostname of the system              	| reefmonitor.de       	|
| SECRET_KEY                	| Secret key for Django               	| supersecr3t          	|
| INFLUX_URL                	| URL of your InfluxDB                	| http://influxdb:8086 	|
| INFLUX_USER               	| Username for the InfluxDB           	| user                 	|
| INFLUX_PASSWORD           	| Password for the InfluxDB           	| pass                 	|
| INFLUX_TOKEN              	| Token for the InfluxDB              	| Secr3tTok3n          	|
| POSTGRE_HOST              	| Address of your PostgreSQL database 	| postgres             	|
| POSTGRE_USER              	| PostgreSQL username                 	| user                 	|
| POSTGRE_PASSWORD          	| PostgreSQL password                 	| pass                 	|
| EMAIL_HOST_USER           	| E-Mail provider username            	| user                 	|
| EMAIL_HOST_PASSWORD       	| E-Mail provider password            	| pass                 	|
| DJANGO_SUPERUSER_USERNAME 	| Django superuser username           	| user                 	|
| DJANGO_SUPERUSER_PASSWORD 	| Django superuser password           	| pass                 	|
| DJANGO_SUPERUSER_EMAIL    	| Django superuser email              	| myname@mail.com      	|