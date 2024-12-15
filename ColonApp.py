from flask import Flask, render_template, request
from ColonCalc import feedback_logic  # Asegúrate de importar tu lógica desde ColonCalc.py

# Define el objeto app
app = Flask(__name__)

# Ruta para el formulario
@app.route("/")
def home():
    return render_template("form.html")  # Muestra el formulario HTML

# Ruta para procesar los datos y mostrar el resultado
@app.route("/result", methods=["POST"])
def result():
    # Recibir datos del formulario
    firstName = request.form["firstName"]
    edad = int(request.form["edad"])
    sexo = request.form["sexo"]
    antFliar = request.form["antFliar"]

    # Manejar edad al diagnóstico del familiar
    edadFamiliar = request.form.get("edadDiagnostico", "").strip()
    if edadFamiliar.isdigit():
        edadDiagnostico = int(edadFamiliar)
    else:
        edadDiagnostico = None  # Si no hay valor, asignar None

    sintomas = request.form["sintomas"]

    # Generar feedback usando la lógica
    feedback = feedback_logic(firstName, edad, sexo, antFliar, "Si" if edadDiagnostico else "No", edadDiagnostico, sintomas)
    
    # Renderizar el resultado
    return render_template("result.html", feedback=feedback)

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
