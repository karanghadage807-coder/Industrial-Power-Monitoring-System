import pandas as pd
from pathlib import Path

# -----------------------------------
# Project directory
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "loads.csv"


# -----------------------------------
# Read data
# -----------------------------------

loads = pd.read_csv(DATA_FILE)


# -----------------------------------
# Calculate average operating power
# -----------------------------------

loads["average_power_kw"] = (
    loads["p_kw"] *
    loads["load_factor"]
)


# -----------------------------------
# Calculate daily energy
# -----------------------------------

loads["daily_energy_kwh"] = (
    loads["average_power_kw"] *
    loads["operating_hours"]
)


# -----------------------------------
# Calculate monthly energy
# -----------------------------------

loads["monthly_energy_kwh"] = (
    loads["daily_energy_kwh"] *
    30
)


# -----------------------------------
# Display results
# -----------------------------------

print("\nENERGY ANALYSIS")
print("================")

print(
    loads[
        [
            "load_name",
            "p_kw",
            "load_factor",
            "operating_hours",
            "average_power_kw",
            "daily_energy_kwh",
            "monthly_energy_kwh"
        ]
    ].to_string(index=False)
)


# -----------------------------------
# Total energy
# -----------------------------------

total_daily_energy = loads["daily_energy_kwh"].sum()

total_monthly_energy = loads["monthly_energy_kwh"].sum()


print("\nSYSTEM ENERGY")
print("=============")

print(
    f"Total Daily Energy : "
    f"{total_daily_energy:.2f} kWh"
)

print(
    f"Total Monthly Energy : "
    f"{total_monthly_energy:.2f} kWh"
)