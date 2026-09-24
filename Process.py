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

def preguntar_sn(mensaje):
    while True:
        r = input(mensaje).strip().lower()
        if r in ("s", "si", "sí"):
            return True
        if r in ("n", "no"):
            return False
        print("Introduce s o n.")

def pedir_nombres(validos):
    while True:
        texto = input(
            "Nombres exactos separados por comas: "
        )
        #Separar nombres
        nombres = [n.strip() for n in texto.split(",") if n.strip()]
        if not nombres:
            return None
        no_existen = [n for n in nombres if n not in validos]
        if not no_existen:
            return nombres
        print("No están en la lista:", ", ".join(no_existen))

def pedir_saltos(validos):
    while True:
        texto = input(
            "Números de los saltos a eliminar, separados por comas "
            "(Enter para cancelar): "
        )
        # Separar numeros
        partes = [p.strip() for p in texto.split(",") if p.strip()]
        if not partes:
            return None
        try:
            numeros = [int(p) for p in partes]
        except ValueError:
            print("Solo se permiten números enteros.")
            continue
        invalidos = [n for n in numeros if n not in validos]
        if not invalidos:
            return numeros
        print("No pertenecen a los atletas seleccionados:", invalidos)

def jump_count(df, sheet_name):
    # DataFrame temporal para acumular los cambios
    df_tmp = df.copy()

    if not df_tmp.index.is_unique:
        df_tmp = df_tmp.reset_index(drop=True)

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
        # 1. Contar saltos por atleta
        conteo = df_tmp["Athlete"].value_counts().reset_index()
        conteo.columns = ["Athlete", "Trials"]
        reprobados = conteo[conteo["Trials"] != 3]

        if reprobados.empty:
            print(f"No hay atletas con un número de intentos distinto de 3 "
                  f"en la sesión '{sheet_name}'.")
            return df_tmp

        df_reprobados = df_tmp.loc[
            df_tmp["Athlete"].isin(reprobados["Athlete"]), cols_mostrar
        ].sort_values("Athlete")

        # 2. Tabla general (cierra la ventana para continuar)
        print(f"Sesión '{sheet_name}': revisa las tablas y cierra la ventana.")
        show(Conteo=reprobados.copy(), Saltos=df_reprobados.copy(),
             settings={"block": True})

        # 3. Menú
        while True:
            accion = input(
                "\n¿Qué quieres hacer?\n"
                "  [1] Eliminar a todos los atletas de la lista\n"
                "  [2] Revisar atletas específicos\n"
                "  [3] Terminar sin eliminar más\n"
                "Opción: "
            ).strip()
            if accion in ("1", "2", "3"):
                break
            print("Introduce 1, 2 o 3.")

        if accion == "1":
            df_tmp = df_tmp.loc[
                ~df_tmp["Athlete"].isin(reprobados["Athlete"])
            ].copy()
            print("Se eliminaron los atletas de la lista.")
            return df_tmp

        if accion == "3":
            return df_tmp

        # 4-5. Pedir y validar nombres (si alguno no existe, no se borra nada)
        nombres = pedir_nombres(set(reprobados["Athlete"]))
        if nombres is None:
            continue

        # 6. Tabla solo con los saltos de los atletas elegidos
        saltos = df_tmp.loc[df_tmp["Athlete"].isin(nombres), cols_mostrar]
        print("Revisa los saltos (el número es el índice de la primera "
              "columna) y cierra la ventana.")
        show(Saltos=saltos.copy(), settings={"block": True})

        # 7. Elegir saltos por número y validarlos
        numeros = pedir_saltos(set(saltos.index))
        if numeros is None:
            continue

        # 8. Confirmar
        print("\nSe eliminarán estos saltos:")
        print(df_tmp.loc[numeros, cols_mostrar[:3]])

        # 9. Eliminar solo esos saltos (los cambios se acumulan en df_tmp)
        if preguntar_sn(f"¿Eliminar {len(numeros)} salto(s)? (s/n): "):
            df_tmp = df_tmp.drop(index=numeros)
            print("Saltos eliminados.")
        else:
            print("No se eliminó nada.")

        # 10-12. ¿Continuar? Si sí, el while recalcula conteos y vuelve a mostrar
        if not preguntar_sn("¿Seguir revisando? (s/n): "):
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
