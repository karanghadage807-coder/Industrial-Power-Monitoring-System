import streamlit as st
import pandas as pd
import math
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Industrial Power Monitoring System",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

LOAD_ANALYSIS_FILE = DATA_DIR / "load_analysis_results.csv"
PRIORITY_FILE = DATA_DIR / "load_priority_results.csv"
RECOMMENDATION_FILE = DATA_DIR / "load_recommendations.csv"
SENSITIVITY_FILE = DATA_DIR / "pf_sensitivity_results.csv"
ENERGY_FILE = DATA_DIR / "energy_analysis_results.csv"
LOSS_FILE = DATA_DIR / "loss_analysis_results.csv"
LOSS_ENERGY_FILE = DATA_DIR / "loss_energy_analysis_results.csv"
CAPACITOR_FILE = DATA_DIR / "capacitor_bank.csv"


# ============================================================
# SYSTEM PARAMETERS
# ============================================================

LV_VOLTAGE = 415
TRANSFORMER_RATING_KVA = 1000

DEFAULT_CAPACITOR_STEP_KVAR = 25
DEFAULT_MAX_BANK_KVAR = 500


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_csv(file_path):
    """
    Safely load a CSV file.
    Returns None if the file does not exist.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return None
    except Exception as error:
        st.warning(
            f"Could not read {file_path.name}: {error}"
        )
        return None


def get_loss_value(loss_df, parameter):
    """
    Extract a value from the Parameter-Value format
    used by loss_analysis_results.csv.
    """
    if loss_df is None:
        return None

    if "Parameter" not in loss_df.columns or "Value" not in loss_df.columns:
        return None

    row = loss_df[
        loss_df["Parameter"].astype(str).str.strip() == parameter
    ]

    if row.empty:
        return None

    try:
        return float(row.iloc[0]["Value"])
    except (ValueError, TypeError):
        return None


def safe_column_sum(df, column):
    """
    Safely calculate the sum of a dataframe column.
    """
    if df is None or column not in df.columns:
        return 0.0

    return float(df[column].sum())


# ============================================================
# LOAD DATA
# ============================================================

load_data = load_csv(LOAD_ANALYSIS_FILE)
priority_data = load_csv(PRIORITY_FILE)
recommendation_data = load_csv(RECOMMENDATION_FILE)
sensitivity_data = load_csv(SENSITIVITY_FILE)
energy_data = load_csv(ENERGY_FILE)
loss_data = load_csv(LOSS_FILE)
loss_energy_data = load_csv(LOSS_ENERGY_FILE)
capacitor_data = load_csv(CAPACITOR_FILE)


# ============================================================
# MAIN DATA CHECK
# ============================================================

if load_data is None:

    st.error(
        "load_analysis_results.csv was not found.\n\n"
        "Run the load analysis script first."
    )

    st.stop()


# ============================================================
# CAPACITOR BANK CONFIGURATION
# ============================================================

capacitor_step_kvar = DEFAULT_CAPACITOR_STEP_KVAR
max_bank_kvar = DEFAULT_MAX_BANK_KVAR

if capacitor_data is not None:

    try:

        capacitor_step_kvar = float(
            capacitor_data.loc[
                capacitor_data["parameter"] == "capacitor_step_kvar",
                "value"
            ].iloc[0]
        )

        max_bank_kvar = float(
            capacitor_data.loc[
                capacitor_data["parameter"] == "max_bank_kvar",
                "value"
            ].iloc[0]
        )

    except (IndexError, KeyError, ValueError, TypeError):

        st.warning(
            "Capacitor bank configuration could not be read. "
            "Default values are being used."
        )


# ============================================================
# SYSTEM CALCULATIONS
# ============================================================

total_p = safe_column_sum(load_data, "P_kW")
total_q = safe_column_sum(load_data, "Q_kVAR")

total_s = math.sqrt(
    total_p ** 2 +
    total_q ** 2
)

overall_pf = (
    total_p / total_s
    if total_s > 0
    else 0
)


# ============================================================
# ORIGINAL SYSTEM CURRENT
# ============================================================

current_before = (
    total_s * 1000 /
    (
        math.sqrt(3) *
        LV_VOLTAGE
    )
    if total_s > 0
    else 0
)


# ============================================================
# ORIGINAL TRANSFORMER LOADING
# ============================================================

loading_before = (
    total_s /
    TRANSFORMER_RATING_KVA
) * 100


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "⚡ Industrial Power Monitoring System"
)

st.subheader(
    "Electrical Load Monitoring & Power Factor Analysis Dashboard"
)

st.caption(
    "Industrial electrical system analysis, power factor correction, "
    "energy consumption and loss reduction."
)

st.markdown("---")


# ============================================================
# SYSTEM OVERVIEW
# ============================================================

st.header("System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Active Power",
        f"{total_p:.2f} kW"
    )

with col2:
    st.metric(
        "Reactive Power",
        f"{total_q:.2f} kVAR"
    )

with col3:
    st.metric(
        "Apparent Power",
        f"{total_s:.2f} kVA"
    )

with col4:
    st.metric(
        "Power Factor",
        f"{overall_pf:.3f}"
    )


# ============================================================
# SYSTEM PARAMETERS
# ============================================================

st.markdown("---")

st.header("System Parameters")

param_col1, param_col2, param_col3, param_col4 = st.columns(4)

with param_col1:
    st.metric(
        "LV Voltage",
        f"{LV_VOLTAGE} V"
    )

with param_col2:
    st.metric(
        "Transformer Rating",
        f"{TRANSFORMER_RATING_KVA} kVA"
    )

with param_col3:
    st.metric(
        "Capacitor Step",
        f"{capacitor_step_kvar:.0f} kVAR"
    )

with param_col4:
    st.metric(
        "Maximum Capacitor Bank",
        f"{max_bank_kvar:.0f} kVAR"
    )


# ============================================================
# POWER FACTOR STATUS
# ============================================================

st.markdown("---")

st.header("Power Factor Status")

if overall_pf >= 0.95:

    st.success(
        f"Power factor is good: {overall_pf:.3f}"
    )

elif overall_pf >= 0.90:

    st.warning(
        f"Power factor is moderate: {overall_pf:.3f}"
    )

else:

    st.error(
        f"Power factor is poor: {overall_pf:.3f}"
    )


# ============================================================
# KEY SYSTEM FINDINGS
# ============================================================

if priority_data is not None:

    st.markdown("---")

    st.header("Key System Findings")

    finding_col1, finding_col2, finding_col3 = st.columns(3)

    # Highest reactive power load
    if "Q_kVAR" in load_data.columns:

        highest_q_load = load_data.loc[
            load_data["Q_kVAR"].idxmax(),
            "Load"
        ]

    else:

        highest_q_load = "N/A"


    # Lowest PF load
    if "PF" in load_data.columns:

        lowest_pf_load = load_data.loc[
            load_data["PF"].idxmin(),
            "Load"
        ]

    else:

        lowest_pf_load = "N/A"


    # Highest priority load
    if (
        "Overall_Rank" in priority_data.columns
        and "Load" in priority_data.columns
    ):

        highest_priority_load = priority_data.loc[
            priority_data["Overall_Rank"].idxmin(),
            "Load"
        ]

    else:

        highest_priority_load = "N/A"


    with finding_col1:

        st.info(
            f"**Highest Reactive Power Load**\n\n"
            f"{highest_q_load}"
        )


    with finding_col2:

        st.info(
            f"**Lowest Power Factor Load**\n\n"
            f"{lowest_pf_load}"
        )


    with finding_col3:

        st.info(
            f"**Highest Priority Load**\n\n"
            f"{highest_priority_load}"
        )


# ============================================================
# INDUSTRIAL LOAD PERFORMANCE
# ============================================================

st.markdown("---")

st.header("Industrial Load Performance")

st.dataframe(
    load_data,
    width="stretch",
    hide_index=True
)


# ============================================================
# LOAD ANALYSIS
# ============================================================

st.markdown("---")

st.header("Load Analysis")

chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    st.subheader("Reactive Power by Load")

    if (
        "Load" in load_data.columns
        and "Q_kVAR" in load_data.columns
    ):

        q_chart = load_data.set_index(
            "Load"
        )["Q_kVAR"]

        st.bar_chart(q_chart)

    else:

        st.info("Reactive power data is not available.")


with chart_col2:

    st.subheader("Power Factor by Load")

    if (
        "Load" in load_data.columns
        and "PF" in load_data.columns
    ):

        pf_chart = load_data.set_index(
            "Load"
        )["PF"]

        st.bar_chart(pf_chart)

    else:

        st.info("Power factor data is not available.")


# ============================================================
# LOAD PRIORITY ANALYSIS
# ============================================================

if priority_data is not None:

    st.markdown("---")

    st.header("Load Priority Analysis")

    st.dataframe(
        priority_data,
        width="stretch",
        hide_index=True
    )

    if (
        "Load" in priority_data.columns
        and "Priority_Score" in priority_data.columns
    ):

        st.subheader("Priority Score")

        priority_chart = priority_data.set_index(
            "Load"
        )["Priority_Score"]

        st.bar_chart(priority_chart)


# ============================================================
# LOAD RECOMMENDATIONS
# ============================================================

if recommendation_data is not None:

    st.markdown("---")

    st.header("Load Recommendations")

    st.dataframe(
        recommendation_data,
        width="stretch",
        hide_index=True
    )


# ============================================================
# POWER FACTOR SENSITIVITY ANALYSIS
# ============================================================

if sensitivity_data is not None:

    st.markdown("---")

    st.header("Power Factor Sensitivity Analysis")

    st.write(
        "Effect of different target power factors on capacitor "
        "requirement, apparent power, current and transformer loading."
    )


    # --------------------------------------------------------
    # Sensitivity Table
    # --------------------------------------------------------

    st.subheader("Sensitivity Results")

    st.dataframe(
        sensitivity_data,
        width="stretch",
        hide_index=True
    )


    # --------------------------------------------------------
    # Target PF vs Transformer Loading
    # --------------------------------------------------------

    if (
        "target_pf" in sensitivity_data.columns
        and "transformer_loading" in sensitivity_data.columns
    ):

        st.subheader(
            "Target PF vs Transformer Loading"
        )

        loading_chart = sensitivity_data.set_index(
            "target_pf"
        )["transformer_loading"]

        st.line_chart(loading_chart)


    # --------------------------------------------------------
    # Target PF vs Current
    # --------------------------------------------------------

    if (
        "target_pf" in sensitivity_data.columns
        and "current_a" in sensitivity_data.columns
    ):

        st.subheader(
            "Target PF vs LV Current"
        )

        current_chart = sensitivity_data.set_index(
            "target_pf"
        )["current_a"]

        st.line_chart(current_chart)


    # --------------------------------------------------------
    # Target PF vs Required Capacitor
    # --------------------------------------------------------

    if (
        "target_pf" in sensitivity_data.columns
        and "required_qc_kvar" in sensitivity_data.columns
    ):

        st.subheader(
            "Target PF vs Required Capacitor"
        )

        capacitor_chart = sensitivity_data.set_index(
            "target_pf"
        )["required_qc_kvar"]

        st.line_chart(capacitor_chart)


# ============================================================
# VARIABLE POWER FACTOR CORRECTION ANALYSIS
# ============================================================

if sensitivity_data is not None:

    required_columns = [
        "target_pf",
        "required_qc_kvar",
        "selected_qc_kvar",
        "achieved_pf",
        "current_a",
        "new_s_kva",
        "transformer_loading"
    ]

    if all(
        column in sensitivity_data.columns
        for column in required_columns
    ):

        st.markdown("---")

        st.header(
            "Power Factor Correction Analysis"
        )

        st.write(
            "Select a target power factor to evaluate the required "
            "capacitor compensation and its effect on system performance."
        )


        # ----------------------------------------------------
        # TARGET PF SELECTION
        # ----------------------------------------------------

        target_pf_options = sorted(
            sensitivity_data["target_pf"]
            .dropna()
            .astype(float)
            .unique()
            .tolist()
        )

        default_index = 0

        if 0.95 in target_pf_options:

            default_index = target_pf_options.index(0.95)


        selected_target_pf = st.selectbox(
            "Select Target Power Factor",
            target_pf_options,
            index=default_index,
            format_func=lambda x: f"{x:.2f}"
        )


        # ----------------------------------------------------
        # SELECT RESULT
        # ----------------------------------------------------

        selected_result = sensitivity_data[
            sensitivity_data["target_pf"] == selected_target_pf
        ]


        if not selected_result.empty:

            result = selected_result.iloc[0]


            # ------------------------------------------------
            # STATUS
            # ------------------------------------------------

            status = str(
                result.get("status", "")
            )

            if status == "Target achieved":

                st.success(
                    f"Target PF of {selected_target_pf:.2f} "
                    f"can be achieved using the practical "
                    f"capacitor bank."
                )

            elif status == "No correction required":

                st.info(
                    f"No correction is required for target PF "
                    f"{selected_target_pf:.2f}."
                )

            else:

                st.warning(
                    f"Target PF analysis completed for "
                    f"{selected_target_pf:.2f}."
                )


            # ------------------------------------------------
            # CORRECTION RESULTS
            # ------------------------------------------------

            st.subheader("Correction Results")

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Original PF",
                    f"{overall_pf:.3f}"
                )

            with col2:

                st.metric(
                    "Target PF",
                    f"{result['target_pf']:.2f}"
                )

            with col3:

                st.metric(
                    "Required Capacitor",
                    f"{result['required_qc_kvar']:.2f} kVAR"
                )

            with col4:

                st.metric(
                    "Selected Capacitor",
                    f"{result['selected_qc_kvar']:.0f} kVAR"
                )


            # ------------------------------------------------
            # ELECTRICAL IMPACT
            # ------------------------------------------------

            st.subheader("Electrical Impact")

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Achieved PF",
                    f"{result['achieved_pf']:.3f}"
                )


            with col2:

                selected_current = float(
                    result["current_a"]
                )

                current_reduction = (
                    (
                        current_before -
                        selected_current
                    )
                    /
                    current_before
                    * 100
                ) if current_before > 0 else 0

                st.metric(
                    "Current Reduction",
                    f"{current_reduction:.2f}%"
                )


            with col3:

                st.metric(
                    "New Apparent Power",
                    f"{result['new_s_kva']:.2f} kVA"
                )


            with col4:

                st.metric(
                    "Transformer Loading",
                    f"{result['transformer_loading']:.2f}%"
                )


            # ------------------------------------------------
            # BEFORE VS AFTER
            # ------------------------------------------------

            st.subheader(
                "Before vs After Correction"
            )

            after_reactive_power = (
                total_q -
                float(result["selected_qc_kvar"])
            )

            comparison_data = pd.DataFrame({

                "Parameter": [
                    "Power Factor",
                    "Reactive Power",
                    "Apparent Power",
                    "LV Current",
                    "Transformer Loading"
                ],

                "Before Correction": [
                    f"{overall_pf:.3f}",
                    f"{total_q:.2f} kVAR",
                    f"{total_s:.2f} kVA",
                    f"{current_before:.2f} A",
                    f"{loading_before:.2f}%"
                ],

                "After Correction": [
                    f"{result['achieved_pf']:.3f}",
                    f"{after_reactive_power:.2f} kVAR",
                    f"{result['new_s_kva']:.2f} kVA",
                    f"{result['current_a']:.2f} A",
                    f"{result['transformer_loading']:.2f}%"
                ]
            })


            st.dataframe(
                comparison_data,
                width="stretch",
                hide_index=True
            )


            # ------------------------------------------------
            # CAPACITOR BANK INFORMATION
            # ------------------------------------------------

            st.subheader(
                "Capacitor Bank Information"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Selected Capacitor",
                    f"{result['selected_qc_kvar']:.0f} kVAR"
                )


            with col2:

                overcompensation = float(
                    result.get(
                        "overcompensation_kvar",
                        0
                    )
                )

                st.metric(
                    "Overcompensation",
                    f"{overcompensation:.2f} kVAR"
                )


            with col3:

                utilization = (
                    float(result["selected_qc_kvar"])
                    /
                    max_bank_kvar
                    * 100
                ) if max_bank_kvar > 0 else 0

                st.metric(
                    "Bank Utilization",
                    f"{utilization:.2f}%"
                )


            # ------------------------------------------------
            # OVERALL IMPROVEMENT
            # ------------------------------------------------

            st.subheader(
                "Overall Improvement"
            )

            improvement_col1, improvement_col2, improvement_col3 = (
                st.columns(3)
            )

            with improvement_col1:

                apparent_power_reduction = (
                    total_s -
                    float(result["new_s_kva"])
                )

                st.metric(
                    "Apparent Power Reduction",
                    f"{apparent_power_reduction:.2f} kVA"
                )


            with improvement_col2:

                st.metric(
                    "Current Reduction",
                    f"{current_reduction:.2f}%"
                )


            with improvement_col3:

                loading_reduction = (
                    loading_before -
                    float(result["transformer_loading"])
                )

                st.metric(
                    "Transformer Loading Reduction",
                    f"{loading_reduction:.2f} percentage points"
                )


            # ------------------------------------------------
            # BEFORE VS AFTER VISUALIZATION
            # ------------------------------------------------

            st.subheader(
                "Impact of Power Factor Correction"
            )

            before_after_chart = pd.DataFrame({

                "Before Correction": [
                    total_q,
                    total_s,
                    current_before,
                    loading_before
                ],

                "After Correction": [
                    after_reactive_power,
                    float(result["new_s_kva"]),
                    float(result["current_a"]),
                    float(result["transformer_loading"])
                ]

            }, index=[

                "Reactive Power (kVAR)",
                "Apparent Power (kVA)",
                "Current (A)",
                "Transformer Loading (%)"

            ])


            st.bar_chart(
                before_after_chart
            )


# ============================================================
# ENERGY CONSUMPTION ANALYSIS
# ============================================================

if energy_data is not None:

    st.markdown("---")

    st.header(
        "Energy Consumption Analysis"
    )

    st.write(
        "Estimated daily and monthly energy consumption "
        "based on load factor and operating hours."
    )


    # --------------------------------------------------------
    # Energy totals
    # --------------------------------------------------------

    total_daily_energy = safe_column_sum(
        energy_data,
        "daily_energy_kwh"
    )

    total_monthly_energy = safe_column_sum(
        energy_data,
        "monthly_energy_kwh"
    )


    energy_col1, energy_col2 = st.columns(2)

    with energy_col1:

        st.metric(
            "Daily Energy Consumption",
            f"{total_daily_energy:,.2f} kWh"
        )

    with energy_col2:

        st.metric(
            "Monthly Energy Consumption",
            f"{total_monthly_energy:,.2f} kWh"
        )


    # --------------------------------------------------------
    # Load-wise energy table
    # --------------------------------------------------------

    st.subheader(
        "Load-wise Energy Consumption"
    )

    st.dataframe(
        energy_data,
        width="stretch",
        hide_index=True
    )


    # --------------------------------------------------------
    # Daily energy chart
    # --------------------------------------------------------

    if (
        "load_name" in energy_data.columns
        and "daily_energy_kwh" in energy_data.columns
    ):

        st.subheader(
            "Daily Energy Consumption by Load"
        )

        daily_energy_chart = (
            energy_data
            .set_index("load_name")["daily_energy_kwh"]
        )

        st.bar_chart(
            daily_energy_chart
        )


    # --------------------------------------------------------
    # Monthly energy chart
    # --------------------------------------------------------

    if (
        "load_name" in energy_data.columns
        and "monthly_energy_kwh" in energy_data.columns
    ):

        st.subheader(
            "Monthly Energy Consumption by Load"
        )

        monthly_energy_chart = (
            energy_data
            .set_index("load_name")["monthly_energy_kwh"]
        )

        st.bar_chart(
            monthly_energy_chart
        )


# ============================================================
# SYSTEM LOSS ANALYSIS
# ============================================================

if loss_data is not None:

    st.markdown("---")

    st.header(
        "System Loss Analysis"
    )

    st.write(
        "Estimated three-phase copper losses before and after "
        "power factor correction."
    )


    # --------------------------------------------------------
    # Extract values from Parameter-Value CSV
    # --------------------------------------------------------

    copper_loss_before = get_loss_value(
        loss_data,
        "Copper Loss Before"
    )

    copper_loss_after = get_loss_value(
        loss_data,
        "Copper Loss After"
    )

    loss_reduction = get_loss_value(
        loss_data,
        "Loss Reduction"
    )

    loss_reduction_percent = get_loss_value(
        loss_data,
        "Loss Reduction Percent"
    )

    transformer_loading_before = get_loss_value(
        loss_data,
        "Transformer Loading Before"
    )

    transformer_loading_after = get_loss_value(
        loss_data,
        "Transformer Loading After"
    )


    # --------------------------------------------------------
    # Loss metrics
    # --------------------------------------------------------

    loss_col1, loss_col2, loss_col3 = st.columns(3)

    with loss_col1:

        if copper_loss_before is not None:

            st.metric(
                "Copper Loss Before",
                f"{copper_loss_before:.2f} kW"
            )


    with loss_col2:

        if copper_loss_after is not None:

            st.metric(
                "Copper Loss After",
                f"{copper_loss_after:.2f} kW"
            )


    with loss_col3:

        if loss_reduction_percent is not None:

            st.metric(
                "Loss Reduction",
                f"{loss_reduction_percent:.2f}%"
            )


    # --------------------------------------------------------
    # Additional transformer information
    # --------------------------------------------------------

    if (
        transformer_loading_before is not None
        and transformer_loading_after is not None
    ):

        transformer_col1, transformer_col2 = st.columns(2)

        with transformer_col1:

            st.metric(
                "Transformer Loading Before",
                f"{transformer_loading_before:.2f}%"
            )

        with transformer_col2:

            st.metric(
                "Transformer Loading After",
                f"{transformer_loading_after:.2f}%"
            )


    # --------------------------------------------------------
    # Loss comparison chart
    # --------------------------------------------------------

    if (
        copper_loss_before is not None
        and copper_loss_after is not None
    ):

        st.subheader(
            "Copper Loss Before vs After Correction"
        )

        loss_chart_data = pd.DataFrame({

            "Copper Loss (kW)": [
                copper_loss_before,
                copper_loss_after
            ]

        }, index=[
            "Before Correction",
            "After Correction"
        ])

        st.bar_chart(
            loss_chart_data
        )


    # --------------------------------------------------------
    # Loss result table
    # --------------------------------------------------------

    with st.expander("View Detailed Loss Analysis Results"):

        st.dataframe(
            loss_data,
            width="stretch",
            hide_index=True
        )


# ============================================================
# LOAD-WISE LOSS ENERGY ANALYSIS
# ============================================================

if loss_energy_data is not None:

    required_loss_energy_columns = [
        "Load",
        "Daily_Loss_Before_kWh",
        "Daily_Loss_After_kWh",
        "Daily_Loss_Saving_kWh",
        "Monthly_Loss_Before_kWh",
        "Monthly_Loss_After_kWh",
        "Monthly_Loss_Saving_kWh"
    ]

    if all(
        column in loss_energy_data.columns
        for column in required_loss_energy_columns
    ):

        st.markdown("---")

        st.header(
            "Loss Energy & Savings Analysis"
        )

        st.write(
            "Estimated electrical loss energy and savings for "
            "individual industrial loads after power factor correction."
        )


        # ----------------------------------------------------
        # System totals
        # ----------------------------------------------------

        total_daily_loss_before = safe_column_sum(
            loss_energy_data,
            "Daily_Loss_Before_kWh"
        )

        total_daily_loss_after = safe_column_sum(
            loss_energy_data,
            "Daily_Loss_After_kWh"
        )

        total_daily_loss_saving = safe_column_sum(
            loss_energy_data,
            "Daily_Loss_Saving_kWh"
        )

        total_monthly_loss_before = safe_column_sum(
            loss_energy_data,
            "Monthly_Loss_Before_kWh"
        )

        total_monthly_loss_after = safe_column_sum(
            loss_energy_data,
            "Monthly_Loss_After_kWh"
        )

        total_monthly_loss_saving = safe_column_sum(
            loss_energy_data,
            "Monthly_Loss_Saving_kWh"
        )


        # ----------------------------------------------------
        # Savings metrics
        # ----------------------------------------------------

        saving_col1, saving_col2, saving_col3 = st.columns(3)

        with saving_col1:

            st.metric(
                "Daily Loss Energy Saved",
                f"{total_daily_loss_saving:.2f} kWh"
            )

        with saving_col2:

            st.metric(
                "Monthly Loss Energy Saved",
                f"{total_monthly_loss_saving:.2f} kWh"
            )

        with saving_col3:

            reduction_percent = (
                total_monthly_loss_saving /
                total_monthly_loss_before *
                100
            ) if total_monthly_loss_before > 0 else 0

            st.metric(
                "Loss Energy Reduction",
                f"{reduction_percent:.2f}%"
            )


        # ----------------------------------------------------
        # Before / after loss energy
        # ----------------------------------------------------

        st.subheader(
            "System Loss Energy Before vs After"
        )

        loss_energy_summary = pd.DataFrame({

            "Before Correction": [
                total_daily_loss_before,
                total_monthly_loss_before
            ],

            "After Correction": [
                total_daily_loss_after,
                total_monthly_loss_after
            ]

        }, index=[

            "Daily Loss Energy (kWh)",
            "Monthly Loss Energy (kWh)"

        ])

        st.bar_chart(
            loss_energy_summary
        )


        # ----------------------------------------------------
        # Load-wise table
        # ----------------------------------------------------

        st.subheader(
            "Load-wise Loss Energy Results"
        )

        st.dataframe(
            loss_energy_data,
            width="stretch",
            hide_index=True
        )


        # ----------------------------------------------------
        # Monthly savings by load
        # ----------------------------------------------------

        st.subheader(
            "Monthly Loss Energy Saving by Load"
        )

        saving_chart = (
            loss_energy_data
            .set_index("Load")[
                "Monthly_Loss_Saving_kWh"
            ]
        )

        st.bar_chart(
            saving_chart
        )


# ============================================================
# PROJECT SUMMARY
# ============================================================

st.markdown("---")

st.header(
    "Project Summary"
)

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

with summary_col1:

    st.metric(
        "Total Industrial Loads",
        len(load_data)
    )


with summary_col2:

    st.metric(
        "Original PF",
        f"{overall_pf:.3f}"
    )


with summary_col3:

    st.metric(
        "Transformer Rating",
        f"{TRANSFORMER_RATING_KVA} kVA"
    )


with summary_col4:

    st.metric(
        "Monthly Energy",
        f"{total_monthly_energy:,.0f} kWh"
        if energy_data is not None
        else "N/A"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Industrial Power Monitoring System | "
    "Electrical Engineering Project"
)