import customtkinter as ctk
import re
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("700x500")
app.title("Cyber Password Checker")

# ---------------- WINDOW TITLE ---------------- #

title = ctk.CTkLabel(
    app,
    text="🔐 CYBER PASSWORD CHECKER",
    font=("Consolas", 28, "bold"),
    text_color="#00ff88"
)
title.pack(pady=20)

# ---------------- PASSWORD ENTRY ---------------- #

password_var = ctk.StringVar()

entry = ctk.CTkEntry(
    app,
    width=500,
    height=50,
    font=("Consolas", 18),
    placeholder_text="Enter your password...",
    show="*",
    textvariable=password_var
)
entry.pack(pady=20)

# ---------------- SHOW/HIDE ---------------- #

show_password = False

def toggle_password():
    global show_password

    if show_password:
        entry.configure(show="*")
        toggle_btn.configure(text="Show")
        show_password = False
    else:
        entry.configure(show="")
        toggle_btn.configure(text="Hide")
        show_password = True

toggle_btn = ctk.CTkButton(
    app,
    text="Show",
    width=100,
    command=toggle_password
)

toggle_btn.pack()

# ---------------- STRENGTH BAR ---------------- #

progress = ctk.CTkProgressBar(app, width=500, height=20)
progress.set(0)
progress.pack(pady=20)

strength_label = ctk.CTkLabel(
    app,
    text="Password Strength",
    font=("Consolas", 18)
)
strength_label.pack()

# ---------------- VALIDATION LABELS ---------------- #

validation_label = ctk.CTkLabel(
    app,
    text="",
    justify="left",
    font=("Consolas", 15),
    text_color="#00ff88"
)
validation_label.pack(pady=20)

# ---------------- CRACK TIME ---------------- #

crack_label = ctk.CTkLabel(
    app,
    text="",
    font=("Consolas", 16),
    text_color="orange"
)
crack_label.pack()

# ---------------- PASSWORD CHECK FUNCTION ---------------- #

def check_password(event=None):

    password = password_var.get()

    score = 0
    feedback = []

    # Length
    if len(password) >= 8:
        score += 1
        feedback.append("✅ Minimum 8 Characters")
    else:
        feedback.append("❌ Password Too Short")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
        feedback.append("✅ Uppercase Letter")

    else:
        feedback.append("❌ Missing Uppercase Letter")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
        feedback.append("✅ Lowercase Letter")

    else:
        feedback.append("❌ Missing Lowercase Letter")

    # Numbers
    if re.search(r"\d", password):
        score += 1
        feedback.append("✅ Number Included")

    else:
        feedback.append("❌ Missing Number")

    # Special Character
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
        feedback.append("✅ Special Character")

    else:
        feedback.append("❌ Missing Special Character")

    # Progress Bar
    progress.set(score / 5)

    # Strength Message
    if score <= 2:
        strength = "WEAK PASSWORD"
        color = "red"

    elif score == 3 or score == 4:
        strength = "MEDIUM PASSWORD"
        color = "yellow"

    else:
        strength = "STRONG PASSWORD"
        color = "#00ff88"

    strength_label.configure(
        text=f"Strength: {strength}",
        text_color=color
    )

    # Validation Text
    validation_label.configure(text="\n".join(feedback))

    # Crack Time Calculation
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"\d", password):
        charset += 10

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset += 32

    if charset > 0:
        combinations = charset ** len(password)

        guesses_per_second = 1_000_000_000

        seconds = combinations / guesses_per_second

        years = seconds / (60 * 60 * 24 * 365)

        if years < 1:
            crack_time = "Few Minutes to Crack"
        elif years < 100:
            crack_time = f"{int(years)} Years to Crack"
        else:
            crack_time = "Millions of Years to Crack"

        crack_label.configure(
            text=f"⏳ Estimated Crack Time: {crack_time}"
        )

entry.bind("<KeyRelease>", check_password)

# ---------------- FOOTER ---------------- #

footer = ctk.CTkLabel(
    app,
    text="Designed by Krrish Pawar",
    font=("Consolas", 14),
    text_color="gray"
)

footer.pack(side="bottom", pady=20)

app.mainloop()