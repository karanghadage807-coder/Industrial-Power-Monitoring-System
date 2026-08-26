import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# -----------------------------------
# Project paths
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "load_priority_results.csv"
OUTPUT_DIR = BASE_DIR / "results"

OUTPUT_DIR.mkdir(exist_ok=True)


# -----------------------------------
# Read priority results
# -----------------------------------

df = pd.read_csv(INPUT_FILE)


# -----------------------------------
# Plot 1: Reactive Power
# -----------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    df["Load"],
    df["Q_kVAR"]
)

plt.xlabel("Load")
plt.ylabel("Reactive Power (kVAR)")
plt.title("Reactive Power by Industrial Load")

plt.xticks(rotation=30)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "reactive_power_by_load.png",
    dpi=300
)

plt.show()


# -----------------------------------
# Plot 2: Power Factor
# -----------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    df["Load"],
    df["PF"]
)

plt.xlabel("Load")
plt.ylabel("Power Factor")
plt.title("Power Factor by Industrial Load")

plt.xticks(rotation=30)

plt.ylim(0, 1)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "power_factor_by_load.png",
    dpi=300
)

plt.show()


# -----------------------------------
# Plot 3: Priority Score
# -----------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    df["Load"],
    df["Priority_Score"]
)

plt.xlabel("Load")
plt.ylabel("Priority Score")
plt.title("Load Priority Score")

plt.xticks(rotation=30)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "load_priority_score.png",
    dpi=300
)

plt.show()


print("\n======================================")
print("LOAD PRIORITY VISUALIZATION COMPLETE")
print("======================================")

print("\nPlots saved in:")

print(OUTPUT_DIR)