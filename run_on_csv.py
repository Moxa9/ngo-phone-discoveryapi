import pandas as pd
import requests
import time

# ===============================
# CONFIG
# ===============================
API_URL = "http://localhost:8081/discover-phone"
INPUT_CSV = "ngo-data-darpan-district-registration-city-and-field-of-work-wise-names-of-non-governmental-organization-ngos-in-telangana8.csv"
OUTPUT_CSV = "ngo_phone_results.csv"

# ===============================
# LOAD NGO FILE
# ===============================
df = pd.read_csv(INPUT_CSV)

results = []

print(f"Total NGOs found: {len(df)}")
print("Starting phone discovery...\n")

# ===============================
# LOOP THROUGH NGOs
# ===============================
for idx, row in df.iterrows():
    ngo_name = str(row.get("ngo_name", "")).strip()
    location = str(row.get("registered_district", "")).strip()
    email = str(row.get("ngo_email", "")).strip()

    if not ngo_name:
        continue

    payload = {
        "ngo_name": ngo_name,
        "location": location,
        "email": email if email else None
    }

    print(f"[{idx+1}] Searching: {ngo_name} ({location})")

    try:
        response = requests.post(API_URL, json=payload, timeout=25)
        data = response.json()
    except Exception as e:
        data = {
            "ngo_name": ngo_name,
            "phone": None,
            "confidence": 0.0,
            "source": None,
            "status": "error",
            "error": str(e)
        }

    results.append({
        "ngo_name": ngo_name,
        "district": location,
        "email": email,
        "phone": data.get("phone"),
        "confidence": data.get("confidence"),
        "source": data.get("source"),
        "status": data.get("status")
    })

    # VERY IMPORTANT: avoid blocking
    time.sleep(2)

# ===============================
# SAVE OUTPUT
# ===============================
out_df = pd.DataFrame(results)
out_df.to_csv(OUTPUT_CSV, index=False)

print("\nDONE ✅")
print(f"Results saved to: {OUTPUT_CSV}")
