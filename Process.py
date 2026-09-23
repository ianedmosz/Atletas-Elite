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


# Function to process the selected file
"""

def jump_count(df, sheet_name):

    matrix_trials = df["Athlete"].value_counts().reset_index()

    #Matriz de repeticiones
    matrix_trials.columns = ["Athlete", "Trials"]

    reprobados = matrix_trials[
        (matrix_trials["Trials"] > 3) | (matrix_trials["Trials"] < 3)
    ]


    if reprobados.empty:
        print(
            f"Todos los participantes tienen un máximo de 3 intentos "
            f"en la sesión '{sheet_name}'."
        )
        return df

    else:
        print(f"Participantes con más de 3 intentos en la sesión '{sheet_name}':")

        #print(reprobados)
        #
        #Imprimir a los los  3> o <3 intentos
        print(df[df["Athlete"].isin(reprobados["Athlete"])])

        descartar = input("¿Desea descartar a estos participantes? (s/n): ")

        if descartar.lower() == "s":
            # Filtrar/eliminar participantes
            df = df[~df["Athlete"].isin(reprobados["Athlete"])]

            print(f"Participantes descartados: {reprobados['Athlete'].tolist()}")

            return df

        else:
            print("No se han descartado a los participantes.")
            return df

"""


# Contar intentos por atleta y filtrarlos en general
def jump_count(df, sheet_name):
    # Data Frame temporal para cambios
    df_tmp = df.copy()

    matrix_trials = df["Athlete"].value_counts().reset_index()
    matrix_trials.columns = ["Athlete", "Trials"]

    # Detectar atletas que no tienen exactamente 3 intentos
    reprobados = matrix_trials[matrix_trials["Trials"] != 3]

    if reprobados.empty:
        print(f"Todos los atletas de la sesión '{sheet_name}' tienen 3 intentos.")
        # Regresar sin cambios
        return df

    print(f"Atletas con más o menos de 3 intentos en la sesión '{sheet_name}'.")

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

    cols_mostrar = [col for col in columnas_base if col in df.columns]

    # DataFrame de atletas reprobados
    df_reprobados = df_tmp.loc[
        df_tmp["Athlete"].isin(reprobados["Athlete"]), cols_mostrar
    ].sort_values("Athlete")

    # Abrir las tablas y esperar hasta que se cierre la ventana
    print("Revisa las tablas y cierra la ventana para continuar.")
    show(
        Conteo=reprobados.copy(),
        Saltos=df_reprobados.copy(),
        settings={"block": True},
    )

    while True:
        accion = input(
            "\n¿Qué quieres hacer?\n"
            "  [1] Eliminar a todos los atletas de la lista en esta sesión\n"
            "  [2] Eliminar a un atleta específico de la lista\n"
            "  [3] No eliminar nada\n"
            "Opción: "
        ).strip()

        if accion == "1":

            df_tmp = df_tmp.loc[~df["Athlete"].isin(reprobados["Athlete"])].copy()
            print("Se eliminaron los atletas de la lista de esta sesión.")
            return df_tmp

        # Mantener esta seccion en loop hasta que el usuario ingrese un nombre válido
        elif accion == "2":
            while(True):
                atleta_a_borrar = input("Escribe el nombre del atleta a eliminar: ").strip()

                if atleta_a_borrar not in reprobados["Athlete"].values:
                    print("El nombre no está en la lista.")
                    print("Ingresa un nombre válido.")
                    continue

                # Aqui el problema radica de como sigo haciendo las ediciones
                df_tmp = df_tmp.loc[df_tmp["Athlete"] != atleta_a_borrar].copy()
                print(f"Se eliminó a '{atleta_a_borrar}' de esta sesión.")
                continuar = input("Continuar (s/n): ").lower()

                if continuar == "n" or continuar == "no":
                    df = df_tmp
                    break

                else:
                    continue

            break

    print("No se eliminó nada.")
    return df


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
