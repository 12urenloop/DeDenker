from config import TELRAAM_URL


class DetectionCollector(object):

    def __init__(self, url_suffix):
        self.url_suffix = url_suffix
        self.last_id = "0"
        self.detections = []
        detections_update(limit=1000)

    def detections_update(limit=1000):
        # get new, and update last_id
        new_detections = requests.get(f'{TELRAAM_URL}/url_suffix/{self.last_id}?limit={limit}')
        self.last_id = new_detections[-1]["id"]

        # sort using timestamp
        self.detections = sorted(new_detections, key=lambda x: x["timestamp"])
