FROM ghcr.io/astral-sh/uv:python3.14-alpine3.23 AS base


FROM base AS build

WORKDIR /dedenker/

RUN apk add --no-cache build-base

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --frozen

COPY ./dedenker/ ./dedenker/
RUN uv run pyinstaller --onefile --name=dedenker --optimize=2 --strip ./dedenker/__main__.py


FROM scratch AS artifact

COPY --from=base /lib/ld-musl-x86_64.so.1 /usr/lib/libz.so.1 /lib/
COPY --from=base /tmp/ /tmp/
COPY --from=build /dedenker/dist/dedenker /dedenker
CMD ["/dedenker"]
