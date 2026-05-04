import json
import os

class Scoreboard:
    def __init__(self, path="data/scores.json", limit=10):
        self.path = path
        self.limit = limit

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    # -------------------------
    # LOAD SCORES
    # -------------------------
    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    # -------------------------
    # SAVE SCORE
    # -------------------------
    def add_score(self, name, time, run_id):
        scores = self.load()

        scores.append({
            "name": name,
            "time": round(time, 2),
            "run_id": run_id
        })

        scores.sort(key=lambda x: x["time"])

        with open(self.path, "w") as f:
            json.dump(scores, f, indent=4)

    # -------------------------
    # TOP N (leaderboard)
    # -------------------------
    def get_top(self):
        scores = self.load()
        scores.sort(key=lambda x: x["time"])
        return scores[:self.limit]

    # -------------------------
    # ALL SCORES
    # -------------------------
    def get_all(self):
        scores = self.load()
        scores.sort(key=lambda x: x["time"])
        return scores