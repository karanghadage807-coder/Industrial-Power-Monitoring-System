import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# -----------------------------------
# Project paths
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RESULT_FILE = (
    BASE_DIR /
    "data" /
    "load_analysis_results.csv"
)


# -----------------------------------
# Read analysis results
# -----------------------------------

results = pd.read_csv(RESULT_FILE)


# -----------------------------------
# Display available loads
# -----------------------------------

print("\nLOAD VISUALIZATION")
print("==================")

print(
    results[
        [
            "Load",
            "P_kW",
            "Q_kVAR",
            "S_kVA",
            "PF",
            "Current_A"
        ]
    ].to_string(index=False)
)


# -----------------------------------
# 1. Active Power by Load
# -----------------------------------

plt.figure()

plt.bar(
    results["Load"],
    results["P_kW"]
)

plt.xlabel("Load")

plt.ylabel("Active Power (kW)")

plt.title(
    "Active Power Consumption by Industrial Load"
)

plt.xticks(rotation=30)

plt.grid(axis="y")

plt.tight_layout()

plt.show()


# -----------------------------------
# 2. Reactive Power by Load
# -----------------------------------

plt.figure()

plt.bar(
    results["Load"],
    results["Q_kVAR"]
)

plt.xlabel("Load")

plt.ylabel("Reactive Power (kVAR)")

plt.title(
    "Reactive Power Consumption by Industrial Load"
)

plt.xticks(rotation=30)

plt.grid(axis="y")

plt.tight_layout()

plt.show()


# -----------------------------------
# 3. Power Factor by Load
# -----------------------------------

plt.figure()

plt.bar(
    results["Load"],
    results["PF"]
)

plt.axhline(
    0.95,
    linestyle="--",
    label="Target PF = 0.95"
)

plt.xlabel("Load")

plt.ylabel("Power Factor")

plt.title(
    "Power Factor Comparison of Industrial Loads"
)

plt.xticks(rotation=30)

plt.legend()

plt.grid(axis="y")

plt.tight_layout()

plt.show()


# -----------------------------------
# 4. Current by Load
# -----------------------------------

plt.figure()

plt.bar(
    results["Load"],
    results["Current_A"]
)

plt.xlabel("Load")

plt.ylabel("Current (A)")

plt.title(
    "Current Consumption by Industrial Load"
)

plt.xticks(rotation=30)

plt.grid(axis="y")

plt.tight_layout()

plt.show()


print("\nAll load analysis plots generated successfully.")