import math
import pandas as pd
from pathlib import Path


# -----------------------------------
# Project paths
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

LOAD_FILE = BASE_DIR / "data" / "loads.csv"
CAPACITOR_FILE = BASE_DIR / "data" / "capacitor_bank.csv"


# -----------------------------------
# Read load data
# -----------------------------------

loads = pd.read_csv(LOAD_FILE)


# -----------------------------------
# Read capacitor-bank configuration
# -----------------------------------

capacitor_data = pd.read_csv(CAPACITOR_FILE)


def get_config_value(parameter):
    return float(
        capacitor_data.loc[
            capacitor_data["parameter"] == parameter,
            "value"
        ].iloc[0]
    )


target_pf = get_config_value("target_pf")

capacitor_step_kvar = get_config_value(
    "capacitor_step_kvar"
)

max_bank_kvar = get_config_value(
    "max_bank_kvar"
)


# -----------------------------------
# Calculate total P and Q
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
# Calculate required capacitor kVAR
# -----------------------------------

phi_initial = math.acos(
    original_pf
)

phi_target = math.acos(
    target_pf
)

required_qc_kvar = (
    total_p_kw *
    (
        math.tan(phi_initial)
        -
        math.tan(phi_target)
    )
)


# -----------------------------------
# Select smallest practical capacitor
# bank that achieves target PF
#
# Assumption:
# Capacitor bank is modeled using
# uniform 25-kVAR switching steps.
# -----------------------------------

selected_qc_kvar = None

for qc in range(
    int(capacitor_step_kvar),
    int(max_bank_kvar) + 1,
    int(capacitor_step_kvar)
):

    test_q = total_q_kvar - qc

    test_s = math.sqrt(
        total_p_kw**2 +
        test_q**2
    )

    test_pf = (
        total_p_kw /
        test_s
    )

    if test_pf >= target_pf:

        selected_qc_kvar = qc

        break


# -----------------------------------
# Check whether target is achievable
# -----------------------------------

if selected_qc_kvar is None:

    raise ValueError(
        "Target PF cannot be achieved "
        "with the available capacitor bank."
    )


# -----------------------------------
# Check maximum available bank
# -----------------------------------

if selected_qc_kvar > max_bank_kvar:

    raise ValueError(
        "Required capacitor bank exceeds "
        "the maximum available capacity."
    )


# -----------------------------------
# Calculate overcompensation
# -----------------------------------

overcompensation_kvar = (
    selected_qc_kvar -
    required_qc_kvar
)


# -----------------------------------
# New reactive power
# -----------------------------------

new_q_kvar = (
    total_q_kvar -
    selected_qc_kvar
)


# -----------------------------------
# Determine PF condition
# -----------------------------------

if new_q_kvar > 0:

    compensation_status = "Lagging"

elif new_q_kvar < 0:

    compensation_status = "Leading"

else:

    compensation_status = "Unity PF"


# -----------------------------------
# New apparent power
# -----------------------------------

new_s_kva = math.sqrt(
    total_p_kw**2 +
    new_q_kvar**2
)


# -----------------------------------
# Actual achieved PF
# -----------------------------------

new_pf = (
    total_p_kw /
    new_s_kva
)


# -----------------------------------
# PF target check
# -----------------------------------

if new_pf >= target_pf:

    pf_status = "Target PF achieved"

else:

    pf_status = "Target PF not achieved"


# -----------------------------------
# Capacitor bank utilization
# -----------------------------------

capacitor_utilization = (
    selected_qc_kvar /
    max_bank_kvar
) * 100


# -----------------------------------
# System voltage
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
    f"{target_pf:.3f}"
)

print(
    f"Required Capacitor : "
    f"{required_qc_kvar:.2f} kVAR"
)

print(
    f"Selected Practical Capacitor : "
    f"{selected_qc_kvar:.2f} kVAR"
)

print(
    f"Overcompensation : "
    f"{overcompensation_kvar:.2f} kVAR"
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
    f"Actual Achieved PF : "
    f"{new_pf:.3f}"
)

print(
    f"Power Factor Condition : "
    f"{compensation_status}"
)

print(
    f"PF Status : "
    f"{pf_status}"
)

print(
    f"Capacitor Bank Utilization : "
    f"{capacitor_utilization:.2f}%"
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