# Documentação do Projeto Zombie Survival Social Network (ZSSN)

## Introdução
O Zombie Survival Social Network (ZSSN) é um projeto de sistema de inventário de sobreviventes em um apocalipse zumbi. O projeto foi desenvolvido em Django, um framework web de alto nível em Python, e utiliza um banco de dados SQLite3. O sistema consiste em três modelos: Sobrevivente, Item e Registro de Troca, que estão relacionados entre si.

## Funcionalidades
As funcionalidades do ZSSN são divididas em dois grupos: sobreviventes e itens.

### Sobreviventes
Os sobreviventes podem ser criados, atualizados e marcados como infectados ou não infectados. As informações de um sobrevivente incluem seu nome, idade, gênero, localização e inventário.

### Itens
Os itens podem ser criados e atualizados. Os tipos de itens incluem água, comida, remédio e munição.

### Troca de Itens
Os sobreviventes podem trocar itens entre si. O sistema registra a troca e verifica se ambas as partes estão de acordo com a troca.

## Endpoints
Os endpoints do ZSSN estão listados abaixo. Todos os endpoints retornam JSON.

### Sobreviventes
* __GET /api/survivors/__ - Retorna uma lista de todos os sobreviventes cadastrados no sistema.  
* __POST /api/survivors/__ - Cria um novo sobrevivente. As informações do sobrevivente e do inventário devem ser fornecidas no corpo da solicitação.  
* __GET /api/survivors/{id}/__ - Retorna informações sobre um sobrevivente específico.  
* __PATCH /api/survivors/{id}/__ - Atualiza as informações de um sobrevivente específico. As informações a serem atualizadas devem ser fornecidas no corpo da solicitação.  
* __POST /api/survivors/{id}/report_infection/__ - Marca um sobrevivente como infectado.  
### Itens
* __GET /api/items/__ - Retorna uma lista de todos os itens cadastrados no sistema.  
* __POST /api/items/__ - Cria um novo item. As informações do item devem ser fornecidas no corpo da solicitação.  
* __GET /api/items/{id}/__ - Retorna informações sobre um item específico.  
* __PATCH /api/items/{id}/__ - Atualiza as informações de um item específico. As informações a serem atualizadas devem ser fornecidas no corpo da solicitação.  
### Troca de Itens
* __POST /api/trade/__ - Registra uma troca de itens entre dois sobreviventes. As informações dos sobreviventes e dos itens devem ser fornecidas no corpo da solicitação.  
## Tecnologias
Python 3.8.5  
Django 3.2.5  
SQLite3  
HTML5  
CSS3  
JavaScript  
## Instalação
1. Clone o repositório  
2. Crie um ambiente virtual: python -m venv venv  
3. Ative o ambiente virtual: venv\Scripts\activate (Windows) ou source venv/bin/activate (Linux/MacOS)  
4. Instale as dependências: `pip install -r requirements.txt`  
5. Execute as migrações do banco de dados: `python manage.py migrate`  
6. Crie um superusuário: `python manage.py createsuperuser`  
7. Inicie o servidor: `python manage.py runserver`  
8. Acesse o sistema em http://localhost:8000/  
