import matplotlib.pyplot as plt
from tkinter import messagebox


def show_volume(manager, exercise):
    data = manager.by_exercise(exercise)
    if not data:
        messagebox.showinfo("Info", f"Tidak ada data untuk {exercise}")
        return

    dates = [e.d for e in data]
    volumes = [e.volume() for e in data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, volumes, marker="o", linewidth=2, label="Volume")

    max_vol = max(volumes)
    idx = volumes.index(max_vol)

    plt.scatter([dates[idx]], [max_vol], s=200, marker="*", color="gold", label="PR")
    plt.title(f"Volume Progress – {exercise}")
    plt.ylabel("Volume (sets × reps × weight)")
    plt.xticks(rotation=30)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def show_1rm(manager, exercise):
    data = manager.by_exercise(exercise)
    if not data:
        messagebox.showinfo("Info", f"Tidak ada data untuk {exercise}")
        return

    dates = []
    one_rms = []

    for e in data:
        try:
            one_rm = e.weight * (1 + e.reps / 30)
            one_rms.append(round(one_rm, 2))
            dates.append(e.d)
        except:
            continue

    plt.figure(figsize=(8, 4))
    plt.plot(dates, one_rms, marker="o", linewidth=2, color="cyan", label="1RM")

    max_1rm = max(one_rms)
    idx = one_rms.index(max_1rm)

    plt.scatter([dates[idx]], [max_1rm], s=200, marker="*", color="gold", label="PR")
    plt.title(f"1RM Progress – {exercise}")
    plt.ylabel("Estimated 1RM (kg)")
    plt.xticks(rotation=30)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def show_fatigue(manager, exercise):
    data = manager.by_exercise(exercise)
    if not data:
        messagebox.showinfo("Info", f"Tidak ada data untuk {exercise}")
        return

    dates = [e.d for e in data]
    fatigue = [e.fatigue_index() for e in data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, fatigue, marker="o", color="orange", linewidth=2)
    plt.title(f"Fatigue Index – {exercise}")
    plt.ylabel("Fatigue Index")
    plt.xticks(rotation=30)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def show_lpr(manager, exercise):
    data = manager.by_exercise(exercise)
    if not data:
        messagebox.showinfo("Info", f"Tidak ada data untuk {exercise}")
        return

    dates = []
    LPRs = []

    for e in data:
        prev = manager.get_prev_entry(exercise, e)
        try:
            lpr = e.load_progression(prev)
        except:
            lpr = 0

        LPRs.append(lpr)
        dates.append(e.d)

    plt.figure(figsize=(8, 4))
    plt.bar(dates, LPRs, color="lightblue")
    plt.title(f"Load Progression Rate – {exercise}")
    plt.ylabel("LPR (%)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def check_plateau(manager, exercise):
    if manager.detect_plateau(exercise):
        messagebox.showwarning("Plateau Warning!",
                               f"Kamu mungkin mengalami plateau di {exercise}\n\n1RM has not increased in 3 sessions.")
    else:
        messagebox.showinfo("Info", f"Tidak ada plateau yang terdeteksi {exercise}.")
