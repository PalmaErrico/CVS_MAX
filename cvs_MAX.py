#%% impostare max_time uguale al numero di righe del file 
import os
import pandas as pd

# Parametri
input_dir = r"C:\Users\Palma\Desktop\DOTTORATO\collaborazione_articoli\ECG_Dataset5\Dataset5"
output_csv = os.path.join(input_dir, "output.csv")
output_excel = os.path.join(input_dir, "output.xlsx")

window_size = 30000      # durata finestra in ms
step_size = 1000         # shift della finestra in ms

control_num_linesv1 = 700000 
control_num_linesv2 = 420000 
# Dati da inserire
data = []

# Scansione dei file
for file in os.listdir(input_dir):
    if file.endswith(".txt"):
        file_path = os.path.join(input_dir, file)
        with open(file_path, "r") as f:
            num_lines = sum(1 for _ in f)

        user = os.path.splitext(file)[0]  # "1.txt" -> "1"
        filename = file

        # Classifica la serie
        if num_lines >= control_num_linesv1:
            series = "v1"
            max_time = num_lines  # Usa il numero effettivo di righe come max_time
        elif num_lines <= control_num_linesv2:
            series = "v2"
            max_time = num_lines  # Usa il numero effettivo di righe come max_time
        else:
            series = "unknown"
            continue

        # Generazione finestre temporali
        start = 0
        while start + window_size <= max_time:
            end = start + window_size
            data.append({
                "filename": filename,
                "user": user,
                "series": series,
                "start_time": f"{start} ms",
                "end_time": f"{end} ms",
                "manual_class": "",
                "analytic_class": ""
            })
            start += step_size

# Salva CSV e Excel
df = pd.DataFrame(data)
df.to_csv(output_csv, index=False)
df.to_excel(output_excel, index=False)

print(f"✅ File generati:\n- {output_csv}\n- {output_excel}")
