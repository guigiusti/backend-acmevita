<p align="center">
  <h1 align="center">ACMEVita - API</h1>
</p>
<div align="center" margin-top="25px">

  ![](https://img.shields.io/github/languages/count/guigiusti/backend-acmevita)
  ![](https://img.shields.io/github/languages/top/guigiusti/backend-acmevita)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## Sumário
- [Sobre](#sobre)
- [Requisitos](#requisitos)
- [Como rodar](#como-rodar)
- [Como rodar em ambiente de desenvolvimento](#como-rodar-em-ambiente-de-desenvolvimento)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Endpoints](#endpoints)

## Sobre

Projeto de criação de uma API utilizando FastAPI com deploy em Docker Container. Possuí opção de utilizar um banco de dados local em SQLite ou PostgreSQL via Docker. Utiliza do Redis para Rate Limiting e do Nginx como proxy reverso.

Para segurança, tanto o container de PostgreSQL quanto de Redis, estão disponíveis para acesso apenas dentro da rede interna do Docker.

Um teste completo se encontra na [pasta de testes](https://github.com/guigiusti/backend-acmevita/tree/master/tests).

Após iniciar o container, a documentação ficará disponível em: http://localhost/api/v1/docs ou http://localhost/api/v1/redocs

## Próximos passos

- Autenticação com JWT ou via serviço externo como Clerk
- Deixar PostgreSQL e Redis mais seguros. Ex: Mudando a senha
- Colocar autenticação nos endpoints de documentação (caso necessário)
- Endpoints de PUT e DELETE

## Estrutura do Projeto
```
app/
├── api/
│   ├── routes/
├── core/            
│   ├── middleware/
├── models/  
├── schemas/         
tests/
```


## Requisitos

### Docker

Siga a [documentação](https://docs.docker.com/engine/install/) respectiva à sua máquina para instalar o docker. 

### Clone o repositório
```
git clone https://github.com/guigiusti/backend-acmevita.git

cd backend-acmevita
```

### Variáveis de ambiente

ENV = "production" | "development" (opcional, padrão é production)

## Como utilizar:

Dentro da raiz do projeto, abra o terminal e digite:

```
docker compose up
```

Para rodar no fundo (detached):

```
docker compose up -d
```

**Importante:**

Para usar o SQLite em vez do PostgreSQL, pode-se remover no arquivo de [docker-compose](https://github.com/guigiusti/backend-acmevita/blob/master/docker-compose.yaml) em APP a seguinte configuração de ambiente "DB_URL". Em ambiente de desenvolvimento, utiliza-se SQLite por padrão.

De igual forma pode-se alterar a configuração de ambiente RATE_LIMIT_ENABLED, para habilitar ou desabilitar o Rate Limiter. Outras configurações podem ser alteradas no [arquivo de configuração da api](https://github.com/guigiusti/backend-acmevita/blob/master/app/core/configs.py).

### Exemplos

Como adicionar um departamento com curl:
```
curl -X POST http://localhost/api/v1/department \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tecnologia"
  }'
```

Como adicionar um colaborador com curl:
```
curl -X POST http://localhost/api/v1/employee \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Guilherme Giusti",
    "department_id": 1,
  }'
```
ou com dependentes:
```
curl -X POST http://localhost/api/v1/employee \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Guilherme Giusti",
    "department_id": 1,
    "dependents": [
      { "name": "Gabriel" },
    ]
  }'
```
Retornar todos departamentos com curl (ou http://localhost/api/v1/departament no navegador):
```
curl -X GET http://localhost/api/v1/department \
  -H "Accept: application/json"
```
Retornar usuários de um departamento com curl (ou http://localhost/api/v1/employee/:department_id: no navegador)
```
curl -X GET http://localhost/api/v1/employee/:department_id: \
  -H "Accept: application/json"
```

## Como utilizar em ambiente de desenvolvimento
Caso ainda não tenha o Python instalado, siga as instruções de instalação no [site oficial](https://www.python.org/downloads/).

Com o Python instalado. Crie um ambiente virtual:
```
python -m venv env
```
Ative-o:
```
source env/bin/activate
```

Para instalar os pacotes utilizados:
```
pip install -r requirements.txt
```
E por fim, para rodar em modo de desenvolvimento:
```
fastapi dev app/main.py
```

### Rodando o teste

Primeiramente mude nas configurações a variável ENV para "development".

Agora basta digitar:

```
pytest tests/
```




## Endpoints

### Departamento
```
GET /department
HTTP 200

Response Body: [
    {
        "id": int,
        "name": string
    }
]
```
```
POST /department
HTTP 201

Request Body {
    "name": string
}
Response Body: {
    "id": int,
    "name": "string"
}
```
### Colaboradores
```
GET /employee/:department_id:
HTTP 200

Response Body: [
    {
        "id": int,
        "name": string
    }
]
```
```
POST /employee
HTTP 201

Request Body {
    "name": strig,
    "department_id": int,
    "dependents": opicional [{
        "name": string
    }]
}
Response Body: {
    "id": int,
    "name": "string",
    "department_id": int,
    "have_dependents": boolean
    "dependents": [{
        "name": string
    }] ou []
}
```
### Manutenção
```
DELETE /clean-db # Apenas habilitado em modo de desenvolvimento. Como para uso dos testes.
HTTP 204
```
```
GET /health
HTTP 200
```
