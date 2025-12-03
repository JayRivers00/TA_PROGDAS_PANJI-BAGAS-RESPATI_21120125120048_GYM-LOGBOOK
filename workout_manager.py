import csv
from workout_entry import WorkoutEntry
from datetime import datetime

class WorkoutManager:

    def __init__(self):
        self.entries = []
        self.file = "gym_log.csv"

    # Load & Save
    def init_csv(self):
        try:
            with open(self.file, "x", newline='') as f:
                w = csv.writer(f)
                w.writerow(["date", "exercise", "sets", "reps", "weight", "notes", "rir"])
        except FileExistsError:
            pass

    def load(self):
        self.entries = []
        try:
            with open(self.file, "r") as f:
                r = csv.DictReader(f)
                for row in r:
                    e = WorkoutEntry(
                        row["date"], row["exercise"],
                        row["sets"], row["reps"], row["weight"],
                        row["notes"], row["rir"]
                    )
                    self.entries.append(e)
        except FileNotFoundError:
            pass

    def save_all(self):
        with open(self.file, "w", newline='') as f:
            w = csv.writer(f)
            w.writerow(["date", "exercise", "sets", "reps", "weight", "notes", "rir"])
            for e in self.entries:
                w.writerow([e.d, e.ex, e.sets, e.reps, e.weight, e.notes, e.rir])

    # tambah entry
    def add(self, entry):
        is_pr = False

        # cek PR
        same_ex = self.by_exercise(entry.ex)
        if same_ex:
            prev_max = max([e.volume() for e in same_ex])
            if entry.volume() > prev_max:
                is_pr = True

        self.entries.append(entry)
        self.save_all()
        return is_pr

    def delete(self, idx):
        if idx < 0 or idx >= len(self.entries):
            return False
        del self.entries[idx]
        self.save_all()
        return True

    def undo_last(self):
        if not self.entries:
            return False
        self.entries.pop()
        self.save_all()
        return True

    def by_exercise(self, ex):
        return [e for e in self.entries if e.ex.lower() == ex.lower()]

    def get_prev_entry(self, exercise, current):
        same = [e for e in self.entries if e.ex.lower() == exercise.lower()]

        if len(same) < 2:
            return None 

        same_sorted = sorted(same, key=lambda e: datetime.strptime(e.d, "%Y-%m-%d"))
        idx = same_sorted.index(current)

        if idx == 0:
            return None

        return same_sorted[idx - 1]


    # Load Progression Rate (LPR)
    def get_progression(self, entry):
        prev = self.get_prev_entry(entry.ex, entry)
        if prev:
            try:
                return entry.load_progression(prev)
            except:
                return 0
        return 0

    # Fatigue Index
    def get_fatigue(self, entry):
        try:
            return entry.fatigue_index()
        except:
            return 0

    # Plateau Detection
    def detect_plateau(self, exercise):
        data = self.by_exercise(exercise)
        if len(data) < 3:
            return False

        last_three = data[-3:]
        one_rms = [e.one_rm() for e in last_three]

        return (one_rms[2] <= one_rms[1] and one_rms[1] <= one_rms[0])
