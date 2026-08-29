import pandas as pd
import math
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

LOAD_FILE = BASE_DIR / "data" / "loads.csv"
OUTPUT_FILE = BASE_DIR / "data" / "loss_energy_analysis_results.csv"


# ============================================================
# SYSTEM PARAMETERS
# ============================================================

LV_VOLTAGE = 415
TARGET_PF = 0.95

# Equivalent feeder resistance used for copper-loss estimation
FEEDER_RESISTANCE_OHM = 0.036


# ============================================================
# READ LOAD DATA
# ============================================================

loads = pd.read_csv(LOAD_FILE)


# ============================================================
# LOAD-WISE ELECTRICAL CALCULATIONS
# ============================================================

results = []

for _, row in loads.iterrows():

    load_name = row["load_name"]

    p_kw = row["p_kw"]

    pf = row["pf"]

    operating_hours = row["operating_hours"]

    load_factor = row["load_factor"]

    # --------------------------------------------------------
    # Original reactive power
    # --------------------------------------------------------

    phi = math.acos(pf)

    q_kvar = (
        p_kw *
        math.tan(phi)
    )

    # --------------------------------------------------------
    # Original apparent power
    # --------------------------------------------------------

    s_kva = math.sqrt(
        p_kw**2 +
        q_kvar**2
    )

    # --------------------------------------------------------
    # Original current
    # --------------------------------------------------------

    current_before = (
        p_kw * 1000 /
        (
            math.sqrt(3) *
            LV_VOLTAGE *
            pf
        )
    )

    # --------------------------------------------------------
    # Copper loss before correction
    # --------------------------------------------------------

    copper_loss_before = (
        3 *
        current_before**2 *
        FEEDER_RESISTANCE_OHM
    ) / 1000

    # ========================================================
    # PF CORRECTION
    # ========================================================

    if TARGET_PF <= pf:

        required_qc = 0

        selected_qc = 0

        q_after = q_kvar

        achieved_pf = pf

    else:

        target_phi = math.acos(
            TARGET_PF
        )

        required_qc = (
            p_kw *
            (
                math.tan(phi) -
                math.tan(target_phi)
            )
        )

        # Practical capacitor selection
        selected_qc = (
            math.ceil(
                required_qc / 25
            ) * 25
        )

        q_after = (
            q_kvar -
            selected_qc
        )

        s_after = math.sqrt(
            p_kw**2 +
            q_after**2
        )

        achieved_pf = (
            p_kw /
            s_after
        )

    # --------------------------------------------------------
    # Current after correction
    # --------------------------------------------------------

    s_after = math.sqrt(
        p_kw**2 +
        q_after**2
    )

    current_after = (
        s_after * 1000 /
        (
            math.sqrt(3) *
            LV_VOLTAGE
        )
    )

    # --------------------------------------------------------
    # Copper loss after correction
    # --------------------------------------------------------

    copper_loss_after = (
        3 *
        current_after**2 *
        FEEDER_RESISTANCE_OHM
    ) / 1000

    # --------------------------------------------------------
    # Daily copper-loss energy
    # --------------------------------------------------------

    daily_loss_before = (
        copper_loss_before *
        operating_hours
    )

    daily_loss_after = (
        copper_loss_after *
        operating_hours
    )

    daily_loss_saving = (
        daily_loss_before -
        daily_loss_after
    )

    # --------------------------------------------------------
    # Monthly copper-loss energy
    # --------------------------------------------------------

    monthly_loss_before = (
        daily_loss_before *
        30
    )

    monthly_loss_after = (
        daily_loss_after *
        30
    )

    monthly_loss_saving = (
        daily_loss_saving *
        30
    )

    results.append({

        "Load": load_name,

        "P_kW": p_kw,

        "Load_Factor": load_factor,

        "Operating_Hours": operating_hours,

        "Original_PF": pf,

        "Required_Capacitor_kVAR": required_qc,

        "Selected_Capacitor_kVAR": selected_qc,

        "Achieved_PF": achieved_pf,

        "Current_Before_A": current_before,

        "Current_After_A": current_after,

        "Copper_Loss_Before_kW": copper_loss_before,

        "Copper_Loss_After_kW": copper_loss_after,

        "Daily_Loss_Before_kWh": daily_loss_before,

        "Daily_Loss_After_kWh": daily_loss_after,

        "Daily_Loss_Saving_kWh": daily_loss_saving,

        "Monthly_Loss_Before_kWh": monthly_loss_before,

        "Monthly_Loss_After_kWh": monthly_loss_after,

        "Monthly_Loss_Saving_kWh": monthly_loss_saving
    })


# ============================================================
# CREATE RESULT DATAFRAME
# ============================================================

results_df = pd.DataFrame(results)


# ============================================================
# SYSTEM TOTALS
# ============================================================

total_daily_loss_before = (
    results_df["Daily_Loss_Before_kWh"].sum()
)

total_daily_loss_after = (
    results_df["Daily_Loss_After_kWh"].sum()
)

total_daily_loss_saving = (
    results_df["Daily_Loss_Saving_kWh"].sum()
)

total_monthly_loss_before = (
    results_df["Monthly_Loss_Before_kWh"].sum()
)

total_monthly_loss_after = (
    results_df["Monthly_Loss_After_kWh"].sum()
)

total_monthly_loss_saving = (
    results_df["Monthly_Loss_Saving_kWh"].sum()
)


if total_monthly_loss_before > 0:

    loss_reduction_percent = (
        total_monthly_loss_saving /
        total_monthly_loss_before
    ) * 100

else:

    loss_reduction_percent = 0


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("             LOSS ENERGY ANALYSIS")
print("=" * 70)

print(
    f"\nTarget Power Factor : {TARGET_PF:.2f}"
)

print(
    f"\nDaily Copper Loss Before : "
    f"{total_daily_loss_before:.2f} kWh"
)

print(
    f"Daily Copper Loss After  : "
    f"{total_daily_loss_after:.2f} kWh"
)

print(
    f"Daily Energy Saving      : "
    f"{total_daily_loss_saving:.2f} kWh"
)

print(
    f"\nMonthly Copper Loss Before : "
    f"{total_monthly_loss_before:.2f} kWh"
)

print(
    f"Monthly Copper Loss After  : "
    f"{total_monthly_loss_after:.2f} kWh"
)

print(
    f"Monthly Energy Saving      : "
    f"{total_monthly_loss_saving:.2f} kWh"
)

print(
    f"Loss Reduction             : "
    f"{loss_reduction_percent:.2f} %"
)


# ============================================================
# SAVE RESULTS
# ============================================================

results_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n")
print("=" * 70)
print("Loss energy analysis results saved to:")
print(OUTPUT_FILE)
print("=" * 70)