import pandas as pd


def extract_and_display_resource_info(df):
    """
    Extract, structure, and display the resource information from the DataFrame.

    Args:
    df (DataFrame): The DataFrame containing the Excel sheet data.
    """
    structured_data = {}
    current_resource = None

    for _, row in df.iterrows():
        resource = row['Ressource']
        intervenant = row['Intervenants']
        cm = row['CM']
        td = row['TD']
        tp_non_dedoubles = row['TP (non dédoublés)']
        tp_dedoubles = row['TP (dédoublés)']
        test = row['Test']

        # Check if new resource starts
        if pd.notna(resource):
            current_resource = resource
            structured_data[current_resource] = []

        # Check if row contains intervenant data
        if pd.notna(intervenant):
            structured_data[current_resource].append({
                'Intervenant': intervenant,
                'CM': cm,
                'TD': td,
                'TP (non dédoublés)': tp_non_dedoubles,
                'TP (dédoublés)': tp_dedoubles,
                'Test': test
            })

    # Display the structured data
    for resource, data in structured_data.items():
        print(f"### Ressource : {resource}")
        if data:
            for d in data:
                print(f"- **Intervenant : {d['Intervenant']}**")
                print(f"  - CM : {d['CM']} heure" if pd.notna(d['CM']) else "  - CM : Non spécifié")
                print(f"  - TD : {d['TD']} heure" if pd.notna(d['TD']) else "  - TD : Non spécifié")
                print(f"  - TP (non dédoublés) : {d['TP (non dédoublés)']} heure" if pd.notna(
                    d['TP (non dédoublés)']) else "  - TP (non dédoublés) : Non spécifié")
                print(f"  - TP (dédoublés) : {d['TP (dédoublés)']} heure" if pd.notna(
                    d['TP (dédoublés)']) else "  - TP (dédoublés) : Non spécifié")
                print(f"  - Test : {d['Test']} heure" if pd.notna(d['Test']) else "  - Test : Non spécifié")
        else:
            print("  Aucune donnée pour cette ressource pour le moment.")
        print("\n")


# Load the Excel file
file_path = 'QuiFaitQuoi_beta.xlsx'
excel_data = pd.ExcelFile(file_path)

# Display the sheet names and the first few rows of each sheet to understand the structure
sheet_names = excel_data.sheet_names
sheets_preview = {}

for sheet in sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    sheets_preview[sheet] = df.head()
df_s1 = pd.read_excel(file_path, sheet_name=sheet_names[0])

# Extract and display the resource information
extract_and_display_resource_info(df_s1)
