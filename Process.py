# Libraries
import os

import pandas as pd


# Count the number of files in the target folder
def count_number(target_folder):
    try:
        file_count = sum(1 for entry in os.scandir(target_folder) if entry.is_file())
        print(f"Total de documentos: {file_count}")

    except FileNotFoundError:
        print(
            f"Error: Could not find the folder "
            f"'{target_folder}' relative to this notebook."
        )


target_folder = "Datos_disciplinas"
count_number(target_folder)


# Ramas y Disciplinas
def ramas_d():
    sports = []
    files = []

    print("Lista de deportes:")

    for file in os.listdir(target_folder):
        if file.endswith(".xlsx"):
            files.append(file)

            name = file.rsplit(".", 1)[0]
            sports.append(name)

            print(f"{len(sports)}: {name}")

    return sports, files


sports, files = ramas_d()


# Read the session number and sport
sport_name = input("Ingrese el nombre del deporte a procesar: ")

#Diccionario con sesiones filtradas o no
sesiones_finales = {}


# Function to process the selected file
def jump_count(df, sheet_name, matrix_trials):

    reprobados = matrix_trials[matrix_trials["Trials"] > 3]

    if reprobados.empty:
        print(
            f"Todos los participantes tienen un máximo de 3 intentos "
            f"en la sesión '{sheet_name}'."
        )
        return df

    else:
        print(f"Participantes con más de 3 intentos en la sesión '{sheet_name}':")

        print(reprobados)

        descartar = input("¿Desea descartar a estos participantes? (s/n): ")

        if descartar.lower() == "s":
            # Filtrar/eliminar participantes
            df = df[~df["Athlete"].isin(reprobados["Athlete"])]

            print(f"Participantes descartados: {reprobados['Athlete'].tolist()}")

            return df

        else:
            print("No se han descartado a los participantes.")
            return df


def main():

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

        # Iterar sobre las hojas del archivo Excel disponibles
        for sheet_name in sheet_names:
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name, header=8)

                matrix_trials = df["Athlete"].value_counts().reset_index()

                #Matriz de repeticiones
                matrix_trials.columns = ["Athlete", "Trials"]

                df = jump_count(df, sheet_name, matrix_trials)

                #Se guarda el DataFrame filtrado en el diccionario de sesiones finales
                sesiones_finales[sheet_name] = df

            except Exception as e:
                print(f"  Error al procesar la hoja '{sheet_name}': {e}")

    else:
        print("Deporte no encontrado.")


if __name__ == "__main__":
    main()
