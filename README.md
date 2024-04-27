# SAGAS Coreografado

Praticando SAGAS coreografado com Python e RabbitMQ.

## Executando o broker

```bash
docker compose up
```

## Dependências

```bash
pip install pika
```
 
## Serviços (um por terminal)

* `python fly.py`
* `python hotel.py`
* `python car.py`

# Iniciando o fluxo

1. Abra o console do broker em `http://localhost:15672`
  * Usuário: `usuario`
  * Senha: `senha`
2. Vá em _Exchanges_ e localize _sagas_
3. Em `Publish message`:
  * _Routing key:_ `fly` (primeiro serviço da sequência)
  * _Payload:_ `{ "action": "proceed", "data": { "qualquer": "coisa" } }`

# Busca por erros

Cada processamento que lança uma exceção cai na fila de erros, onde pode ser verificado.

1. Abra o console do broker em `http://localhost:15672`
  * Usuário: `usuario`
  * Senha: `senha`
2. Vá em _Queues_ e abra _errors_
3. Em `Get messages`:
  * Indique quantas mensagens deseja recuperar
  * Importante deixar o _Ack mode_ como _Nack message requeue true_