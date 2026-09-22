import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from pathlib import Path

BASE_DIR = Path(__file__).parent

# PLAYER STATS
player_xp = 0
player_level = 1
player_class = None
character_pil_image = None 
workout_log = [] 

_update_stats_callback = None

CLASSES = {
    "Knight": BASE_DIR / "assets" / "knight.png",
    "Mage":   BASE_DIR / "assets" / "mage.png",
    "Archer": BASE_DIR / "assets" / "archer.png",
    "Healer": BASE_DIR / "assets" / "healer.png",
}

# LEVEL SYSTEM
def check_level_up():
    global player_xp, player_level

    level_threshold = player_level * 100

    while player_xp >= level_threshold:
        player_xp -= level_threshold
        player_level += 1
        level_threshold = player_level * 100
        messagebox.showinfo("Level Up ⚔", f"You reached Level {player_level}!")

# ADD WORKOUT
def open_add_workout():
    workout_window = tk.Toplevel()
    workout_window.title("Add Workout")
    workout_window.geometry("400x400")
    workout_window.configure(bg="#1e1b2e")

    tk.Label(workout_window, text="⚔ Log Training ⚔",
             font=("Bookman Old Style", 16, "bold"),
             bg="#1e1b2e", fg="#d4af37").pack(pady=10)

    form_frame = tk.Frame(workout_window, bg="#1e1b2e")
    form_frame.pack(pady=10)

    # EXERCISE
    exercise_frame = tk.Frame(form_frame, bg="#1e1b2e")
    exercise_frame.pack(fill="x", pady=5)
    tk.Label(exercise_frame, text="Exercise:",
             width=15, anchor="w",
             bg="#1e1b2e", fg="#d4af37").pack(side="left")
    exercise_entry = tk.Entry(exercise_frame, bg="#2c2a3e", fg="white",
                              insertbackground="white")
    exercise_entry.pack(side="right", fill="x", expand=True)

    # WEIGHT
    weight_frame = tk.Frame(form_frame, bg="#1e1b2e")
    weight_frame.pack(fill="x", pady=5)
    tk.Label(weight_frame, text="Weight (lbs):",
             width=15, anchor="w",
             bg="#1e1b2e", fg="#d4af37").pack(side="left")
    weight_entry = tk.Entry(weight_frame, bg="#2c2a3e", fg="white",
                            insertbackground="white")
    weight_entry.pack(side="right", fill="x", expand=True)

    # REPS
    reps_frame = tk.Frame(form_frame, bg="#1e1b2e")
    reps_frame.pack(fill="x", pady=5)
    tk.Label(reps_frame, text="Reps:",
             width=15, anchor="w",
             bg="#1e1b2e", fg="#d4af37").pack(side="left")
    reps_entry = tk.Entry(reps_frame, bg="#2c2a3e", fg="white",
                          insertbackground="white")
    reps_entry.pack(side="right", fill="x", expand=True)

    def save_workout():
        global player_xp, player_level

        if not exercise_entry.get() or not weight_entry.get() or not reps_entry.get():
            messagebox.showerror("Error", "Fill all fields!")
            return

        try:
            weight = float(weight_entry.get())
            reps = int(reps_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Numbers only for weight and reps!")
            return

        xp = (reps * 2) + (weight * 0.5)
        player_xp += xp

        # Record the workout in the log
        workout_log.append({
            "exercise": exercise_entry.get().strip(),
            "weight": weight,
            "reps": reps,
            "xp": int(xp)
        })

        # Clear fields after saving
        exercise_entry.delete(0, tk.END)
        weight_entry.delete(0, tk.END)
        reps_entry.delete(0, tk.END)

        check_level_up()

        if _update_stats_callback is not None:
            _update_stats_callback()

        messagebox.showinfo("XP Gained", f"+{int(xp)} XP earned!")

    tk.Button(workout_window, text="Save Workout",
              command=save_workout,
              bg="#8b0000", fg="white").pack(pady=10)


# VIEW WORKOUT HISTORY
def open_workout_history():
    history_window = tk.Toplevel()
    history_window.title("Workout History")
    history_window.geometry("500x400")
    history_window.configure(bg="#1e1b2e")

    tk.Label(history_window, text="📜 Training Log 📜",
             font=("Bookman Old Style", 16, "bold"),
             bg="#1e1b2e", fg="#d4af37").pack(pady=10)

    if not workout_log:
        tk.Label(history_window, text="No workouts logged yet. Get training!",
                 bg="#1e1b2e", fg="white",
                 font=("Bookman Old Style", 11)).pack(pady=20)
        return

    # Scrollable frame using a canvas
    container = tk.Frame(history_window, bg="#1e1b2e")
    container.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(container, bg="#1e1b2e", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#1e1b2e")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Column headers
    header_frame = tk.Frame(scroll_frame, bg="#2c2a3e")
    header_frame.pack(fill="x", pady=(0, 4))
    for text, width in [("#", 4), ("Exercise", 20), ("Weight (lbs)", 12), ("Reps", 6), ("XP", 6)]:
        tk.Label(header_frame, text=text, width=width, anchor="w",
                 bg="#2c2a3e", fg="#d4af37",
                 font=("Bookman Old Style", 10, "bold")).pack(side="left", padx=4)

    # One row per workout
    for i, entry in enumerate(workout_log, start=1):
        row_bg = "#1e1b2e" if i % 2 == 0 else "#252338"
        row = tk.Frame(scroll_frame, bg=row_bg)
        row.pack(fill="x", pady=1)
        for text, width in [
            (str(i),               4),
            (entry["exercise"],   20),
            (str(entry["weight"]),12),
            (str(entry["reps"]),   6),
            (f"+{entry['xp']}",   6),
        ]:
            tk.Label(row, text=text, width=width, anchor="w",
                     bg=row_bg, fg="white",
                     font=("Bookman Old Style", 10)).pack(side="left", padx=4)

    # Totals row
    total_xp = sum(e["xp"] for e in workout_log)
    total_reps = sum(e["reps"] for e in workout_log)
    totals_frame = tk.Frame(history_window, bg="#2c2a3e")
    totals_frame.pack(fill="x", padx=10, pady=6)
    tk.Label(totals_frame,
             text=f"Total workouts: {len(workout_log)}   |   Total reps: {total_reps}   |   Total XP earned: {total_xp}",
             bg="#2c2a3e", fg="#d4af37",
             font=("Bookman Old Style", 10, "bold")).pack(pady=4)

# CLASS SELECTION
def choose_class():
    global player_class, character_pil_image

    class_window = tk.Toplevel()
    class_window.title("Choose Class")
    class_window.geometry("300x300")
    class_window.configure(bg="#1e1b2e")

    tk.Label(class_window, text="Choose Your Class ⚔",
             font=("Bookman Old Style", 16, "bold"),
             bg="#1e1b2e", fg="#d4af37").pack(pady=10)

    def select_class(cls):
        global player_class, character_pil_image

        player_class = cls

        
        try:
            img = Image.open(CLASSES[cls])
            try:
                img = img.resize((120, 120), Image.Resampling.LANCZOS)
            except AttributeError:
                img = img.resize((120, 120))
            character_pil_image = img
        except Exception as e:
            character_pil_image = None
            messagebox.showwarning(
                "Image Not Found",
                f"Could not load image for {cls}.\n\nExpected: {CLASSES[cls]}\n\nError: {e}"
            )

        class_window.destroy()
        open_main_app()

    for cls in CLASSES:
        tk.Button(class_window,
                  text=cls,
                  command=lambda c=cls: select_class(c),
                  bg="#8b0000", fg="white",
                  width=20).pack(pady=5)

# LOGIN WINDOW
window = tk.Tk()
window.title("Log-in")
window.geometry("400x300")
window.configure(bg="#1e1b2e")

def login():
    if username_entry.get() == "admin" and password_entry.get() == "1234":
        choose_class()
    else:
        messagebox.showerror("Login Failed", "Wrong credentials!")

tk.Label(window, text="⚔ Fitness Fantasy ⚔",
         font=("Bookman Old Style", 18, "bold"),
         bg="#1e1b2e", fg="#d4af37").pack(pady=15)

tk.Label(window, text="Username", bg="#1e1b2e", fg="#d4af37").pack()
username_entry = tk.Entry(window, bg="#2c2a3e", fg="white", insertbackground="white")
username_entry.pack(pady=5)

tk.Label(window, text="Password", bg="#1e1b2e", fg="#d4af37").pack()
password_entry = tk.Entry(window, show="*", bg="#2c2a3e", fg="white",
                          insertbackground="white")
password_entry.pack(pady=5)

tk.Button(window, text="Begin Adventure", command=login,
          bg="#8b0000", fg="white").pack(pady=15)

# MAIN APP
def open_main_app():
    global _update_stats_callback, character_pil_image

    window.destroy()

    app = tk.Tk()
    app.title("Fitness Fantasy")
    app.geometry("500x450")
    app.configure(bg="#1e1b2e")

    tk.Label(app, text="🏰 Fitness Fantasy 🏰",
             font=("Bookman Old Style", 18, "bold"),
             bg="#1e1b2e", fg="#d4af37").pack(pady=20)

    # CHARACTER DISPLAY
    if character_pil_image is not None:
        tk_image = ImageTk.PhotoImage(character_pil_image)
        character_label = tk.Label(app, image=tk_image, bg="#1e1b2e")
        character_label.image = tk_image  
    else:
        character_label = tk.Label(app, text=f"[ {player_class} ]",
                                   font=("Bookman Old Style", 14),
                                   bg="#1e1b2e", fg="white")

    character_label.pack(pady=10)

    stats_label = tk.Label(app,
                           text=f"Level: {player_level} | XP: {player_xp}",
                           bg="#1e1b2e", fg="white",
                           font=("Bookman Old Style", 11))
    stats_label.pack()

    xp_bar = ttk.Progressbar(app, length=300)
    xp_bar.pack(pady=10)

    def update_stats():
        stats_label.config(text=f"Level: {player_level} | XP: {int(player_xp)}")
        xp_bar["maximum"] = player_level * 100
        xp_bar["value"] = player_xp

    _update_stats_callback = update_stats

    update_stats()

    tk.Button(app, text="⚔ Add Workout ⚔",
              command=open_add_workout,
              bg="#8b0000", fg="white").pack(pady=10)

    tk.Button(app, text="📜 View Training Log",
              command=open_workout_history,
              bg="#4a3f6b", fg="white").pack(pady=5)

    tk.Button(app, text="Exit Realm",
              command=app.destroy,
              bg="#2c2a3e", fg="white").pack(pady=5)

    app.mainloop()

window.mainloop()