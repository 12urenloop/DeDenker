# De Denker

> A Lapper that makes you HMM 

Counting Laps using a custom trained Hidden Markov Model using the Baum Welch algorithm. Read more about it here: [FKD13/12urenloop-hmmlearn](https://github.com/FKD13/12urenloop-hmmlearn/blob/yeet/report.pdf).

## Production Setup

One option is to use the prebuild docker image: `ghcr.io/12urenloop/dedenker:main`.
A possible `docker-compose.yml` can be the next one. Adapt where needed.

```
services:
  de-denker:
    image: ghcr.io/12urenloop/dedenker:main
    restart: unless-stopped
    environment:
      - "DD_TELRAAM_URL=http://telraam.local:8080"
```

You will need to run your own [Telraam](https://github.com/12urenloop/Telraam) instance for development. Ask for help in the ~12urenloop channel on our [Mattermost](https://chat.zeus.gent) instance if guidance is needed with setting this all up.

## Development Setup

Create a virtualenv

```shell
python3 -m venv venv
. venv/bin/activate
```

```shell
pip install poetry
poetry install
```
