import pandas as pd
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
# Read load analysis results
# -----------------------------------

results = pd.read_csv(RESULT_FILE)


# -----------------------------------
# Rank loads by reactive power
# -----------------------------------

results = results.sort_values(
    by="Q_kVAR",
    ascending=False
).reset_index(drop=True)


results["Reactive_Power_Rank"] = (
    results.index + 1
)


# -----------------------------------
# Identify PF priority
# -----------------------------------

results["PF_Priority"] = results["PF"].apply(
    lambda pf:
        "High"
        if pf < 0.90
        else
        (
            "Medium"
            if pf < 0.95
            else
            "Low"
        )
)


# -----------------------------------
# Create engineering priority score
# -----------------------------------

results["Priority_Score"] = (
    results["Q_kVAR"] *
    (1 - results["PF"])
)


# -----------------------------------
# Rank by priority score
# -----------------------------------

priority_results = results.sort_values(
    by="Priority_Score",
    ascending=False
).reset_index(drop=True)


priority_results["Overall_Rank"] = (
    priority_results.index + 1
)


# -----------------------------------
# Display results
# -----------------------------------

print("\n")
print("=" * 70)
print("             LOAD PRIORITY ANALYSIS")
print("=" * 70)

print(
    priority_results[
        [
            "Overall_Rank",
            "Load",
            "P_kW",
            "Q_kVAR",
            "PF",
            "PF_Priority",
            "Priority_Score"
        ]
    ].to_string(index=False)
)


# -----------------------------------
# Key engineering findings
# -----------------------------------

highest_q_load = priority_results.loc[
    priority_results["Q_kVAR"].idxmax(),
    "Load"
]

lowest_pf_load = priority_results.loc[
    priority_results["PF"].idxmin(),
    "Load"
]

highest_priority_load = priority_results.loc[
    0,
    "Load"
]


print("\n")
print("=" * 70)
print("                 KEY FINDINGS")
print("=" * 70)

print(
    f"Highest Reactive Power Load : "
    f"{highest_q_load}"
)

print(
    f"Lowest Power Factor Load    : "
    f"{lowest_pf_load}"
)

print(
    f"Highest Priority Load       : "
    f"{highest_priority_load}"
)


# -----------------------------------
# Save results
# -----------------------------------

OUTPUT_FILE = (
    BASE_DIR /
    "data" /
    "load_priority_results.csv"
)

priority_results.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n")
print(
    "Load priority results saved to:"
)

print(OUTPUT_FILE)