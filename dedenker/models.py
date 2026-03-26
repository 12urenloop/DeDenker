class Detection:
    __slots__ = ["id", "timestamp", "baton_id", "station_id", "rssi"]

    def __init__(self, d_id, timestamp, baton_id, station_id, rssi):
        self.id = d_id
        self.timestamp = timestamp
        self.baton_id = baton_id
        self.rssi = rssi
        self.station_id = station_id
