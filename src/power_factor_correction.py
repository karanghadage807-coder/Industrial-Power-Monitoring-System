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
# Calculate total active and reactive power
# -----------------------------------

total_p_kw = 0
total_q_kvar = 0

for _, row in loads.iterrows():

    p = row["p_kw"]

    pf = row["pf"]

    phi = math.acos(pf)

    q = p * math.tan(phi)

    total_p_kw += p

    total_q_kvar += q


# -----------------------------------
# Original apparent power
# -----------------------------------

original_s_kva = math.sqrt(
    total_p_kw**2 +
    total_q_kvar**2
)


# -----------------------------------
# Original power factor
# -----------------------------------

original_pf = (
    total_p_kw /
    original_s_kva
)


# -----------------------------------
# Target power factor
# -----------------------------------

target_pf = 0.95


# -----------------------------------
# Calculate angles
# -----------------------------------

phi_initial = math.acos(original_pf)

phi_target = math.acos(target_pf)


# -----------------------------------
# Required capacitor kVAR
# -----------------------------------

required_qc_kvar = (
    total_p_kw *
    (
        math.tan(phi_initial)
        -
        math.tan(phi_target)
    )
)


# -----------------------------------
# Practical capacitor selection
# -----------------------------------

selected_qc_kvar = 125


# -----------------------------------
# New reactive power
# -----------------------------------

new_q_kvar = (
    total_q_kvar -
    selected_qc_kvar
)


# -----------------------------------
# New apparent power
# -----------------------------------

new_s_kva = math.sqrt(
    total_p_kw**2 +
    new_q_kvar**2
)


# -----------------------------------
# New power factor
# -----------------------------------

new_pf = (
    total_p_kw /
    new_s_kva
)


# -----------------------------------
# Voltage
# -----------------------------------

lv_voltage = 415


# -----------------------------------
# Current before correction
# -----------------------------------

current_before = (
    original_s_kva * 1000 /
    (math.sqrt(3) * lv_voltage)
)


# -----------------------------------
# Current after correction
# -----------------------------------

current_after = (
    new_s_kva * 1000 /
    (math.sqrt(3) * lv_voltage)
)


# -----------------------------------
# Current reduction
# -----------------------------------

current_reduction_percent = (
    (current_before - current_after)
    / current_before
) * 100


# -----------------------------------
# Transformer loading
# -----------------------------------

transformer_rating_kva = 1000


loading_before = (
    original_s_kva /
    transformer_rating_kva
) * 100


loading_after = (
    new_s_kva /
    transformer_rating_kva
) * 100


# -----------------------------------
# Display results
# -----------------------------------

print("\nPOWER FACTOR CORRECTION")
print("=======================")

print(
    f"Active Power : "
    f"{total_p_kw:.2f} kW"
)

print(
    f"Original Reactive Power : "
    f"{total_q_kvar:.2f} kVAR"
)

print(
    f"Original Apparent Power : "
    f"{original_s_kva:.2f} kVA"
)

print(
    f"Original Power Factor : "
    f"{original_pf:.3f}"
)

print(
    f"Target Power Factor : "
    f"{target_pf:.2f}"
)

print(
    f"Required Capacitor : "
    f"{required_qc_kvar:.2f} kVAR"
)

print(
    f"Selected Capacitor : "
    f"{selected_qc_kvar:.2f} kVAR"
)

print(
    f"New Reactive Power : "
    f"{new_q_kvar:.2f} kVAR"
)

print(
    f"New Apparent Power : "
    f"{new_s_kva:.2f} kVA"
)

print(
    f"New Power Factor : "
    f"{new_pf:.3f}"
)

print(
    f"\nCurrent Before Correction : "
    f"{current_before:.2f} A"
)

print(
    f"Current After Correction : "
    f"{current_after:.2f} A"
)

print(
    f"Current Reduction : "
    f"{current_reduction_percent:.2f}%"
)

print(
    f"\nTransformer Loading Before : "
    f"{loading_before:.2f}%"
)

print(
    f"Transformer Loading After : "
    f"{loading_after:.2f}%"
)