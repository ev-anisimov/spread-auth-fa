ARG PYTHON_VERSION=3.11
ARG NODE_VERSION=22.11.0
ARG DEV_REGISTRY=alpha.awada.systems

#############################
# frontend builder с установленными зависимостями проекта
#############################
FROM --platform=${BUILDPLATFORM} ${DEV_REGISTRY}/node:${NODE_VERSION} AS static-builder
#############################

WORKDIR /frontend/

COPY ./frontend/package*.json .

RUN --mount=type=cache,target=/tmp/npm-cache \
    npm set cache /tmp/npm-cache; \
    npm ci


#############################
# frontend builder с готовой статикой
#############################
FROM static-builder AS static
#############################

COPY ./frontend/ /frontend/

RUN npm run build


#############################
# python с установленными зависимостями проекта
#############################
FROM ${DEV_REGISTRY}/python-dev:${PYTHON_VERSION} AS prod-deps
#############################

WORKDIR /application/

COPY ./backend/poetry.lock ./backend/pyproject.toml /application/

RUN poetry install --no-root --without dev


#############################
# python с проектом
#############################
#############################
FROM prod-deps AS prod-builder
#############################

COPY ./backend/ /application/

RUN poetry install

RUN mkdir /config
RUN --mount=type=bind,source=generate_schema.py,target=/application/app/generate_schema.py \
    /application/.venv/bin/python3 ./app/generate_schema.py


#############################
FROM prod-builder AS dev-builder
#############################

RUN poetry install --with dev


#############################
FROM dev-builder AS dev
#############################

COPY --chmod=700 ./entrypoint.sh /entrypoint.sh
COPY --from=static /frontend/dist/web /static
COPY backend/config/dev.json /config/default.json
COPY location.snippet upstream.snippet /snippets/

WORKDIR /application

ENTRYPOINT [ "/entrypoint.sh" ]


#############################
FROM ${DEV_REGISTRY}/python:${PYTHON_VERSION} AS production
#############################

COPY --from=prod-builder /application /application
COPY --from=prod-builder /config/schema.json /config/schema.json
COPY --chmod=700 ./entrypoint.sh /entrypoint.sh
COPY --from=static /frontend/dist/web /static
COPY ./backend/config/prod.json /config/default.json
COPY location.snippet upstream.snippet /snippets/

WORKDIR /application

ENTRYPOINT [ "/entrypoint.sh" ]