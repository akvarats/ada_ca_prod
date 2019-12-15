#!/bin/sh

curl -i -d '{"text":"Не работает светофор"}' -H "Content-Type: application/json" -H "Authorization: token 454e351314464a979ede98764308fa19" -X POST http://gw/classify
curl -i -d '{"text":"Не работает светофор"}' -H "Content-Type: application/json" -H "Authorization: token b9666c82d3d84822b0d246d6b3980469" -X POST http://gw/classify