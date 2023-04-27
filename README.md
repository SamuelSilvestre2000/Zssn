#Documentação do Projeto Zombie Survival Social Network (ZSSN)
##Introdução
O Zombie Survival Social Network (ZSSN) é um projeto de sistema de inventário de sobreviventes em um apocalipse zumbi. O projeto foi desenvolvido em Django, um framework web de alto nível em Python, e utiliza um banco de dados SQLite3. O sistema consiste em três modelos: Sobrevivente, Item e Registro de Troca, que estão relacionados entre si.

##Funcionalidades
As funcionalidades do ZSSN são divididas em dois grupos: sobreviventes e itens.

###Sobreviventes
Os sobreviventes podem ser criados, atualizados e marcados como infectados ou não infectados. As informações de um sobrevivente incluem seu nome, idade, gênero, localização e inventário.

###Itens
Os itens podem ser criados e atualizados. Os tipos de itens incluem água, comida, remédio e munição.

###Troca de Itens
Os sobreviventes podem trocar itens entre si. O sistema registra a troca e verifica se ambas as partes estão de acordo com a troca.

##Endpoints
Os endpoints do ZSSN estão listados abaixo. Todos os endpoints retornam JSON.

###Sobreviventes
GET /api/survivors/ - Retorna uma lista de todos os sobreviventes cadastrados no sistema.
POST /api/survivors/ - Cria um novo sobrevivente. As informações do sobrevivente e do inventário devem ser fornecidas no corpo da solicitação.
GET /api/survivors/{id}/ - Retorna informações sobre um sobrevivente específico.
PATCH /api/survivors/{id}/ - Atualiza as informações de um sobrevivente específico. As informações a serem atualizadas devem ser fornecidas no corpo da solicitação.
POST /api/survivors/{id}/report_infection/ - Marca um sobrevivente como infectado.
###Itens
GET /api/items/ - Retorna uma lista de todos os itens cadastrados no sistema.
POST /api/items/ - Cria um novo item. As informações do item devem ser fornecidas no corpo da solicitação.
GET /api/items/{id}/ - Retorna informações sobre um item específico.
PATCH /api/items/{id}/ - Atualiza as informações de um item específico. As informações a serem atualizadas devem ser fornecidas no corpo da solicitação.
###Troca de Itens
POST /api/trade/ - Registra uma troca de itens entre dois sobreviventes. As informações dos sobreviventes e dos itens devem ser fornecidas no corpo da solicitação.
##Tecnologias
Python 3.8.5
Django 3.2.5
SQLite3
HTML5
CSS3
JavaScript
##Instalação
