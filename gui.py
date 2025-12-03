import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from workout_manager import WorkoutManager
from workout_entry import WorkoutEntry
from plotter import show_volume, show_1rm, show_fatigue, show_lpr, check_plateau


def start_ui():
    W, H = 1280, 720
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    mgr = WorkoutManager()
    mgr.init_csv()
    mgr.load()

    app = ctk.CTk()
    app.title("Gym Logbook")
    app.geometry(f"{W}x{H}")
    app.resizable(False, False)
    app.configure(fg_color="#0E141A")

    # buat panel
    L = ctk.CTkFrame(app, width=400, height=600, corner_radius=22, fg_color=("white", "gray12"))
    L.place(x=20, y=70)

    R = ctk.CTkFrame(app, width=600, height=600, corner_radius=22, fg_color=("white", "gray12"))
    R.place(x=430, y=70) 

    # panel kiri
    ctk.CTkLabel(L, text="Add Workout", font=("Segoe UI", 28, "bold")).pack(pady=(22, 12))

    # buat variabel string
    date_v = ctk.StringVar(value=date.today().isoformat())
    ex_v = ctk.StringVar()
    s_v = ctk.StringVar()
    r_v = ctk.StringVar()
    w_v = ctk.StringVar()
    n_v = ctk.StringVar()
    rir_v = ctk.StringVar()

    def create_field(parent, label, var, width=300):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(frame, text=label, font=("Segoe UI", 12)).pack(anchor="w", padx=15, pady=(8, 0))
        ctk.CTkEntry(frame, textvariable=var, width=width, height=32).pack(pady=(4, 0), padx=15, fill="x", expand=True)
        frame.pack(pady=8, padx=0, fill="x")

    create_field(L, "Date", date_v)
    create_field(L, "Exercise", ex_v)

    # sets, reps, weight fields
    lbl_frame = ctk.CTkFrame(L, fg_color="transparent")
    lbl_frame.pack(pady=(12, 2), padx=15, fill="x")
    for i in range(3):
        lbl_frame.grid_columnconfigure(i, weight=1)
    
    ctk.CTkLabel(lbl_frame, text="Sets", font=("Segoe UI", 13)).grid(row=0, column=0, sticky="ew", padx=(0, 6))
    ctk.CTkLabel(lbl_frame, text="Reps", font=("Segoe UI", 13)).grid(row=0, column=1, sticky="ew", padx=(0, 6))
    ctk.CTkLabel(lbl_frame, text="Weight", font=("Segoe UI", 13)).grid(row=0, column=2, sticky="ew")

    entry_frame = ctk.CTkFrame(L, fg_color="transparent")
    entry_frame.pack(pady=(2, 10), padx=15, fill="x")
    for i in range(3):
        entry_frame.grid_columnconfigure(i, weight=1)
    
    ctk.CTkEntry(entry_frame, textvariable=s_v, width=90, height=32).grid(row=0, column=0, padx=(0, 6), sticky="ew")
    ctk.CTkEntry(entry_frame, textvariable=r_v, width=90, height=32).grid(row=0, column=1, padx=(0, 6), sticky="ew")
    ctk.CTkEntry(entry_frame, textvariable=w_v, width=90, height=32).grid(row=0, column=2, sticky="ew")

    create_field(L, "RIR", rir_v)
    create_field(L, "Notes", n_v, width=350)

    def add_record():
        try:
            entry = WorkoutEntry(date_v.get(), ex_v.get(), s_v.get(), r_v.get(), w_v.get(), n_v.get(), rir_v.get())
        except Exception:
            messagebox.showerror("Error", "Invalid input")
            return

        is_pr = mgr.add(entry)
        refresh()
        if is_pr:
            messagebox.showinfo("PR!", f"New PR untuk {entry.ex}")

        if mgr.detect_plateau(entry.ex):
            messagebox.showwarning("Plateau Warning", f"Kamu mungkin mengalami plateau di {entry.ex}")

    def undo_record():
        if mgr.undo_last():
            refresh()

    # Action buttons
    ctk.CTkButton(L, text="Add Workout", width=200, height=40, font=("Segoe UI", 14), command=add_record).pack(pady=(12, 6), padx=15, fill="x")
    ctk.CTkButton(L, text="Undo", width=200, height=40, font=("Segoe UI", 14), command=undo_record).pack(pady=(0, 12), padx=15, fill="x")

    # history box
    ctk.CTkLabel(R, text="Workout History", font=("Segoe UI", 28, "bold")).pack(pady=(22, 13))

    ctrl = ctk.CTkFrame(R, fg_color="transparent")
    ctrl.pack(pady=(8, 10), padx=20, fill="x")

    flt = ctk.StringVar()

    filter_entry = ctk.CTkEntry(ctrl, textvariable=flt, placeholder_text="Filter by exercise", placeholder_text_color="white", width=300, height=36)
    filter_entry.grid(row=0, column=0, padx=(0, 12), sticky="ew")

    app.after(200, lambda: app.focus())
    ctrl.grid_columnconfigure(0, weight=1)

    buttons = [
        ("Volume", lambda: show_volume(mgr, flt.get()), 78),
        ("1RM", lambda: show_1rm(mgr, flt.get()), 60),
        ("Fatigue", lambda: show_fatigue(mgr, flt.get()), 78),
        ("LPR", lambda: show_lpr(mgr, flt.get()), 56),
        ("Plateau", lambda: check_plateau(mgr, flt.get()), 70),
    ]

    for i, (text, cmd, width) in enumerate(buttons, start=1):
        ctk.CTkButton(ctrl, text=text, width=width, height=34, font=("Segoe UI", 12), command=cmd).grid(row=0, column=i, padx=5)

    # container untuk tabel
    tv_container = tk.Frame(R, width=800, height=380, bg="#1f1f1f")

    tv_container.pack(padx=15, pady=(4, 12), fill="both", expand=True)
    tv_container.pack_propagate(False)

    # isi tabel
    cols = ("date", "exercise", "sets", "reps", "weight", "volume", "rir", "trend")
    tree = ttk.Treeview(tv_container, columns=cols, show="headings", height=18)

    # setup kolom
    col_config = {
        "exercise": (170, "w"),
        "volume": (90, "center"),
        "trend": (70, "center"),
    }
    for col in cols:
        tree.heading(col, text=col.capitalize())
        width, anchor = col_config.get(col, (90, "center"))
        tree.column(col, width=width, anchor=anchor)

    tree.pack(fill="both", expand=True, side="left")
    scrollbar = ttk.Scrollbar(tv_container, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    def refresh():
        tree.delete(*tree.get_children())
        mgr.load()
        for e in mgr.entries:
            vol = e.volume()
            prev = mgr.get_prev_entry(e.ex, e)
            if prev is None:
                trend = "–"
            else:
                trend = "▲" if vol > prev.volume() else "▼" if vol < prev.volume() else "➖"
            row = [e.d, e.ex, e.sets, e.reps, e.weight, vol, e.rir, trend]
            tree.insert("", "end", values=row)

    refresh()

    def delete_selected():
        sel = tree.selection()
        if not sel:
            return
        idx = tree.index(sel[0])
        mgr.delete(idx)
        refresh()

    # Delete button
    ctk.CTkButton(ctrl, text="Delete", width=70, height=34, font=("Segoe UI", 12), command=delete_selected).grid(row=0, column=len(buttons)+1, padx=6)

    app.mainloop()