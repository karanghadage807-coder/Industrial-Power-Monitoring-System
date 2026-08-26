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
# Read input data
# -----------------------------------

loads = pd.read_csv(LOAD_FILE)

capacitor_data = pd.read_csv(CAPACITOR_FILE)


# -----------------------------------
# Read capacitor configuration
# -----------------------------------

def get_config_value(parameter):

    return float(
        capacitor_data.loc[
            capacitor_data["parameter"] == parameter,
            "value"
        ].iloc[0]
    )


capacitor_step_kvar = get_config_value(
    "capacitor_step_kvar"
)

max_bank_kvar = get_config_value(
    "max_bank_kvar"
)


# -----------------------------------
# System parameters
# -----------------------------------

lv_voltage = 415

transformer_rating_kva = 1000


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
# Function for PF sensitivity
# -----------------------------------

def calculate_pf_sensitivity(target_pf):

    # --------------------------------
    # Calculate required capacitor
    # --------------------------------

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


    # --------------------------------
    # Check whether correction is
    # actually required
    # --------------------------------

    if target_pf <= original_pf:

        current_a = (
            original_s_kva * 1000 /
            (
                math.sqrt(3) *
                lv_voltage
            )
        )

        transformer_loading = (
            original_s_kva /
            transformer_rating_kva
        ) * 100


        return {

            "target_pf": target_pf,

            "required_qc_kvar": 0.0,

            "selected_qc_kvar": 0.0,

            "overcompensation_kvar": 0.0,

            "achieved_pf": original_pf,

            "new_s_kva": original_s_kva,

            "current_a": current_a,

            "transformer_loading":
                transformer_loading,

            "status":
                "No correction required"
        }


    # --------------------------------
    # Select smallest practical
    # capacitor bank
    # --------------------------------

    selected_qc_kvar = None


    for qc in range(
        int(capacitor_step_kvar),
        int(max_bank_kvar) + 1,
        int(capacitor_step_kvar)
    ):

        test_q = (
            total_q_kvar -
            qc
        )

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


    # --------------------------------
    # Target cannot be achieved
    # --------------------------------

    if selected_qc_kvar is None:

        return {

            "target_pf": target_pf,

            "required_qc_kvar":
                required_qc_kvar,

            "selected_qc_kvar":
                None,

            "overcompensation_kvar":
                None,

            "achieved_pf":
                None,

            "new_s_kva":
                None,

            "current_a":
                None,

            "transformer_loading":
                None,

            "status":
                "Target not achievable"
        }


    # --------------------------------
    # Calculate overcompensation
    # --------------------------------

    overcompensation_kvar = (
        selected_qc_kvar -
        required_qc_kvar
    )


    # --------------------------------
    # New reactive power
    # --------------------------------

    new_q_kvar = (
        total_q_kvar -
        selected_qc_kvar
    )


    # --------------------------------
    # New apparent power
    # --------------------------------

    new_s_kva = math.sqrt(
        total_p_kw**2 +
        new_q_kvar**2
    )


    # --------------------------------
    # Actual achieved PF
    # --------------------------------

    achieved_pf = (
        total_p_kw /
        new_s_kva
    )


    # --------------------------------
    # Current after correction
    # --------------------------------

    current_a = (
        new_s_kva * 1000 /
        (
            math.sqrt(3) *
            lv_voltage
        )
    )


    # --------------------------------
    # Transformer loading
    # --------------------------------

    transformer_loading = (
        new_s_kva /
        transformer_rating_kva
    ) * 100


    # --------------------------------
    # PF status
    # --------------------------------

    if achieved_pf >= target_pf:

        status = "Target achieved"

    else:

        status = "Target not achieved"


    # --------------------------------
    # Return results
    # --------------------------------

    return {

        "target_pf":
            target_pf,

        "required_qc_kvar":
            required_qc_kvar,

        "selected_qc_kvar":
            selected_qc_kvar,

        "overcompensation_kvar":
            overcompensation_kvar,

        "achieved_pf":
            achieved_pf,

        "new_s_kva":
            new_s_kva,

        "current_a":
            current_a,

        "transformer_loading":
            transformer_loading,

        "status":
            status
    }


# -----------------------------------
# Target PF values
# -----------------------------------

target_pf_values = [
    0.90,
    0.92,
    0.94,
    0.95,
    0.96,
    0.97,
    0.98,
]


# -----------------------------------
# Run sensitivity analysis
# -----------------------------------

results = []


for target_pf in target_pf_values:

    result = calculate_pf_sensitivity(
        target_pf
    )

    results.append(result)


# -----------------------------------
# Convert results to DataFrame
# -----------------------------------

results_df = pd.DataFrame(results)


# -----------------------------------
# Display results
# -----------------------------------

print("\n")
print("POWER FACTOR SENSITIVITY ANALYSIS")
print("=================================")


print(
    f"\nOriginal Active Power : "
    f"{total_p_kw:.2f} kW"
)


print(
    f"Original Reactive Power : "
    f"{total_q_kvar:.2f} kVAR"
)


print(
    f"Original Power Factor : "
    f"{original_pf:.3f}"
)


print("\n")


print(
    results_df.to_string(
        index=False,
        formatters={

            "target_pf":
                "{:.5f}".format,

            "required_qc_kvar":
                lambda x:
                "N/A"
                if pd.isna(x)
                else f"{x:.2f}",

            "selected_qc_kvar":
                lambda x:
                "N/A"
                if pd.isna(x)
                else f"{x:.0f}",

            "overcompensation_kvar":
                lambda x:
                "N/A"
                if pd.isna(x)
                else f"{x:.2f}",

            "achieved_pf":
                lambda x:
                "N/A"
                if pd.isna(x)
                else f"{x:.5f}",

            "new_s_kva":
                lambda x:
                "N/A"
                if pd.isna(x)
                else f"{x:.2f}",

            "current_a":
                lambda x:
                "N/A"
                if pd.isna(x)
                else f"{x:.2f}",

            "transformer_loading":
                lambda x:
                "N/A"
                if pd.isna(x)
                else f"{x:.2f}%"
        }
    )
)


# -----------------------------------
# Save sensitivity results
# -----------------------------------

OUTPUT_FILE = (
    BASE_DIR /
    "data" /
    "pf_sensitivity_results.csv"
)


results_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n")


print(
    "Sensitivity results saved to:"
)


print(
    OUTPUT_FILE
)