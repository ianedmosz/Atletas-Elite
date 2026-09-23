# Libraries
import os
import traceback

from numpy._core.umath import true_divide
import pandas as pd
from pandasgui import show


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
sport_input = input("Ingrese el numero del deporte a procesar: ")

# Diccionario con sesiones filtradas o no
sesiones_finales = {}


def jump_count(df, sheet_name):
    # DataFrame temporal para acumular los cambios
    df_tmp = df.copy()

    columnas_base = [
        "Athlete",
        "Test Type",
        "Trial",
        "Jump Height (Imp-Mom) [cm]",
        "Concentric Impulse (Left) [N s]",
        "Concentric Impulse (Right) [N s]",
        "Concentric RFD (Left) [N/s]",
        "Concentric RFD (Right) [N/s]",
        "Eccentric Braking RFD (Left) [N/s]",
        "Eccentric Braking RFD (Right) [N/s]",
        "RSI-modified (Imp-Mom) [m/s]",
        "Takeoff Peak Force (Right) [N]",
        "Takeoff Peak Force (Left) [N]",
        "Concentric Time to Peak Force (Left) [ms]",
        "Concentric Time to Peak Force (Right) [ms]",
        "Force at Peak Power (Left) [N]",
        "Force at Peak Power (Right) [N]",
        "Peak Landing Force (Left) [N]",
        "Peak Landing Force (Right) [N]",
        "Landing RFD (Right) [N/s]",
        "Landing RFD (Left) [N/s]",
        "Concentric Peak Force (Left) [N]",
        "Concentric Peak Force (Right) [N]",
        "Eccentric Peak Force (Left) [N]",
        "Eccentric Peak Force (Right) [N]",
    ]

    cols_mostrar = [col for col in columnas_base if col in df_tmp.columns]

    while True:
        matrix_trials = df_tmp["Athlete"].value_counts().reset_index()
        matrix_trials.columns = ["Athlete", "Trials"]
        #Tabla de los que no cumplieron
        reprobados = matrix_trials[matrix_trials["Trials"] != 3]

        if reprobados.empty:
            print(
                f"No hay atletas con un número de intentos distinto de 3 "
                f"en la sesión '{sheet_name}'."
            )
            return df_tmp

        df_reprobados = df_tmp.loc[
            df_tmp["Athlete"].isin(reprobados["Athlete"]),
            cols_mostrar,
        ].sort_values("Athlete")

        print(f"Sesión '{sheet_name}': revisa las tablas y cierra la ventana.")

        show(
            Conteo=reprobados.copy(),
            Saltos=df_reprobados.copy(),
            settings={"block": True},
        )

        while True:
            accion = input(
                "\n¿Qué quieres hacer?\n"
                "  [1] Eliminar a todos los atletas de la lista\n"
                "  [2] Revisar y eliminar a un atleta específico\n"
                "  [3] Terminar sin eliminar más atletas\n"
                "Opción: "
            ).strip()

            if accion in ("1", "2", "3"):
                break

            print("Introduce 1, 2 o 3.")

        if accion == "1":
            df_tmp = df_tmp.loc[
                ~df_tmp["Athlete"].isin(reprobados["Athlete"])
            ].copy()

            print("Se eliminaron los atletas de la lista de esta sesión.")
            return df_tmp

        elif accion == "3":
            return df_tmp

        # Opción 2: elegir un atleta de la lista actual
        while True:
            atleta_a_borrar = input(
                "Escribe el nombre exacto del atleta: "
            ).strip()

            if atleta_a_borrar == "":
                return df_tmp

            if atleta_a_borrar in reprobados["Athlete"].values:
                break

            print("El nombre no está en la lista. Ingresa un nombre válido.")

        # Mostrar únicamente los saltos del atleta elegido
        saltos_atleta = df_tmp.loc[
            df_tmp["Athlete"] == atleta_a_borrar,
            cols_mostrar,
        ]

        print(f"Revisa los saltos de '{atleta_a_borrar}' y cierra la ventana.")

        show(
            Saltos=saltos_atleta.copy(),
            settings={"block": True},
        )

        while True:
            confirmar = input(
                f"¿Eliminar a '{atleta_a_borrar}' con todos sus intentos? (s/n): "
            ).strip().lower()

            if confirmar in ("s", "si", "sí", "n", "no"):
                break

            print("Introduce s o n.")

        if confirmar in ("s", "si", "sí"):
            df_tmp = df_tmp.loc[
                df_tmp["Athlete"] != atleta_a_borrar
            ].copy()

            print(f"Se eliminó a '{atleta_a_borrar}' de esta sesión.")
        else:
            print(f"No se eliminó a '{atleta_a_borrar}'.")

        # Comprobar si quedan atletas por revisar
        conteo_restante = df_tmp["Athlete"].value_counts()

        if not (conteo_restante != 3).any():
            print("No quedan atletas con un número de intentos distinto de 3.")
            return df_tmp

        while True:
            continuar = input(
                "¿Quieres seguir revisando atletas? (s/n): "
            ).strip().lower()

            if continuar in ("s", "si", "sí", "n", "no"):
                break

            print("Introduce s o n.")

        if continuar in ("n", "no"):
            return df_tmp


def main():

    sport_index = int(sport_input) - 1

    if 0 <= sport_index < len(files):
        selected_file = files[sport_index]

        # Cargar el archivo Excel
        file_path = os.path.join(target_folder, selected_file)

        xl = pd.ExcelFile(file_path)
        sheet_names = xl.sheet_names

        print(f"Sesiones: {sheet_names}")

        # Iterar sobre las hojas del archivo Excel disponibles
        for sheet_name in sheet_names:
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name, header=8)

                df = jump_count(df, sheet_name)

                # Se guarda el DataFrame filtrado en el diccionario de sesiones finales
                sesiones_finales[sheet_name] = df

            except Exception as e:
                print(f"  Error al procesar la hoja '{sheet_name}': {e}")
                traceback.print_exc()

    else:
        print("Deporte no encontrado.")


if __name__ == "__main__":
    main()
