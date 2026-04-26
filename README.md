# De Denker

> A Lapper that makes you HMM 

Counting Laps using a custom trained Hidden Markov Model using the Baum Welch algorithm. Read more about it here: [FKD13/12urenloop-hmmlearn](https://github.com/FKD13/12urenloop-hmmlearn/blob/yeet/report.pdf).

## Production Setup

One option is to use the prebuild docker image: `ghcr.io/12urenloop/dedenker:main`.
A possible `docker-compose.yml` can be the next one. Adapt where needed.

```yml
services:
  dedenker:
    image: ghcr.io/12urenloop/dedenker
    restart: unless-stopped
    environment:
      - "DD_TELRAAM_URL=http://telraam.local:8080"
```

You will need to run your own [Telraam](https://github.com/12urenloop/Telraam) instance for development. Ask for help in the ~12urenloop channel on our [Mattermost](https://chat.zeus.gent) instance if guidance is needed with setting this all up.

## Development Setup

Make sure `uv` is installed:

```console
command -v uv || (curl -LsSf https://astral.sh/uv/install.sh | sh)
```

Create a `.venv`:

```console
uv venv --python=python3.14
source .venv/bin/activate
```

Install dependencies:

```console
uv sync --frozen
```

Run DeDenker:

```console
python -m dedenker
```
