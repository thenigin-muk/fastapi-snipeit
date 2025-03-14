# app/normalize_carrier.py
import pandas as pd
import json
import os
import tempfile

DATA_DIR = tempfile.gettempdir()
os.makedirs(DATA_DIR, exist_ok=True)

carrier_files = {
    "verizon.csv": "Verizon",
    "tmobile.csv": "T-Mobile",
    "att_phones.csv": "AT&T",
    "att_devices.csv": "AT&T"
}

column_mappings = {
    "verizon.csv": {
        "Device ID": "IMEI",
        "SIM ID": "SIM",
        "Mobile Number": "Phone Number",
        "Username": "Device Name",
        "Cost Center": "cost_center"
    },
    "tmobile.csv": {
        "DAC": "cost_center",
        "Device User": "Device Name",
        "Mobile Number": "Phone Number"
    },
    "att_phones.csv": {
        "Device IMEI": "IMEI",
        "SIM number (ICCID)": "SIM",
        "Wireless number": "Phone Number",
        "COST CENTER": "cost_center",
        "Wireless user name": "Device Name"
    },
    "att_devices.csv": {
        "IMEI": "IMEI",
        "ICCID": "SIM",
        "MSISDN": "Phone Number",
        "Customer": "cost_center",
        "Device ID": "Device Name",
        "IMEI Model": "model.name"
    }
}

required_columns = ["IMEI", "SIM", "Phone Number", "Device Name", "Carrier", "cost_center"]

def normalize_carrier_data(debug=False):
    cleaned_data = []

    for file, carrier in carrier_files.items():
        try:
            df = pd.read_csv(f"data/{file}", sep=",", dtype=str, skiprows=1 if "verizon" in file else 0)
            print(f"✅ Loaded {file}")
        except Exception as e:
            print(f"❌ Error loading {file}: {e}")
            continue

        df.columns = df.columns.str.strip()
        if file in column_mappings:
            df = df.rename(columns=column_mappings[file])
        df = df.loc[:, ~df.columns.duplicated()].copy()
        df["Carrier"] = carrier

        # Clean phone numbers (remove dots, spaces)
        if "Phone Number" in df.columns:
            df["Phone Number"] = df["Phone Number"].str.replace(r"[.\s]", "", regex=True)

        # Remove "IMEI:" and "SIM:" prefixes for T-Mobile
        if carrier == "T-Mobile":
            if "IMEI" in df.columns:
                df["IMEI"] = df["IMEI"].str.replace("IMEI:", "", regex=False)
            if "SIM" in df.columns:
                df["SIM"] = df["SIM"].str.replace("SIM:", "", regex=False)

        # Ensure all required columns exist
        for col in required_columns:
            if col not in df.columns:
                df[col] = "UNKNOWN"

        df = df[required_columns]
        df = df.apply(lambda x: x.str.replace("\t", "").str.strip() if x.dtype == "object" else x)
        df = df.reset_index(drop=True)
        cleaned_data.extend(df.to_dict(orient="records"))

    # Write to JSON for debugging
    if debug:
        with open(f"{DATA_DIR}/carrier_data.json", "w") as json_file:
            json.dump(cleaned_data, json_file, indent=4)
        print(f"✔ Debug JSON saved to {DATA_DIR}/carrier_data.json")

    return cleaned_data  # Store in-memory instead of always saving

