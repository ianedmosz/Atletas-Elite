# Things to do 
## Today: 25/09/2026

## Things

- [ ] Unir todos los datos en un solo csv como data frame general, agregar una columna de session 
- [ ]



import os
import pandas as pd
from IPython.display import display

# Your variables
target_folder = "Datos_disciplinas"
files = ["file1.xlsx", "file2.xlsx"]  # Your list of files
sports = ["Football", "Basketball"]  # Your matching list of sports

results = []

# Zip files and sports together so they match perfectly
for file_name, sport in zip(files, sports):
    file_path = os.path.join(target_folder, file_name)
    
    try:
        xl = pd.ExcelFile(file_path)
        
        # Loop through each sheet (session) in the file
        for sheet_name in xl.sheet_names:
            # Read only the sheet into a temporary DataFrame
            df_sheet = pd.read_csv(file_path) if file_name.endswith('.csv') else pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Check if the "athletes" column exists (case-insensitive check recommended)
            # Adjust 'athletes' if your actual column name is capitalized (e.g., 'Athletes')
            athlete_col = [col for col in df_sheet.columns if col.lower() == 'athletes']
            
            if athlete_col:
                # Count unique athletes ignoring missing/NaN values
                unique_count = df_sheet[athlete_col[0]].dropna().nunique()
            else:
                unique_count = "Column 'athletes' not found"
                
            results.append({
                "sport": sport,
                "sheet name": sheet_name,
                "number of athletes": unique_count
            })
            
    except Exception as e:
        results.append({
            "sport": sport,
            "sheet name": "Error reading file",
            "number of athletes": 0
        })

# Create the final requested DataFrame
df_athletes_summary = pd.DataFrame(results)
display(df_athletes_summary)




