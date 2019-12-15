# ADA - classification appeals

## Setup

```sh
$ docker volume create storage ada_storage
```

## Run

Build docker services

```sh
$ make build
```

Restart

```sh
$ make restart
```

Open shell

```sh
$ make shell-gw
$ make shell-auth
$ make shell-classification-gate

$ make shell-ryazyan
$ make shell-yakutia
```

## Secrets

Location: ./secrets

Secret `jwt_secret_key`:
```
some-jwt-secret-key
```

Secret `region_tokens`:
```json
{
  "454e351314464a979ede98764308fa19": { "region": "ryazyan", "worker_url": "http://ryazyan" },
  "b9666c82d3d84822b0d246d6b3980469": { "region": "yakutiya", "worker_url": "http://yakutiya" }
}
```

## Storage

```shell script
$ docker create volume ada_storage
```

## Models

Prepare word2vec model:

```shell script
$ mkdir models/180
$ wget http://vectors.nlpl.eu/repository/11/180.zip -O tmp.zip; unzip -o -d models/180 tmp.zip; rm -rf tmp.zip
```

## Testing

### Test classification worker

Worker environment variables:

```
ADA_STORAGE=/tmp/ada_storage
```



## Links

API: https://gist.github.com/akvarats/2502259a1d72df64f6763223bc873177

Initial ASI-repo: https://git.asi.ru/damir.rakhimov/classification-appeals-ada

Word2Vec model http://vectors.nlpl.eu/repository/11/180.zip


