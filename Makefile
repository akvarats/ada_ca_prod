build:
	docker-compose build

up:
	docker-compose up -d

up-non-daemon:
	docker-compose up

start:
	docker-compose start

stop:
	docker-compose stop

down:
	docker-compose down

restart:
	docker-compose restart

restart-auth:
	docker-compose restart auth

restart-classification-gate:
	docker-compose restart classification_gate

shell-gw:
	docker exec -it ada_gw bash

shell-auth:
	docker exec -it ada_auth bash

shell-classification-gate:
	docker exec -it ada_classification_gate

logs-gw:
	docker-compose logs gw

logs-auth:
	docker-compose logs auth

logs-classification-gate:
	docker-compose logs classification_gate

logs-recovery:
	docker-compose logs recovery