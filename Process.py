# Libraries
import os

import pandas as pd

target_folder = "Datos_disciplinas"

# Count the number of files in the target folder

try:
    file_count = sum(1 for entry in os.scandir(target_folder) if entry.is_file())
    print(f"Total de documentos: {file_count}")

except FileNotFoundError:
    print(
        f"Error: Could not find the folder '{target_folder}' relative to this notebook."
    )


# Ramas y Diciplinas

sports = []
files = []
print("Lista de deportes:")
for n, file in enumerate(os.listdir(target_folder), 1):
    if file.endswith(".xlsx"):
        files.append(file)
        # print(f"File: {file}")
        name = file.rsplit(".", 1)[0]
        sports.append(name)
        print(f"{n}: {sports[n - 1]}")

# Read the session number and sport


sport_name = input("Ingrese el nombre del deporte a procesar: ")
selected_file = ""

if sport_name in sports:
    for i in range(len(sports)):
        if sports[i] == sport_name:
            selected_file = files[i]
            break

    # Cargar el archivo Excel
    file_path = os.path.join(target_folder, selected_file)
    xl = pd.ExcelFile(file_path)
    sheet_names = xl.sheet_names

    print(f"Sesiones: {sheet_names}")

    for sheet_name in sheet_names:
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=8)
            print(df.columns)
            participants = df["Athlete"].dropna().unique()

            matrix_trials = df["Athlete"].value_counts().reset_index()
            matrix_trials.columns = ["Athlete", "Trials"]
            reprobados = matrix_trials[matrix_trials["Trials"] < 3]

            if reprobados.empty:
                print(
                    f"Todos los participantes han realizado al menos 3 intentos en la sesión '{sheet_name}'."
                )
            else:
                print(
                    f"Participantes que no han realizado al menos 3 intentos en la sesión '{sheet_name}':"
                )
                print(reprobados)

        except Exception as e:
            print(f" -> Error al procesar la hoja '{sheet_name}': {e}")

else:
    print("Deporte no encontrado.")
