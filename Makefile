.PHONY: build run rebuild up down restart rm-volumes clean-up

##### service #####
build:
	./build-push.sh build-local

run:
	./build-push.sh run-local

rebuild: build run 


static-build:
	cd frontend && npm i && npm run build

run-bc:
	 ./backend/.venv/bin/uvicorn --app-dir ./backend  spread_auth.main:app --timeout-keep-alive 300 --port 5000 --reload

run-fr:
	cd ./frontend && npm run serve

run-all:
	$(MAKE) run-bc &
	$(MAKE) run-fr

###### store ######
up:
	docker run \
		--pull=always \
		--rm  \
        --hostname store-starter \
        --name store-starter \
	    --entrypoint "sh" \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v awada:/opt/awada \
		-e SPREAD_STORE_TAG=latest \
		alpha.awada.systems/spread-store:latest \
		-c 'cd /opt/store-updater/; \
			docker compose -f store-updater.compose.yaml up -d'

down:
	docker ps --filter 'label=com.docker.compose.project=awada' --format {{.ID}} | xargs -n 1 docker rm --force && sleep 1 || true

restart: down up

rm-volumes:
	docker volume rm awada awada-sockets awada-snippets || true

clean-up: down rm-volumes up
