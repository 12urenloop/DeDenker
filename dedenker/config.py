import os

TELRAAM_URL: str = os.environ.get('DD_TELRAAM_URL', 'http://localhost:8080')
LAP_SOURCE_ID: int = int(os.environ.get('DD_LAP_SOURCE_ID', '0'))
RONNY_COUNT: int = int(os.environ.get('DD_RONNY_COUNT', '7'))
SLEEP_DURATION: int = int(os.environ.get('DD_SLEEP_DURATION', '5'))
