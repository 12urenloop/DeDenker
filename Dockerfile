FROM python:3.13.2-alpine3.21 AS base


FROM base AS build

WORKDIR /dedenker

RUN apk add --no-cache build-base
RUN pip install poetry==2.1
RUN poetry self add poetry-pyinstaller-plugin==1.4

COPY pyproject.toml poetry.lock .
RUN poetry install --no-root

COPY dedenker/ dedenker/
RUN PYTHONOPTIMIZE=2 poetry build --format=pyinstaller
RUN mv dist/pyinstaller/musllinux_1_2_x86_64/dedenker dist/


FROM scratch AS artifact
COPY --from=base /lib/ld-musl-x86_64.so.1 /usr/lib/libz.so.1 /lib/
COPY --from=base /tmp /tmp
COPY --from=build /dedenker/dist/dedenker /dedenker
CMD ["/dedenker"]
