# SAGAS Coreografado

Praticando SAGAS coreografado com Python e RabbitMQ.

Executando o broker:

```bash
docker compose up
```
 
Serviços (um por terminal):
* `python fly.py`
* `python hotel.py`
* `python car.py`

Iniciando o fluxo:

1. Abra o console do broker em `http://localhost:15672`
  * Usuário: `usuario`
  * Senha: `senha`
2. Vá em _Exchanges_ e localize _sagas_
3. Em `Publish message`:
  * _Routing key:_ `fly` (primeiro serviço da sequência)
  * _Payload:_ `{ "action": "proceed", "data": { "qualquer": "coisa" } }`



