#### OBJETIVO
criar uma stack

para importar os dados fundos 
http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/
e criar um base de dados mongo.


## instalar
> docker-compose -d --build 

## baixar dados
> docker-compose run app import_all
> docker-compose run app import_cadastro
> docker-compose run app convert_db