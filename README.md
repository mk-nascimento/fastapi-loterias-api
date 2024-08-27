# fastapi-loterias-api
Esta API foi desenvolvido para consulta dos resultados das loterias da Caixa Econômica Federal do Brasil. A aplicação permite acessar os resultados mais recentes ou de concursos específicos através de rotas simples. Utiliza MongoDB para armazenamento dos dados e Redis para cache, melhorando o desempenho das consultas.

## Funcionalidades

- **Consulta do último resultado de uma loteria**: Obtenha o último resultado disponível para uma loteria específica.
- **Consulta de resultado por concurso**: Acesse o resultado de um concurso específico através do seu número.
- **Armazenamento e cache**: Usa MongoDB para persistência de dados e Redis para cache dos resultados mais recentes.

## Instalação

1. **Pré-requisitos**:
   - [![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB.svg?logo=python)](https://www.python.org/downloads/release/python-3110/)
   - [![MongoDB](https://img.shields.io/badge/MongoDB-7.0+-4FAA41.svg?logo=mongodb)](https://www.mongodb.com/pt-br/docs/manual/installation/)
   - [![Redis](https://img.shields.io/badge/Redis-7.4+-DC382D.svg?logo=redis)](https://www.example.org)
    - [![Poetry 1.8+](https://img.shields.io/badge/Poetry-1.8+-60A5FA.svg?logo=poetry)](https://python-poetry.org/docs/#installation)

2. **Clonar o repositório**:
   ```bash
   git clone https://github.com/mk-nascimento/fastapi-loterias-api.git
   cd fastapi-loterias-api
   ```

3. **Instalar as dependências**:

    - Poetry
        > Antes de prosseguir com a instalação, é recomendado verificar a versão do Python e Poetry recomendada no topo deste arquivo. Certifique-se de ter a versão correta instalada em seu sistema antes de continuar.
        ```sh
        poetry install
        ```

    - Ou, se você preferir usar pip:
        > Antes de prosseguir com a instalação, é recomendado verificar a versão do Python recomendada no topo deste arquivo. Certifique-se de ter a versão correta instalada em seu sistema antes de continuar.
        ```sh
        pip install -r requirements.txt
        ```

4. **Configurar variáveis de ambiente**:
   - Crie um arquivo `.env` partindo do [.env.example](.env.example):
   ```bash
    cp .env.example .env
   ```

5. **Executar a aplicação**:
   ```bash
   poetry run fastapi run loterias/main.py
   ```

   A aplicação estará disponível em `http://localhost:8000`.

## Rotas Disponíveis

### 1. **Índice**

- **GET /**
  Retorna uma página HTML simples com um link para a documentação Swagger.

  **Exemplo de resposta**:
  ```html
  Visit Swagger documentation at: <a href='/docs'>/docs</a>
  ```

### 2. **Obter o último resultado de uma loteria**

- **GET /{loteria}**
  Retorna o último resultado disponível para a loteria especificada.

  **Parâmetros**:
  - `loteria` (str): Nome da loteria (ex: "megasena", "quina").

  **Exemplo de resposta**:
  ```json
  {
    "_id": "64dfc...",
    "acumulado": false,
    "dataApuracao": "01/01/2001",
    ...
  }
  ```

### 3. **Obter o resultado de um concurso específico**

- **GET /{loteria}/{concurso}**
  Retorna o resultado do concurso especificado para a loteria.

  **Parâmetros**:
  - `loteria` (str): Nome da loteria (ex: "megasena", "quina").
  - `concurso` (int): Número do concurso (ex: 123).

  **Exemplo de resposta**:
  ```json
  {
    "_id": "64dfc...",
    "acumulado": false,
    "dataApuracao": "01/01/2001",
    ...
  }
  ```

  **Erros possíveis**:
  - `404 NOT FOUND`: Quando o concurso solicitado não é encontrado.

## Considerações

- A rota `/` é oculta no Swagger e serve apenas para redirecionar os usuários à documentação da API.
- As rotas foram projetadas para ser simples e intuitivas, com tratamento de erros e validação de parâmetros.

## Contribuição

Contribuições são bem-vindas! Por favor, envie um pull request ou abra uma issue para discutir as mudanças que deseja fazer.

## Licença

Este projeto está licenciado sob a licença Apache 2.0 - veja o arquivo [LICENSE](LICENSE) para detalhes.
