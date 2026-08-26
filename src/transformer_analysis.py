import pandas as pd
import math
from pathlib import Path


# -----------------------------------
# Project paths
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

LOAD_FILE = BASE_DIR / "data" / "loads.csv"
TRANSFORMER_FILE = BASE_DIR / "data" / "transformer.csv"


# -----------------------------------
# Read data
# -----------------------------------

loads = pd.read_csv(LOAD_FILE)

transformer = pd.read_csv(
    TRANSFORMER_FILE
)


# -----------------------------------
# Transformer parameters
# -----------------------------------

rated_kva = float(
    transformer.loc[
        transformer["parameter"] == "rated_power_kva",
        "value"
    ].iloc[0]
)

primary_kv = float(
    transformer.loc[
        transformer["parameter"] == "primary_voltage_kv",
        "value"
    ].iloc[0]
)

secondary_v = float(
    transformer.loc[
        transformer["parameter"] == "secondary_voltage_v",
        "value"
    ].iloc[0]
)

core_loss_kw = float(
    transformer.loc[
        transformer["parameter"] == "core_loss_kw",
        "value"
    ].iloc[0]
)

copper_loss_rated_kw = float(
    transformer.loc[
        transformer["parameter"] == "copper_loss_rated_kw",
        "value"
    ].iloc[0]
)


# -----------------------------------
# Calculate load parameters
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
# Total apparent power
# -----------------------------------

total_s_kva = math.sqrt(
    total_p_kw**2 +
    total_q_kvar**2
)


# -----------------------------------
# Overall power factor
# -----------------------------------

overall_pf = (
    total_p_kw /
    total_s_kva
)


# -----------------------------------
# Transformer loading
# -----------------------------------

loading = (
    total_s_kva /
    rated_kva
)

loading_percent = loading * 100


# -----------------------------------
# Transformer currents
# -----------------------------------

lv_full_load_current = (
    rated_kva * 1000 /
    (math.sqrt(3) * secondary_v)
)

hv_full_load_current = (
    rated_kva * 1000 /
    (math.sqrt(3) * primary_kv * 1000)
)

lv_load_current = (
    total_s_kva * 1000 /
    (math.sqrt(3) * secondary_v)
)


# -----------------------------------
# Transformer copper loss
# -----------------------------------

copper_loss_kw = (
    loading**2 *
    copper_loss_rated_kw
)


# -----------------------------------
# Total transformer losses
# -----------------------------------

total_loss_kw = (
    core_loss_kw +
    copper_loss_kw
)


# -----------------------------------
# Transformer efficiency
# -----------------------------------

efficiency = (
    total_p_kw /
    (total_p_kw + total_loss_kw)
) * 100


# -----------------------------------
# Display results
# -----------------------------------

print("\nTRANSFORMER ANALYSIS")
print("====================")

print(
    f"Transformer Rating : "
    f"{rated_kva:.2f} kVA"
)

print(
    f"Total Active Power : "
    f"{total_p_kw:.2f} kW"
)

print(
    f"Total Reactive Power : "
    f"{total_q_kvar:.2f} kVAR"
)

print(
    f"Total Apparent Power : "
    f"{total_s_kva:.2f} kVA"
)

print(
    f"Overall Power Factor : "
    f"{overall_pf:.3f}"
)

print(
    f"Transformer Loading : "
    f"{loading_percent:.2f}%"
)

print(
    f"LV Full Load Current : "
    f"{lv_full_load_current:.2f} A"
)

print(
    f"HV Full Load Current : "
    f"{hv_full_load_current:.2f} A"
)

print(
    f"Actual LV Load Current : "
    f"{lv_load_current:.2f} A"
)

print(
    f"Copper Loss : "
    f"{copper_loss_kw:.2f} kW"
)

print(
    f"Core Loss : "
    f"{core_loss_kw:.2f} kW"
)

print(
    f"Total Transformer Loss : "
    f"{total_loss_kw:.2f} kW"
)

print(
    f"Transformer Efficiency : "
    f"{efficiency:.2f}%"
)

# -----------------------------------
# Transformer status
# -----------------------------------

if loading_percent < 70:

    status = "NORMAL - Low/Moderate Loading"

elif loading_percent < 90:

    status = "NORMAL - High Loading"

elif loading_percent <= 100:

    status = "WARNING - Near Rated Capacity"

else:

    status = "OVERLOADED - Immediate Attention Required"


print(
    f"\nTransformer Status : {status}"
)