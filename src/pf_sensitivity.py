import math
import pandas as pd
from pathlib import Path


# -----------------------------------
# Project paths
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

LOAD_FILE = BASE_DIR / "data" / "loads.csv"


# -----------------------------------
# Read load data
# -----------------------------------

loads = pd.read_csv(LOAD_FILE)


# -----------------------------------
# Calculate total P and Q
# -----------------------------------

total_p = 0
total_q = 0

for _, row in loads.iterrows():

    p = row["p_kw"]

    pf = row["pf"]

    phi = math.acos(pf)

    q = p * math.tan(phi)

    total_p += p

    total_q += q


# -----------------------------------
# Original apparent power
# -----------------------------------

original_s = math.sqrt(
    total_p**2 +
    total_q**2
)


# -----------------------------------
# Target PF values
# -----------------------------------

target_pfs = [
    0.90,
    0.92,
    0.95,
    0.97,
    0.98,
    1.00
]


results = []


# -----------------------------------
# Sensitivity analysis
# -----------------------------------

for target_pf in target_pfs:

    target_phi = math.acos(target_pf)

    capacitor_kvar = (
        total_p *
        (
            math.tan(math.acos(
                total_p / original_s
            ))
            -
            math.tan(target_phi)
        )
    )

    new_q = total_q - capacitor_kvar

    new_s = math.sqrt(
        total_p**2 +
        new_q**2
    )

    results.append({
        "Target PF": target_pf,
        "Required Capacitor (kVAR)": capacitor_kvar,
        "New Apparent Power (kVA)": new_s,
        "Loading (%)": new_s / 1000 * 100
    })


# -----------------------------------
# Create DataFrame
# -----------------------------------

results_df = pd.DataFrame(results)


print("\nPOWER FACTOR SENSITIVITY")
print("========================")

print(
    results_df.to_string(index=False)
)