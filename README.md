# Central de Atendimento API - FastAPI + MongoDB

Este projeto é uma API desenvolvida com **FastAPI** e **MongoDB** para gerenciar informações de clientes e seus cartões de crédito. A API permite realizar operações como bloqueio de cartões, consulta de limites e registro de operações no histórico do cliente.

## Funcionalidades

- **Bloqueio de Cartões**: Permite bloquear um cartão de crédito de um cliente e registrar o motivo do bloqueio.
- **Consulta de Limite**: Permite consultar o limite de crédito disponível, utilizado e total de um cartão de crédito.
- **Histórico de Operações**: Cada ação realizada (como bloqueio ou consulta de limite) é registrada no histórico do cliente para acompanhamento.

## Tecnologias Utilizadas

- **FastAPI**: Framework para criação da API.
- **MongoDB**: Banco de dados NoSQL para armazenar dados de clientes e seus cartões de crédito.
- **PyMongo**: Biblioteca Python para interação com o MongoDB.
- **Uvicorn**: Servidor ASGI para rodar a aplicação FastAPI.

