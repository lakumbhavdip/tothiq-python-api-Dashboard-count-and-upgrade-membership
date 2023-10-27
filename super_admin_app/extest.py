import pandas as pd
import json

# Specify the file paths
excel_file_path = "C:/Users/HP/Downloads/Translated Under Review-Tothiq-Web-Individual-Business-Users-panel-Labels-Tothiq-Team-10-08-2023 (1) (1).xlsx"  # Replace with the actual Excel file path
fixture_file_path = "data_fixture.json"  # Replace with the desired fixture file path

# Read specific columns from Excel file into a DataFrame
selected_columns = ["Label Name", "English Label", "Arbic Label"]  # Specify the columns you want
df = pd.read_excel(excel_file_path, usecols=selected_columns)

# Convert DataFrame to a list of dictionaries
data_dict = df.to_dict(orient='records')

# Write the data to a JSON fixture file
with open(fixture_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data_dict, json_file, indent=4, ensure_ascii=False)

print(f"Fixture file '{fixture_file_path}' created.")
