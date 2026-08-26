import pandas as pd
import math
from pathlib import Path


# ============================================================
# INDUSTRIAL POWER MONITORING SYSTEM
# Load-Wise Electrical Analysis
# ============================================================


# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

LOAD_FILE = BASE_DIR / "data" / "loads.csv"

OUTPUT_FILE = (
    BASE_DIR /
    "data" /
    "load_analysis_results.csv"
)


# ------------------------------------------------------------
# 2. Read load data
# ------------------------------------------------------------

loads = pd.read_csv(LOAD_FILE)


# ------------------------------------------------------------
# 3. Calculate load-wise electrical parameters
# ------------------------------------------------------------

results = []


for _, row in loads.iterrows():

    load_name = row["load_name"]

    p_kw = float(row["p_kw"])

    pf = float(row["pf"])

    voltage_v = float(row["voltage_v"])


    # --------------------------------------------------------
    # Phase angle
    # --------------------------------------------------------

    phi = math.acos(pf)

    phi_deg = math.degrees(phi)


    # --------------------------------------------------------
    # Reactive power
    # --------------------------------------------------------

    q_kvar = (
        p_kw *
        math.tan(phi)
    )


    # --------------------------------------------------------
    # Apparent power
    # --------------------------------------------------------

    s_kva = math.sqrt(
        p_kw**2 +
        q_kvar**2
    )


    # --------------------------------------------------------
    # Three-phase current
    # --------------------------------------------------------

    current_a = (
        p_kw * 1000 /
        (
            math.sqrt(3) *
            voltage_v *
            pf
        )
    )


    # --------------------------------------------------------
    # Power factor condition
    # --------------------------------------------------------

    if pf >= 0.95:

        pf_condition = "Good"

    elif pf >= 0.90:

        pf_condition = "Moderate"

    else:

        pf_condition = "Poor"


    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    results.append({

        "Load": load_name,

        "P_kW": p_kw,

        "Q_kVAR": q_kvar,

        "S_kVA": s_kva,

        "PF": pf,

        "Phase_Angle_deg": phi_deg,

        "Voltage_V": voltage_v,

        "Current_A": current_a,

        "PF_Condition": pf_condition
    })


# ------------------------------------------------------------
# 4. Create result DataFrame
# ------------------------------------------------------------

results_df = pd.DataFrame(results)


# ------------------------------------------------------------
# 5. Calculate system totals
# ------------------------------------------------------------

total_p = results_df["P_kW"].sum()

total_q = results_df["Q_kVAR"].sum()

total_s = math.sqrt(
    total_p**2 +
    total_q**2
)

overall_pf = (
    total_p /
    total_s
)


# ------------------------------------------------------------
# 6. Calculate load contribution
# ------------------------------------------------------------

results_df["P_Contribution_%"] = (
    results_df["P_kW"] /
    total_p *
    100
)


results_df["Q_Contribution_%"] = (
    results_df["Q_kVAR"] /
    total_q *
    100
)


# ------------------------------------------------------------
# 7. Round numerical values
# ------------------------------------------------------------

results_df["P_kW"] = (
    results_df["P_kW"].round(2)
)

results_df["Q_kVAR"] = (
    results_df["Q_kVAR"].round(2)
)

results_df["S_kVA"] = (
    results_df["S_kVA"].round(2)
)

results_df["PF"] = (
    results_df["PF"].round(3)
)

results_df["Phase_Angle_deg"] = (
    results_df["Phase_Angle_deg"].round(2)
)

results_df["Current_A"] = (
    results_df["Current_A"].round(2)
)

results_df["P_Contribution_%"] = (
    results_df["P_Contribution_%"].round(2)
)

results_df["Q_Contribution_%"] = (
    results_df["Q_Contribution_%"].round(2)
)


# ------------------------------------------------------------
# 8. Display load analysis
# ------------------------------------------------------------

print("\n")
print("=" * 70)
print("             INDUSTRIAL LOAD ANALYSIS")
print("=" * 70)


print(
    results_df.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 9. Display system totals
# ------------------------------------------------------------

print("\n")
print("=" * 70)
print("                    SYSTEM TOTALS")
print("=" * 70)


print(
    f"Total Active Power       : "
    f"{total_p:.2f} kW"
)


print(
    f"Total Reactive Power     : "
    f"{total_q:.2f} kVAR"
)


print(
    f"Total Apparent Power     : "
    f"{total_s:.2f} kVA"
)


print(
    f"Overall Power Factor     : "
    f"{overall_pf:.3f}"
)


# ------------------------------------------------------------
# 10. Identify important loads
# ------------------------------------------------------------

highest_p_load = results_df.loc[
    results_df["P_kW"].idxmax()
]


highest_q_load = results_df.loc[
    results_df["Q_kVAR"].idxmax()
]


lowest_pf_load = results_df.loc[
    results_df["PF"].idxmin()
]


print("\n")
print("=" * 70)
print("                 KEY LOAD FINDINGS")
print("=" * 70)


print(
    f"Highest Active Power Load : "
    f"{highest_p_load['Load']}"
)


print(
    f"Highest Reactive Power Load : "
    f"{highest_q_load['Load']}"
)


print(
    f"Lowest Power Factor Load : "
    f"{lowest_pf_load['Load']}"
)


# ------------------------------------------------------------
# 11. Count PF conditions
# ------------------------------------------------------------

good_count = (
    results_df["PF_Condition"]
    .eq("Good")
    .sum()
)


moderate_count = (
    results_df["PF_Condition"]
    .eq("Moderate")
    .sum()
)


poor_count = (
    results_df["PF_Condition"]
    .eq("Poor")
    .sum()
)


print("\n")
print("POWER FACTOR CONDITION SUMMARY")
print("------------------------------")


print(
    f"Good Loads      : {good_count}"
)


print(
    f"Moderate Loads  : {moderate_count}"
)


print(
    f"Poor Loads      : {poor_count}"
)


# ------------------------------------------------------------
# 12. Save results
# ------------------------------------------------------------

results_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n")
print(
    "Load analysis results saved to:"
)


print(
    OUTPUT_FILE
)