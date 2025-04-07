FROM python:3.13.2-alpine3.21 AS requirements

RUN pip install poetry-plugin-export

WORKDIR /de-denker

COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

FROM python:3.13.2-alpine3.21 AS build

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /de-denker

RUN apk add build-base

COPY --from=requirements /de-denker/requirements.txt .

RUN pip install -r requirements.txt

FROM python:3.13.2-alpine3.21

COPY --from=build /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

COPY config.py main.py models.py static_probabilities.py telraam_api.py ./

CMD ["python", "main.py"]
