from requests import get, post

from config import TELRAAM_URL


class TelraamAPI:
    """
    A Class that can be used to query the Telraam api.
    Primirily just a wrapper around the api. Including an optimized detections downloader.
    """

    def __init__(self):
        self._detections_cache: list[dict] = []

    def _get(self, resource: str) -> list[dict]:
        response = get(f'{TELRAAM_URL}/{resource}')
        return response.json()

    def _get_detections_batch(self, limit) -> list[dict]:
        last_id: int = self._detections_cache[-1]["id"] if len(self._detections_cache) != 0 else 0
        return self._get(f'detection/since/{last_id}?limit={limit}')

    def get_detections(self, limit=1000):
        new_detections = self._get_detections_batch(limit)
        while len(new_detections) == limit:
            self._detections_cache += new_detections
            new_detections = self._get_detections_batch(limit)
        self._detections_cache += new_detections
        return self._detections_cache.copy()

    def get_stations(self) -> list[dict]:
        return self._get('station')

    def get_teams(self) -> list[dict]:
        return self._get('team')

    def get_batons(self) -> list[dict]:
        return self._get('baton')

    def get_baton_switchovers(self) -> list[dict]:
        return self._get('batonswitchover')

    def post_laps(self, team_laps: list[dict]) -> None:
        post(f'{TELRAAM_URL}/lappers/external/laps', json=team_laps)
