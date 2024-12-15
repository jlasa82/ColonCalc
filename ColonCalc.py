
import tkinter as tk
from tkinter import messagebox
import sqlite3
import csv

# Crear o conectar a la base de datos
conn = sqlite3.connect("cancer_data.db")
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    edad INTEGER,
    sexo TEXT,
    antecedentes TEXT,
    edad_familiar TEXT,
    edad_diagnostico INTEGER,
    sintomas TEXT,
    feedback TEXT
)
""")
conn.commit()

# Función para almacenar datos en la base de datos
def save_to_database(firstName, edad, sexo, antFliar, edadFamiliar, edadDiagnostico, sintomas, feedback):
    cursor.execute("""
    INSERT INTO cases (first_name, edad, sexo, antecedentes, edad_familiar, edad_diagnostico, sintomas, feedback)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (firstName, edad, sexo, antFliar, edadFamiliar, edadDiagnostico, sintomas, feedback))
    conn.commit()

# Exportar base de datos a CSV
def export_to_csv():
    cursor.execute("SELECT * FROM cases")
    data = cursor.fetchall()
    with open("cancer_data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Nombre", "Edad", "Sexo", "Antecedentes", "Edad Familiar", "Edad Diagnóstico", "Síntomas", "Feedback"])
        writer.writerows(data)
    messagebox.showinfo("Exportación exitosa", "Los datos se han exportado a 'cancer_data.csv'.")

# Backend adaptado
def feedback_logic(firstName, edad, sexo, antFliar, edadFamiliar, edadDiagnostico, sintomas):
    if edad >= 50:
        return f"{firstName}, deberías consultar con tu médico para realizar algún estudio de pesquisa de cáncer de colon."
    elif 40 <= edad < 50 and antFliar == "Si" and edadFamiliar == "No":
        return f"{firstName}, deberías consultar con tu médico para realizar algún estudio de pesquisa de cáncer de colon."
    elif edad < 50 and sintomas == "Si":
        return f"{firstName}, deberías consultar con tu médico para realizar algún estudio endoscópico."
    elif edadFamiliar == "Si" and edad >= (edadDiagnostico - 10):
        return f"{firstName}, deberías consultar con tu médico para realizar algún estudio de pesquisa de cáncer de colon."
    else:
        return f"{firstName}, por el momento no está indicado que realices un estudio de pesquisa de cáncer de colon."

def update_familiar_age_options():
    if ant_fliar_var.get() == "Si":
        edad_familiar_frame.pack(pady=5, after=ant_fliar_frame)
    else:
        edad_familiar_frame.pack_forget()

def reset_form():
    first_name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    sexo_var.set("Selecciona")
    ant_fliar_var.set("Selecciona")
    edad_familiar_var.set("Selecciona")
    edad_diagnostico_entry.delete(0, tk.END)
    sintomas_var.set("Selecciona")
    result_label.config(text="")

def collect_data():
    firstName = first_name_entry.get()
    try:
        edad = int(age_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa una edad válida.")
        return

    sexo = sexo_var.get()
    if sexo not in ["Masculino", "Femenino"]:
        messagebox.showerror("Error", "Selecciona un sexo válido.")
        return

    antFliar = ant_fliar_var.get()
    edadFamiliar = edad_familiar_var.get()
    edadDiagnostico = None

    if antFliar == "Si":
        if edadFamiliar == "Si":
            try:
                edadDiagnostico = int(edad_diagnostico_entry.get())
                if edadDiagnostico <= 0:
                    messagebox.showerror("Error", "Ingresa una edad válida para el diagnóstico.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa una edad válida para el diagnóstico.")
                return

    sintomas = sintomas_var.get()

    feedback = feedback_logic(firstName, edad, sexo, antFliar, edadFamiliar, edadDiagnostico, sintomas)
    save_to_database(firstName, edad, sexo, antFliar, edadFamiliar, edadDiagnostico, sintomas, feedback)
    result_label.config(text=feedback)

    messagebox.showinfo("Resultado", feedback)
    reset_form()

# Frontend
root = tk.Tk()
root.title("Pesquisa de Cáncer Colorrectal")
root.configure(bg="white")

# Estilo
label_style = {"bg": "white", "fg": "darkblue", "font": ("Helvetica", 12)}
entry_style = {"font": ("Helvetica", 12)}

tk.Label(root, text="¿Cómo te llamas?", **label_style).pack(pady=5)
first_name_entry = tk.Entry(root, **entry_style)
first_name_entry.pack()

tk.Label(root, text="¿Cuál es tu edad?", **label_style).pack(pady=5)
age_entry = tk.Entry(root, **entry_style)
age_entry.pack()

tk.Label(root, text="Sexo al nacimiento:", **label_style).pack(pady=5)
sexo_var = tk.StringVar(value="Selecciona")
tk.Radiobutton(root, text="Masculino", variable=sexo_var, value="Masculino", **label_style).pack()
tk.Radiobutton(root, text="Femenino", variable=sexo_var, value="Femenino", **label_style).pack()

ant_fliar_frame = tk.Frame(root, bg="white")
tk.Label(ant_fliar_frame, text="¿Tienes antecedentes familiares de cáncer de colon?", **label_style).pack(pady=5)
ant_fliar_var = tk.StringVar(value="Selecciona")
tk.Radiobutton(ant_fliar_frame, text="Sí", variable=ant_fliar_var, value="Si", command=update_familiar_age_options, **label_style).pack()
tk.Radiobutton(ant_fliar_frame, text="No", variable=ant_fliar_var, value="No", command=update_familiar_age_options, **label_style).pack()
tk.Radiobutton(ant_fliar_frame, text="No sé", variable=ant_fliar_var, value="No se", command=update_familiar_age_options, **label_style).pack()
ant_fliar_frame.pack(pady=5)

edad_familiar_frame = tk.Frame(root, bg="white")
tk.Label(edad_familiar_frame, text="¿Conoces la edad al diagnóstico?", **label_style).pack()
edad_familiar_var = tk.StringVar(value="Selecciona")
tk.Radiobutton(edad_familiar_frame, text="Sí", variable=edad_familiar_var, value="Si", **label_style).pack()
tk.Radiobutton(edad_familiar_frame, text="No", variable=edad_familiar_var, value="No", **label_style).pack()
tk.Label(edad_familiar_frame, text="Si seleccionaste 'Sí', ingresa la edad:", **label_style).pack()
edad_diagnostico_entry = tk.Entry(edad_familiar_frame, **entry_style)
edad_diagnostico_entry.pack()

tk.Label(root, text="¿Presentas alguno de estos síntomas?", **label_style).pack(pady=5)
tk.Label(root, text="""1. Dolor abdominal
2. Sangrado con las heces
3. Pérdida de peso involuntaria
4. Anemia
5. Diarrea o cambio en el ritmo evacuatorio""", **label_style, justify="left").pack()
sintomas_var = tk.StringVar(value="Selecciona")
tk.Radiobutton(root, text="Sí", variable=sintomas_var, value="Si", **label_style).pack()
tk.Radiobutton(root, text="No", variable=sintomas_var, value="No", **label_style).pack()

tk.Button(root, text="Evaluar", command=collect_data, bg="darkblue", fg="white", font=("Helvetica", 12)).pack(pady=10)
tk.Button(root, text="Exportar Datos", command=export_to_csv, bg="green", fg="white", font=("Helvetica", 12)).pack(pady=10)

result_label = tk.Label(root, text="", wraplength=400, justify="center", bg="white", fg="darkblue", font=("Helvetica", 12))
result_label.pack(pady=20)

root.mainloop()
