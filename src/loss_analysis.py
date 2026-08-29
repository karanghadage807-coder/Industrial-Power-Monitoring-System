import pandas as pd
import math
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "load_analysis_results.csv"
OUTPUT_FILE = BASE_DIR / "data" / "loss_analysis_results.csv"


# ============================================================
# SYSTEM PARAMETERS
# ============================================================

LV_VOLTAGE = 415
TRANSFORMER_RATING_KVA = 1000

# Equivalent feeder resistance per phase
# Assumed value for project-level loss analysis
FEEDER_RESISTANCE_OHM = 0.02

# PF correction selected for comparison
TARGET_PF = 0.95

# Practical capacitor-bank step
CAPACITOR_STEP_KVAR = 25

# Maximum capacitor-bank capacity
MAX_BANK_KVAR = 500


# ============================================================
# LOAD DATA
# ============================================================

load_data = pd.read_csv(INPUT_FILE)


# ============================================================
# SYSTEM TOTALS
# ============================================================

total_p = load_data["P_kW"].sum()
total_q = load_data["Q_kVAR"].sum()

total_s = math.sqrt(
    total_p**2 +
    total_q**2
)

original_pf = total_p / total_s


# ============================================================
# CURRENT BEFORE PF CORRECTION
# ============================================================

current_before = (
    total_s * 1000 /
    (
        math.sqrt(3) *
        LV_VOLTAGE
    )
)


# ============================================================
# PF CORRECTION CALCULATION
# ============================================================

if TARGET_PF <= original_pf:

    required_qc = 0
    selected_qc = 0

else:

    phi_initial = math.acos(original_pf)
    phi_target = math.acos(TARGET_PF)

    required_qc = total_p * (
        math.tan(phi_initial) -
        math.tan(phi_target)
    )

    selected_qc = None

    for qc in range(
        CAPACITOR_STEP_KVAR,
        MAX_BANK_KVAR + 1,
        CAPACITOR_STEP_KVAR
    ):

        test_q = total_q - qc

        test_s = math.sqrt(
            total_p**2 +
            test_q**2
        )

        test_pf = total_p / test_s

        if test_pf >= TARGET_PF:

            selected_qc = qc
            break


    if selected_qc is None:

        raise ValueError(
            "Target PF cannot be achieved "
            "with the available capacitor bank."
        )


# ============================================================
# SYSTEM PARAMETERS AFTER PF CORRECTION
# ============================================================

new_q = total_q - selected_qc

new_s = math.sqrt(
    total_p**2 +
    new_q**2
)

achieved_pf = total_p / new_s


# ============================================================
# CURRENT AFTER PF CORRECTION
# ============================================================

current_after = (
    new_s * 1000 /
    (
        math.sqrt(3) *
        LV_VOLTAGE
    )
)


# ============================================================
# COPPER LOSS CALCULATION
# ============================================================

# Three-phase copper loss:
#
# P_loss = 3 I^2 R
#
# Result is in watts.

loss_before_w = (
    3 *
    current_before**2 *
    FEEDER_RESISTANCE_OHM
)

loss_after_w = (
    3 *
    current_after**2 *
    FEEDER_RESISTANCE_OHM
)


# Convert watts to kW

loss_before_kw = loss_before_w / 1000
loss_after_kw = loss_after_w / 1000


# ============================================================
# LOSS REDUCTION
# ============================================================

loss_reduction_kw = (
    loss_before_kw -
    loss_after_kw
)

loss_reduction_percent = (
    loss_reduction_kw /
    loss_before_kw
) * 100


# ============================================================
# TRANSFORMER LOADING
# ============================================================

loading_before = (
    total_s /
    TRANSFORMER_RATING_KVA
) * 100

loading_after = (
    new_s /
    TRANSFORMER_RATING_KVA
) * 100


# ============================================================
# RESULT TABLE
# ============================================================

results = pd.DataFrame({

    "Parameter": [

        "Active Power",
        "Original Reactive Power",
        "Original Apparent Power",
        "Original Power Factor",
        "Target Power Factor",
        "Selected Capacitor",
        "New Reactive Power",
        "New Apparent Power",
        "Achieved Power Factor",
        "Current Before",
        "Current After",
        "Copper Loss Before",
        "Copper Loss After",
        "Loss Reduction",
        "Loss Reduction Percent",
        "Transformer Loading Before",
        "Transformer Loading After"
    ],

    "Value": [

        total_p,
        total_q,
        total_s,
        original_pf,
        TARGET_PF,
        selected_qc,
        new_q,
        new_s,
        achieved_pf,
        current_before,
        current_after,
        loss_before_kw,
        loss_after_kw,
        loss_reduction_kw,
        loss_reduction_percent,
        loading_before,
        loading_after
    ],

    "Unit": [

        "kW",
        "kVAR",
        "kVA",
        "",
        "",
        "kVAR",
        "kVAR",
        "kVA",
        "",
        "A",
        "A",
        "kW",
        "kW",
        "kW",
        "%",
        "%",
        "%"
    ]
})


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 70)
print("                 SYSTEM LOSS ANALYSIS")
print("=" * 70)

print(
    f"\nActive Power                 : {total_p:.2f} kW"
)

print(
    f"Original Reactive Power     : {total_q:.2f} kVAR"
)

print(
    f"Original Apparent Power     : {total_s:.2f} kVA"
)

print(
    f"Original Power Factor       : {original_pf:.3f}"
)

print(
    f"\nTarget Power Factor         : {TARGET_PF:.2f}"
)

print(
    f"Selected Capacitor          : {selected_qc:.0f} kVAR"
)

print(
    f"Achieved Power Factor       : {achieved_pf:.3f}"
)


print("\n" + "-" * 70)
print("CURRENT ANALYSIS")
print("-" * 70)

print(
    f"Current Before Correction   : {current_before:.2f} A"
)

print(
    f"Current After Correction    : {current_after:.2f} A"
)


print("\n" + "-" * 70)
print("COPPER LOSS ANALYSIS")
print("-" * 70)

print(
    f"Copper Loss Before          : {loss_before_kw:.4f} kW"
)

print(
    f"Copper Loss After           : {loss_after_kw:.4f} kW"
)

print(
    f"Loss Reduction              : {loss_reduction_kw:.4f} kW"
)

print(
    f"Loss Reduction              : {loss_reduction_percent:.2f} %"
)


print("\n" + "-" * 70)
print("TRANSFORMER LOADING")
print("-" * 70)

print(
    f"Loading Before              : {loading_before:.2f} %"
)

print(
    f"Loading After               : {loading_after:.2f} %"
)


# ============================================================
# SAVE RESULTS
# ============================================================

results.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n" + "=" * 70)

print(
    "Loss analysis results saved to:"
)

print(OUTPUT_FILE)

print("=" * 70)