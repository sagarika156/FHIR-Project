import pandas as pd
import json

# Load ONLY the "Observation" sheet from Excel
df = pd.read_excel("FHIR final questionnaire.xlsx", sheet_name="Observation")

# Create the base StructureDefinition for Observation
structure_definition = {
    "resourceType": "StructureDefinition",
    "url": "https://example.org/fhir/StructureDefinition/MyObservation",
    "name": "MyObservation",
    "status": "draft",
    "fhirVersion": "5.0.0",
    "kind": "resource",
    "abstract": False,
    "type": "Observation",
    "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
    "derivation": "constraint",
    "differential": {
        "element": []
    }
}

# Convert each Excel row into a FHIR element
for index, row in df.iterrows():
    path_raw = str(row["Element (Path)"]).strip()
    
    # Convert colon (:) into dot (.) to match FHIR path style
    path = path_raw.replace(":", ".")
    
    element = {
        "id": path,
        "path": path
    }

    # Add min/max from cardinality
    cardinality = str(row.get("Cardinality", "0..1")).strip()
    if '..' in cardinality:
        min_card, max_card = cardinality.split('..')
        element["min"] = int(min_card)
        element["max"] = max_card

    # Optional: include short description from Field Name
    if "Field Name" in row and pd.notna(row["Field Name"]):
        element["short"] = str(row["Field Name"]).strip()

    # Optional: add Data Type (for readability or documentation)
    if "Data Type" in row and pd.notna(row["Data Type"]):
        element["type"] = [{"code": str(row["Data Type"]).strip()}]

    # Optional: include Fixed/Binding as comment or binding (simple format)
    if "Fixed/Binding" in row and pd.notna(row["Fixed/Binding"]):
        fixed = str(row["Fixed/Binding"]).strip()
        element["comment"] = f"Fixed/Binding: {fixed}"

    # Add the element to the profile
    structure_definition["differential"]["element"].append(element)

# Save the generated StructureDefinition
with open("ObservationProfile.json", "w") as f:
    json.dump(structure_definition, f, indent=2)

print("✅ ObservationProfile.json created successfully!")


