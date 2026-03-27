# SQL-Commands Lab

Este repositório é o meu lab de dados, configurado para ser customizável e já pronto para uso com Debezium e Redpanda (event streaming). A arquitetura atual suporta captura de mudanças em tempo real a partir do Postgres e fluxo de eventos para aplicações de streaming.

## O que este lab implementa

- Replicação de banco de dados (CDC)
- Aplicações de processamento de stream
- Pipelines de ETL em streaming
- Atualização de caches em tempo real
- Microsserviços orientados a eventos

## Estrutura principal

- `docker-compose.yml`: orquestra Postgres, pgAdmin, Redpanda, Debezium, Jupyter e Redis.
- `postgres/`: configuração e scripts de inicialização do PostgreSQL.
- `debezium/`: conector Debezium para outbox/event stream.
- `jupyter/`: ambiente Python/jupyter para explorar dados e SQL.

## Uso

1. Ajuste o arquivo `.env` com credenciais e URLs.
2. Execute `./start.sh` para subir o ambiente.
3. Acesse Jupyter em `http://localhost:8888` e pgAdmin em `http://localhost:5050`.
4. Confira status dos conectores com `curl -s http://localhost:8083/connectors/postgres-connector/status`.

## Observação

Este lab está orientado a experimentação e aprendizado com streaming de dados e arquitetura event-driven.
