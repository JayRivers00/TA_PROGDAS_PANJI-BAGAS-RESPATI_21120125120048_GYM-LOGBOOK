class WorkoutEntry:
    def __init__(self, d, ex, sets, reps, weight, notes, rir):
        self.d = d
        self.ex = ex
        self.sets = int(sets)
        self.reps = int(reps)
        self.weight = float(weight)
        self.notes = notes
        self.rir = int(rir)

    def volume(self):
        return self.sets * self.reps * self.weight

    def one_rm(self):
        return round(self.weight * (1 + self.reps / 30), 2)

    def fatigue_index(self):
        try:
            fi = (self.sets * self.reps) / max(1, self.rir)
            return round(fi, 2)
        except:
            return 0

    def load_progression(self, prev):
        if not prev:
            return 0
        try:
            return round(((self.weight - prev.weight) / prev.weight) * 100, 2)
        except:
            return 0

    def to_list(self):
        return [
            self.d, self.ex, self.sets, self.reps,
            self.weight, self.notes, self.rir
        ]
