FROM python:3.13.2-alpine3.21 AS base
WORKDIR /de-denker

FROM base AS requirements
RUN pip install poetry-plugin-export
COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

FROM base AS build
RUN apk add --no-cache build-base
ENV PYTHONDONTWRITEBYTECODE=1
COPY --from=requirements /de-denker/requirements.txt .
RUN pip install -r requirements.txt

FROM base AS artifact
RUN apk add --no-cache libgomp libstdc++
COPY --from=build /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY ./dedenker ./dedenker
CMD ["python", "-m", "dedenker.main"]
