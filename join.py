import os
import pandas as pd

target_folder = "Datos_disciplinas"


files = [f for f in os.listdir(target_folder) if f.endswith(".xlsx") and not f.startswith("~$")]


def read_file(file_name):
    
    route = os.path.join(target_folder,file_name)
    sheet = pd.read_excel(route,header=8,sheet_name=None)
    #Lista de df
    dfs = []

    for sheet_name, df in sheet.items():
            #Renombrar a Genero sin tilde
            df = df.rename(columns={"Género": "Genero"})
            #Agregar el nombre del sheet name
            df["Sesion"] = sheet_name
            df["File"] = file_name
            dfs.append(df)


    return dfs

todos = []
for f in files:
      todos.extend(read_file(f))


df_final = pd.concat(todos,ignore_index=True)


columnas_base = [
    "Forms ID",
    "C000 ID",
    "Athlete",
    "Date of Birth",
    "Genero",
    "Disciplina",
    "Test Type",
    "Test Date",
    "Body Weight [kg]",
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






df_final = df_final.reindex(columns=columnas_base + ["Sesion", "File"])
df_final.to_csv("df_final.csv", index=False, encoding="utf-8-sig")

print(df_final.columns.tolist())