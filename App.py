#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import dash
import dash_bootstrap_components as dbc
import dash_table  # Tambahkan ini!
from dash.dependencies import Input, Output
import os

# Folder tempat file Excel berada
folder_path = "D:/Project/Petronas/20240402 - Petronas/Report-Oktober24/Petronas (oktober)/CSV"  # Ganti dengan path folder kamu

# Buat daftar file Excel dalam folder
file_list = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

# Buat dataframe kosong untuk menampung hasil penggabungan
combined_df = pd.DataFrame()

# Loop melalui setiap file dan gabungkan
for file in file_list:
    file_path = os.path.join(folder_path, file)
    df_all = pd.read_csv(file_path)  # Membaca file Excel
    df_all["Source File"] = file  # Tambahkan kolom nama file asal
    combined_df = pd.concat([combined_df, df_all], ignore_index=True)
    
    
df_all=combined_df

#Row Data
#df = pd.read_excel(r"C:\Users\User\Documents\Program\Tes - Copy.xlsx", engine="openpyxl", keep_default_na=False)
#Initial Value
df_Initial = pd.read_excel(r"C:\Users\User\Documents\Program\Initial values.xlsx", engine="openpyxl")
#Faktor Koreksi
df_FK = pd.read_excel(r"C:\Users\User\Documents\Program\Faktor Koreksi.xlsx", engine="openpyxl")

# Create a new DataFrame for filtered values
df_filter = pd.DataFrame()
df_filter["Time"] = df_all["Time"]  # Keep the Time column
df_filter["1524"] = None  # Initialize empty column
df_filter["1530"] = None
df_filter["1543"] = None
df_filter["1550"] = None
df_filter["1554"] = None
df_filter["1558"] = None
df_filter["1561"] = None
df_filter["1571"] = None

# Konversi semua kolom kecuali kolom pertama ke numerik
df_all.iloc[:, 1:] = df_all.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

# Iterasi kolom mulai dari indeks ke-1 (kolom ke-2)
for col in df_all.columns[1:]:
    df_filter["1524"] = df_filter["1524"].combine_first(df_all[col].where((df_all[col] >= 1523.5) & (df_all[col] <= 1525.5)))
    df_filter["1530"] = df_filter["1530"].combine_first(df_all[col].where((df_all[col] >= 1529.5) & (df_all[col] <= 1531.5)))
    df_filter["1543"] = df_filter["1543"].combine_first(df_all[col].where((df_all[col] >= 1542.5) & (df_all[col] <= 1544.5)))
    df_filter["1550"] = df_filter["1550"].combine_first(df_all[col].where((df_all[col] >= 1549.5) & (df_all[col] <= 1551.5)))
    df_filter["1554"] = df_filter["1554"].combine_first(df_all[col].where((df_all[col] >= 1553.5) & (df_all[col] <= 1555.5)))
    df_filter["1558"] = df_filter["1558"].combine_first(df_all[col].where((df_all[col] >= 1557.5) & (df_all[col] <= 1559.5)))
    df_filter["1561"] = df_filter["1561"].combine_first(df_all[col].where((df_all[col] >= 1560.5) & (df_all[col] <= 1561.5)))
    df_filter["1571"] = df_filter["1571"].combine_first(df_all[col].where((df_all[col] >= 1570.5) & (df_all[col] <= 1572.5)))

        
# HITUNG NILAI
# Hitung Sensor 1 (1524&1530)
#y = 14.8937770176x - 0.0254409157
Sensordelta1=(df_filter["1524"]-df_Initial.at[0,"1D_1524"])-(df_filter["1530"]-df_Initial.at[0,"1T_1530"])
Disp_sensor_1=Sensordelta1*14.8937770176-0.0254409157

# Hitung Sensor 2 (1554&1543)
#y = 12.40672510x + 0.23656772
Sensordelta2=(df_filter["1554"]-df_Initial.at[0,"2D_1554"])-(df_filter["1543"]-df_Initial.at[0,"2T_1543"])
Disp_sensor_2=Sensordelta2*12.40672510+0.23656772
# Hitung Sensor 2 (1554&1543)
#y = 16.4040172404x + 0.0655412363 (1554&1558)
Sensordelta3=(df_filter["1550"]-df_Initial.at[0,"3D_1550"])-(df_filter["1558"]-df_Initial.at[0,"3T_1558"])
Disp_sensor_3=Sensordelta3*16.4040172404+0.0655412363

#y = 15.5680068502x + 0.3431042233 (1561&1571)
Sensordelta4=(df_filter["1561"]-df_Initial.at[0,"4D_1561"])-(df_filter["1571"]-df_Initial.at[0,"4T_1571"])
Disp_sensor_4=Sensordelta3*16.4040172404+0.0655412363

# TABLE SENSOR (DISPLACEMENT)

# Create a new DataFrame for filtered values
df_Disp = pd.DataFrame()
df_Disp["Time"] = df_all["Time"]  # Keep the Time column
df_Disp["Sensor_1"] = None  # Initialize empty column
df_Disp["Sensor_2"] = None
df_Disp["Sensor_3"] = None
df_Disp["Sensor_4"] = None
for col in df_all.columns:
    if col != "Time":
        df_Disp["Sensor_1"]=Disp_sensor_1
        df_Disp["Sensor_2"]=Disp_sensor_2
        df_Disp["Sensor_3"]=Disp_sensor_3
        df_Disp["Sensor_4"]=Disp_sensor_4
        
        
        
#DASHBOAR
# Asumsikan df_Disp sudah ada di script utama sebelum menjalankan Dash
# df_Disp harus memiliki kolom: ["Time", "Sensor_1", "Sensor_2", "Sensor_3", "Sensor_4", "Sensor_5", "Sensor_6", "Sensor_7"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
from fastapi import FastAPI

app = FastAPI()

app.layout = dbc.Container([
    # Judul
    dbc.Row([
        dbc.Col(html.H1("Monitoring"), width=8),
    ], align="center"),

    html.Br(),

    # Tab untuk memilih alat monitoring
    dcc.Tabs(id="tabs-example", value="tab-1", children=[
        dcc.Tab(label="Inclinometer", value="tab-1", style={"fontSize": "20px", "padding": "15px"}),
        dcc.Tab(label="Extensometer", value="tab-2", style={"fontSize": "20px", "padding": "15px"}),
        dcc.Tab(label="Settlement Plate", value="tab-3", style={"fontSize": "20px", "padding": "15px"})
    ], className="mb-3"),

    html.Br(),

    # ROW untuk Grafik dan Tabel
    dbc.Row([
        dbc.Col(dcc.Graph(id="graph-output-1"), width=6),  # Grafik 1
        dbc.Col(dcc.Graph(id="graph-output-2"), width=6)   # Grafik 2
    ]),
    
    html.Br(),

    # Tabel Data
    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id="table-output",
            style_table={'width': '100%'},
            columns=[{"name": "Sensor", "id": "Sensor"}, {"name": "Value", "id": "Value"}]  # Nama kolom tabel
        ), width=12)
    ])
], fluid=True)

# Callback untuk memperbarui dua grafik dan tabel berdasarkan tab yang dipilih
@app.callback(
    [Output("graph-output-1", "figure"), Output("graph-output-2", "figure"), Output("table-output", "data")],
    [Input("tabs-example", "value")]
)
def update_content(tab_value):
    global df_Disp  # Pastikan df_Disp bisa diakses dari script utama

    # Default nilai untuk table_data
    table_data = []

    if tab_value == "tab-1":
        # Grafik untuk Inclinometer (Sensor 1 & Sensor 2)
        figure_1 = {
            "data": [
                go.Scatter(x=df_Disp["Time"], y=df_Disp["Sensor_1"], mode='lines+markers', name="Sensor 1"),
                go.Scatter(x=df_Disp["Time"], y=df_Disp["Sensor_2"], mode='lines+markers', name="Sensor 2"),
            ],
            "layout": go.Layout(title="Inclinometer Data (Sensor 1 & 2)", xaxis={'title': 'Time'}, yaxis={'title': 'Value'})
        }

        # Grafik kedua untuk Inclinometer (Sensor 6)
        figure_2 = {
            "data": [go.Scatter(x=df_Disp["Time"], y=df_Disp["Sensor_1"], mode='lines+markers', name="Sensor 6")],
            "layout": go.Layout(title="Inclinometer Data (Sensor 6)", xaxis={'title': 'Time'}, yaxis={'title': 'Value'})
        }

        # Data tabel
        table_data = [
            {"Sensor": "Sensor_1", "Value": df_Disp.iloc[-1]["Sensor_1"]},
            {"Sensor": "Sensor_2", "Value": df_Disp.iloc[-1]["Sensor_2"]},
            {"Sensor": "Sensor_1", "Value": df_Disp.iloc[-1]["Sensor_1"]}
        ]

    elif tab_value == "tab-2":  
        # Grafik pertama untuk Extensometer (Sensor 3)
        figure_1 = {
            "data": [go.Scatter(x=df_Disp["Time"], y=df_Disp["Sensor_3"], mode='lines+markers', name="Sensor 3")],
            "layout": go.Layout(title="Extensometer Data (Sensor 3)", xaxis={'title': 'Time'}, yaxis={'title': 'Value'})
        }

        # Grafik kedua untuk Extensometer (Sensor 5)
        figure_2 = {
            "data": [go.Scatter(x=df_Disp["Time"], y=df_Disp["Sensor_1"], mode='lines+markers', name="Sensor 5")],
            "layout": go.Layout(title="Extensometer Data (Sensor 5)", xaxis={'title': 'Time'}, yaxis={'title': 'Value'})
        }

        table_data = [
            {"Sensor": "Sensor_3", "Value": df_Disp.iloc[-1]["Sensor_3"]},
            {"Sensor": "Sensor_1", "Value": df_Disp.iloc[-1]["Sensor_1"]}
        ]
    
    elif tab_value == "tab-3":
        # Grafik pertama untuk Settlement Plate (Sensor 4)
        figure_1 = {
            "data": [go.Scatter(x=df_Disp["Time"], y=df_Disp["Sensor_4"], mode='lines+markers', name="Sensor 4")],
            "layout": go.Layout(title="Settlement Plate Data (Sensor 4)", xaxis={'title': 'Time'}, yaxis={'title': 'Value'})
        }

        # Grafik kedua untuk Settlement Plate (Sensor 7)
        figure_2 = {
            "data": [go.Scatter(x=df_Disp["Time"], y=df_Disp["Sensor_1"], mode='lines+markers', name="Sensor 7")],
            "layout": go.Layout(title="Settlement Plate Data (Sensor 7)", xaxis={'title': 'Time'}, yaxis={'title': 'Value'})
        }

        table_data = [
            {"Sensor": "Sensor_4", "Value": df_Disp.iloc[-1]["Sensor_4"]},
            {"Sensor": "Sensor_1", "Value": df_Disp.iloc[-1]["Sensor_1"]}
        ]

    return figure_1, figure_2, table_data

if __name__ == '__main__':
    app.run_server(debug=True, port=8065)




# In[ ]:




