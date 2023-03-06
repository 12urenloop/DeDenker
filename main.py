from time import time, sleep

import colorlog
import numpy as np
from hmmlearn.base import ConvergenceMonitor
from hmmlearn.hmm import CategoricalHMM

from config import RONNY_COUNT, SLEEP_DURATION
from static_probabilities import START_PROBABILITIES_12UL, EMISSION_PROBABILITIES_12UL, TRANSITION_PROBABILITIES_12UL
from telraam_api import TelraamAPI

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s\t%(message)s'))

logger = colorlog.getLogger('example')
logger.addHandler(handler)
logger.setLevel('DEBUG')

api: TelraamAPI = TelraamAPI()

# The training timer, initialized after initial training
last_training: float = 0

# The model used for decoding
model: CategoricalHMM | None = None

while True:
    start = time()

    detections: list = sorted(api.get_detections(), key=lambda x: x["timestamp"])
    stations: list = sorted(api.get_stations(), key=lambda x: x["id"])
    teams: list = api.get_teams()
    baton_switchovers: list = sorted(api.get_baton_switchovers(), key=lambda x: x["timestamp"])
    batons: list = api.get_batons()

    # Process the detections

    team_detections: dict[int, list] = {team["id"]: [] for team in teams}
    team_by_id: dict[int, dict] = {team["id"]: team for team in teams}
    baton_team: dict[int, dict] = {}

    switchover_index = 0
    for detection in detections:
        while switchover_index < len(baton_switchovers) and baton_switchovers[switchover_index]["timestamp"] < \
                detection["timestamp"]:
            switchover = baton_switchovers[switchover_index]
            if switchover["previousBatonId"] in baton_team:
                if baton_team[switchover["previousBatonId"]] == team_by_id[switchover["teamId"]]:
                    del baton_team[switchover["previousBatonId"]]
                else:
                    logger.warning(
                        f"baton ({switchover['previousBatonId']}) was not assigned to team {switchover['teamId']} at time of de assignment"
                    )
            if switchover["newBatonId"] is not None:
                baton_team[switchover["newBatonId"]] = team_by_id[switchover["teamId"]]
            switchover_index += 1

        if detection["batonId"] in baton_team:
            if detection["rssi"] > -80:
                current_detections = team_detections[baton_team[detection["batonId"]]["id"]]
                if len(current_detections) > 0 and current_detections[-1]["timestamp"] == detection["timestamp"]:
                    if current_detections[-1]["rssi"] < detection["rssi"]:
                        current_detections[-1] = detection
                else:
                    current_detections.append(detection)

    # Our station ids are not usable as detection identifier. These need to go from 0..n-1 with n the number of stations
    # To achieve this we map the station to a unique id in this range so this can be used by hmmlearn
    # for training and decoding.
    station_to_emission = {v: k for k, v in enumerate([station["id"] for station in stations])}

    # If last training was more than 5 minutes ago, Train again
    if model is None or time() - last_training > 30:  # (5 * 60):
        logger.info(f"Starting training on {len(detections)} detections")

        # Adapt the detection data to the required format.
        training_data = [
            [[station_to_emission[detection["stationId"]]] for detection in team_detections[i]]
            for i in team_detections.keys()
        ]
        training_data_lengths = [len(x) for x in training_data]

        # Set up the model. We start from probabilities retrieved from the last event.
        # This should help us predict correct laps when limited data is available in the beginning of the event.
        model = CategoricalHMM(n_components=RONNY_COUNT, n_iter=1000, init_params="", implementation="scaling")
        model.transmat_ = TRANSITION_PROBABILITIES_12UL.copy()
        model.emissionprob_ = EMISSION_PROBABILITIES_12UL.copy()
        model.startprob_ = START_PROBABILITIES_12UL.copy()

        # TODO: is this needed? We don't make any graphs. Maybe nice to have some stats?
        model.monitor_ = ConvergenceMonitor(model.monitor_.tol, model.monitor_.n_iter, model.monitor_.verbose)

        # Train the model
        model.fit(np.concatenate(training_data), training_data_lengths)

        logger.info(
            f"Training converged after {model.monitor_.iter} iterations with error {model.monitor_.history[-1]}"
        )

        # Reset the training timer
        last_training = time()
    else:
        logger.debug("Training timeout not reached, continuing with previous model")

    half = RONNY_COUNT // 2

    team_laps: list[dict] = []

    for team in teams:
        decode_data = np.array([
            [station_to_emission[detection["stationId"]] for detection in team_detections[team["id"]]]
        ])

        _, path = model.decode(decode_data)

        laps: list[dict] = []

        prev = path[0]
        for i, segment in enumerate(path[1:]):
            delta = half - (half - (segment - prev)) % RONNY_COUNT
            if delta > 0 and prev > segment:
                laps.append({
                    'timestamp': team_detections[team["id"]][i + 1]["timestamp"]
                })
            elif delta < 0 and prev < segment:
                if len(laps) > 0:
                    laps.pop()
            prev = segment

        logger.debug(f"Counted {len(laps)} laps for {team['name']}")

        team_laps.append({'teamId': team["id"], 'laps': laps})

    # do_push(laps)
    api.post_laps(team_laps)

    logger.info(f'Lapper took {time() - start:.2f} seconds for this iteration')

    logger.debug(f'Going to sleep for {SLEEP_DURATION} seconds')

    sleep(SLEEP_DURATION)
