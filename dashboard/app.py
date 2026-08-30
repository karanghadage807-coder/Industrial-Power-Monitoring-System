import streamlit as st
import pandas as pd
import math
from pathlib import Path


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

FILES = {
    "load": DATA_DIR / "load_analysis_results.csv",
    "priority": DATA_DIR / "load_priority_results.csv",
    "recommendation": DATA_DIR / "load_recommendations.csv",
    "sensitivity": DATA_DIR / "pf_sensitivity_results.csv",
    "energy": DATA_DIR / "energy_analysis_results.csv",
    "loss": DATA_DIR / "loss_analysis_results.csv",
    "loss_energy": DATA_DIR / "loss_energy_analysis_results.csv",
    "capacitor": DATA_DIR / "capacitor_bank.csv",
}

LV_VOLTAGE = 415
TRANSFORMER_RATING_KVA = 1000


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Industrial Power Monitoring System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_csv(file_path):
    """Load CSV safely."""

    try:
        return pd.read_csv(file_path)

    except FileNotFoundError:
        return None

    except Exception as error:
        st.warning(
            f"Unable to read {file_path.name}: {error}"
        )
        return None


def get_loss_value(loss_df, parameter):
    """Extract a value from system loss analysis."""

    if loss_df is None:
        return None

    if "Parameter" not in loss_df.columns:
        return None

    rows = loss_df[
        loss_df["Parameter"] == parameter
    ]

    if rows.empty:
        return None

    return float(rows.iloc[0]["Value"])


def safe_number(value, decimals=2):
    """Format numeric values safely."""

    try:
        return f"{float(value):.{decimals}f}"

    except (ValueError, TypeError):
        return "N/A"


def style_dataframe(df):
    """Display dataframe using current Streamlit width API."""

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )


# ============================================================
# LOAD DATA
# ============================================================

load_data = load_csv(FILES["load"])
priority_data = load_csv(FILES["priority"])
recommendation_data = load_csv(FILES["recommendation"])
sensitivity_data = load_csv(FILES["sensitivity"])
energy_data = load_csv(FILES["energy"])
loss_data = load_csv(FILES["loss"])
loss_energy_data = load_csv(FILES["loss_energy"])
capacitor_data = load_csv(FILES["capacitor"])


# ============================================================
# MAIN DATA VALIDATION
# ============================================================

if load_data is None:

    st.error(
        "Load analysis results could not be found."
    )

    st.info(
        "Run the load analysis script first."
    )

    st.stop()


required_load_columns = {
    "Load",
    "P_kW",
    "Q_kVAR",
    "PF"
}

missing_columns = (
    required_load_columns -
    set(load_data.columns)
)

if missing_columns:

    st.error(
        "The load analysis CSV is missing required "
        f"columns: {', '.join(sorted(missing_columns))}"
    )

    st.stop()


# ============================================================
# SYSTEM CALCULATIONS
# ============================================================

total_p = load_data["P_kW"].sum()

total_q = load_data["Q_kVAR"].sum()

total_s = math.sqrt(
    total_p ** 2 +
    total_q ** 2
)

overall_pf = (
    total_p / total_s
    if total_s > 0
    else 0
)

current_before = (
    total_s * 1000 /
    (
        math.sqrt(3) *
        LV_VOLTAGE
    )
)

loading_before = (
    total_s /
    TRANSFORMER_RATING_KVA
) * 100


# ============================================================
# CAPACITOR CONFIGURATION
# ============================================================

capacitor_step_kvar = 25
max_bank_kvar = 500

if capacitor_data is not None:

    try:

        capacitor_step_kvar = float(
            capacitor_data.loc[
                capacitor_data["parameter"]
                == "capacitor_step_kvar",
                "value"
            ].iloc[0]
        )

        max_bank_kvar = float(
            capacitor_data.loc[
                capacitor_data["parameter"]
                == "max_bank_kvar",
                "value"
            ].iloc[0]
        )

    except (IndexError, KeyError, ValueError):

        pass


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚡ IPMS")

    st.caption(
        "Industrial Power Monitoring System"
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Load Analysis",
            "Power Factor Correction",
            "Energy Analysis",
            "Loss Analysis",
            "Recommendations"
        ]
    )

    st.markdown("---")

    st.subheader("System")

    st.write(
        f"**LV Voltage:** {LV_VOLTAGE} V"
    )

    st.write(
        f"**Transformer:** "
        f"{TRANSFORMER_RATING_KVA} kVA"
    )

    st.write(
        f"**Capacitor Step:** "
        f"{capacitor_step_kvar:.0f} kVAR"
    )

    st.write(
        f"**Maximum Bank:** "
        f"{max_bank_kvar:.0f} kVAR"
    )

    st.markdown("---")

    st.caption(
        "Electrical Engineering Project"
    )


# ============================================================
# HEADER
# ============================================================

st.title(
    "⚡ Industrial Power Monitoring System"
)

st.caption(
    "Electrical Load Monitoring • Power Factor Correction "
    "• Energy Analysis • Loss Analysis"
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.header("System Overview")

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

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

    st.markdown("---")

    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    st.subheader("System Status")

    status_col1, status_col2, status_col3 = st.columns(3)

    with status_col1:

        if overall_pf >= 0.95:

            st.success(
                f"Power Factor: {overall_pf:.3f} — Good"
            )

        elif overall_pf >= 0.90:

            st.warning(
                f"Power Factor: {overall_pf:.3f} — Moderate"
            )

        else:

            st.error(
                f"Power Factor: {overall_pf:.3f} — Poor"
            )

    with status_col2:

        if loading_before < 80:

            st.success(
                f"Transformer Loading: "
                f"{loading_before:.2f}%"
            )

        elif loading_before < 90:

            st.warning(
                f"Transformer Loading: "
                f"{loading_before:.2f}%"
            )

        else:

            st.error(
                f"Transformer Loading: "
                f"{loading_before:.2f}%"
            )

    with status_col3:

        st.info(
            f"Total Industrial Loads: "
            f"{len(load_data)}"
        )

    # --------------------------------------------------------
    # KEY FINDINGS
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("Key System Findings")

    highest_q_load = load_data.loc[
        load_data["Q_kVAR"].idxmax(),
        "Load"
    ]

    lowest_pf_load = load_data.loc[
        load_data["PF"].idxmin(),
        "Load"
    ]

    finding_col1, finding_col2, finding_col3 = st.columns(3)

    with finding_col1:

        st.info(
            f"**Highest Reactive Power**\n\n"
            f"{highest_q_load}"
        )

    with finding_col2:

        st.info(
            f"**Lowest Power Factor**\n\n"
            f"{lowest_pf_load}"
        )

    with finding_col3:

        st.info(
            f"**Transformer Loading**\n\n"
            f"{loading_before:.2f}%"
        )

    # --------------------------------------------------------
    # LOAD PERFORMANCE
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("Industrial Load Performance")

    style_dataframe(load_data)

    # --------------------------------------------------------
    # QUICK VISUALIZATION
    # --------------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        st.subheader(
            "Reactive Power by Load"
        )

        q_chart = (
            load_data
            .set_index("Load")["Q_kVAR"]
        )

        st.bar_chart(q_chart)

    with chart_col2:

        st.subheader(
            "Power Factor by Load"
        )

        pf_chart = (
            load_data
            .set_index("Load")["PF"]
        )

        st.bar_chart(pf_chart)


# ============================================================
# LOAD ANALYSIS
# ============================================================

elif page == "Load Analysis":

    st.header("Load Analysis")

    st.write(
        "Detailed electrical performance of individual "
        "industrial loads."
    )

    # --------------------------------------------------------
    # LOAD TABLE
    # --------------------------------------------------------

    style_dataframe(load_data)

    st.markdown("---")

    # --------------------------------------------------------
    # LOAD KPIs
    # --------------------------------------------------------

    highest_power = load_data.loc[
        load_data["P_kW"].idxmax()
    ]

    highest_q = load_data.loc[
        load_data["Q_kVAR"].idxmax()
    ]

    lowest_pf = load_data.loc[
        load_data["PF"].idxmin()
    ]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Highest Active Power",
            f"{highest_power['Load']}",
            f"{highest_power['P_kW']:.2f} kW"
        )

    with col2:

        st.metric(
            "Highest Reactive Power",
            f"{highest_q['Load']}",
            f"{highest_q['Q_kVAR']:.2f} kVAR"
        )

    with col3:

        st.metric(
            "Lowest Power Factor",
            f"{lowest_pf['Load']}",
            f"{lowest_pf['PF']:.3f}"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # LOAD CHARTS
    # --------------------------------------------------------

    st.subheader("Load Performance")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        st.write("Active Power")

        power_chart = (
            load_data
            .set_index("Load")["P_kW"]
        )

        st.bar_chart(power_chart)

    with chart_col2:

        st.write("Reactive Power")

        reactive_chart = (
            load_data
            .set_index("Load")["Q_kVAR"]
        )

        st.bar_chart(reactive_chart)

    st.subheader("Power Factor")

    pf_chart = (
        load_data
        .set_index("Load")["PF"]
    )

    st.bar_chart(pf_chart)

    # --------------------------------------------------------
    # PRIORITY
    # --------------------------------------------------------

    if priority_data is not None:

        st.markdown("---")

        st.subheader(
            "Load Priority Analysis"
        )

        style_dataframe(priority_data)

        if (
            "Load" in priority_data.columns
            and
            "Priority_Score" in priority_data.columns
        ):

            priority_chart = (
                priority_data
                .set_index("Load")["Priority_Score"]
            )

            st.bar_chart(priority_chart)


# ============================================================
# POWER FACTOR CORRECTION
# ============================================================

elif page == "Power Factor Correction":

    st.header(
        "Power Factor Correction Analysis"
    )

    st.write(
        "Evaluate the effect of different target power "
        "factors on capacitor requirement and system "
        "electrical performance."
    )

    if sensitivity_data is None:

        st.error(
            "Power factor sensitivity results are not available."
        )

        st.stop()

    # --------------------------------------------------------
    # SENSITIVITY TABLE
    # --------------------------------------------------------

    st.subheader(
        "Power Factor Sensitivity"
    )

    style_dataframe(sensitivity_data)

    st.markdown("---")

    # --------------------------------------------------------
    # TARGET PF SELECTION
    # --------------------------------------------------------

    if "target_pf" not in sensitivity_data.columns:

        st.error(
            "The sensitivity file does not contain "
            "'target_pf'."
        )

        st.stop()

    target_pf_options = (
        sensitivity_data["target_pf"]
        .dropna()
        .astype(float)
        .tolist()
    )

    default_index = 0

    if 0.95 in target_pf_options:

        default_index = (
            target_pf_options.index(0.95)
        )

    selected_target_pf = st.selectbox(
        "Select Target Power Factor",
        target_pf_options,
        index=default_index,
        format_func=lambda x: f"{x:.2f}"
    )

    selected_result = sensitivity_data[
        sensitivity_data["target_pf"]
        == selected_target_pf
    ]

    if selected_result.empty:

        st.warning(
            "No result available for the selected target PF."
        )

        st.stop()

    result = selected_result.iloc[0]

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    status = str(
        result.get("status", "")
    )

    if status == "Target achieved":

        st.success(
            f"Target PF {selected_target_pf:.2f} "
            "can be achieved with the available capacitor bank."
        )

    elif status == "No correction required":

        st.info(
            f"No correction is required for PF "
            f"{selected_target_pf:.2f}."
        )

    else:

        st.warning(
            f"Target PF {selected_target_pf:.2f} "
            "may not be achievable with the configured bank."
        )

    # --------------------------------------------------------
    # CORRECTION RESULTS
    # --------------------------------------------------------

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
            f"{selected_target_pf:.2f}"
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

    # --------------------------------------------------------
    # ELECTRICAL IMPACT
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("Electrical Impact")

    selected_current = float(
        result["current_a"]
    )

    selected_s = float(
        result["new_s_kva"]
    )

    selected_loading = float(
        result["transformer_loading"]
    )

    achieved_pf = float(
        result["achieved_pf"]
    )

    current_reduction = (
        (
            current_before -
            selected_current
        )
        / current_before
    ) * 100

    loading_reduction = (
        loading_before -
        selected_loading
    )

    apparent_power_reduction = (
        total_s -
        selected_s
    )

    after_reactive_power = (
        total_q -
        float(result["selected_qc_kvar"])
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Achieved PF",
            f"{achieved_pf:.3f}"
        )

    with col2:

        st.metric(
            "Current Reduction",
            f"{current_reduction:.2f}%"
        )

    with col3:

        st.metric(
            "Apparent Power Reduction",
            f"{apparent_power_reduction:.2f} kVA"
        )

    with col4:

        st.metric(
            "Transformer Loading",
            f"{selected_loading:.2f}%"
        )

    # --------------------------------------------------------
    # BEFORE VS AFTER
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader(
        "Before vs After Correction"
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
            f"{achieved_pf:.3f}",
            f"{after_reactive_power:.2f} kVAR",
            f"{selected_s:.2f} kVA",
            f"{selected_current:.2f} A",
            f"{selected_loading:.2f}%"
        ]
    })

    style_dataframe(comparison_data)

    # --------------------------------------------------------
    # CAPACITOR INFORMATION
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader(
        "Capacitor Bank"
    )

    selected_capacitor = float(
        result["selected_qc_kvar"]
    )

    overcompensation = float(
        result.get(
            "overcompensation_kvar",
            0
        )
    )

    utilization = (
        selected_capacitor /
        max_bank_kvar
    ) * 100

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Selected Capacitor",
            f"{selected_capacitor:.0f} kVAR"
        )

    with col2:

        st.metric(
            "Overcompensation",
            f"{overcompensation:.2f} kVAR"
        )

    with col3:

        st.metric(
            "Bank Utilization",
            f"{utilization:.2f}%"
        )

    # --------------------------------------------------------
    # SENSITIVITY CHARTS
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader(
        "Sensitivity Analysis"
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        if "transformer_loading" in sensitivity_data.columns:

            st.write(
                "Target PF vs Transformer Loading"
            )

            loading_chart = (
                sensitivity_data
                .set_index("target_pf")
                ["transformer_loading"]
            )

            st.line_chart(loading_chart)

    with chart_col2:

        if "current_a" in sensitivity_data.columns:

            st.write(
                "Target PF vs LV Current"
            )

            current_chart = (
                sensitivity_data
                .set_index("target_pf")
                ["current_a"]
            )

            st.line_chart(current_chart)

    if "required_qc_kvar" in sensitivity_data.columns:

        st.write(
            "Target PF vs Required Capacitor"
        )

        capacitor_chart = (
            sensitivity_data
            .set_index("target_pf")
            ["required_qc_kvar"]
        )

        st.line_chart(capacitor_chart)


# ============================================================
# ENERGY ANALYSIS
# ============================================================

elif page == "Energy Analysis":

    st.header(
        "Energy Consumption Analysis"
    )

    st.write(
        "Estimated energy consumption based on load factor "
        "and operating hours."
    )

    if energy_data is None:

        st.error(
            "Energy analysis results are not available."
        )

        st.stop()

    # --------------------------------------------------------
    # TOTAL ENERGY
    # --------------------------------------------------------

    total_daily_energy = (
        energy_data["daily_energy_kwh"].sum()
    )

    total_monthly_energy = (
        energy_data["monthly_energy_kwh"].sum()
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Daily Energy Consumption",
            f"{total_daily_energy:,.2f} kWh"
        )

    with col2:

        st.metric(
            "Monthly Energy Consumption",
            f"{total_monthly_energy:,.2f} kWh"
        )

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader(
        "Load-wise Energy Consumption"
    )

    style_dataframe(energy_data)

    # --------------------------------------------------------
    # DAILY ENERGY
    # --------------------------------------------------------

    st.subheader(
        "Daily Energy Consumption by Load"
    )

    daily_energy_chart = (
        energy_data
        .set_index("load_name")
        ["daily_energy_kwh"]
    )

    st.bar_chart(daily_energy_chart)

    # --------------------------------------------------------
    # MONTHLY ENERGY
    # --------------------------------------------------------

    st.subheader(
        "Monthly Energy Consumption by Load"
    )

    monthly_energy_chart = (
        energy_data
        .set_index("load_name")
        ["monthly_energy_kwh"]
    )

    st.bar_chart(monthly_energy_chart)


# ============================================================
# LOSS ANALYSIS
# ============================================================

elif page == "Loss Analysis":

    st.header(
        "Electrical Loss Analysis"
    )

    st.write(
        "Estimated system and load-wise copper losses "
        "before and after power factor correction."
    )

    # --------------------------------------------------------
    # SYSTEM LOSS
    # --------------------------------------------------------

    if loss_data is not None:

        st.subheader(
            "System-level Copper Loss"
        )

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

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Copper Loss Before",
                f"{copper_loss_before:.2f} kW"
            )

        with col2:

            st.metric(
                "Copper Loss After",
                f"{copper_loss_after:.2f} kW"
            )

        with col3:

            st.metric(
                "Loss Reduction",
                f"{loss_reduction_percent:.2f}%"
            )

        loss_chart = pd.DataFrame({

            "Copper Loss (kW)": [
                copper_loss_before,
                copper_loss_after
            ]

        }, index=[
            "Before Correction",
            "After Correction"
        ])

        st.bar_chart(loss_chart)

        with st.expander(
            "View system loss data"
        ):

            style_dataframe(loss_data)

    # --------------------------------------------------------
    # LOSS ENERGY
    # --------------------------------------------------------

    if loss_energy_data is not None:

        st.markdown("---")

        st.subheader(
            "Energy Savings from Loss Reduction"
        )

        required_columns = {
            "Daily_Loss_Saving_kWh",
            "Monthly_Loss_Saving_kWh",
            "Monthly_Loss_Before_kWh"
        }

        if required_columns.issubset(
            loss_energy_data.columns
        ):

            daily_saving = (
                loss_energy_data[
                    "Daily_Loss_Saving_kWh"
                ].sum()
            )

            monthly_saving = (
                loss_energy_data[
                    "Monthly_Loss_Saving_kWh"
                ].sum()
            )

            monthly_before = (
                loss_energy_data[
                    "Monthly_Loss_Before_kWh"
                ].sum()
            )

            saving_percent = (
                monthly_saving /
                monthly_before *
                100
                if monthly_before > 0
                else 0
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Daily Loss Energy Saved",
                    f"{daily_saving:.2f} kWh"
                )

            with col2:

                st.metric(
                    "Monthly Loss Energy Saved",
                    f"{monthly_saving:.2f} kWh"
                )

            with col3:

                st.metric(
                    "Loss Energy Reduction",
                    f"{saving_percent:.2f}%"
                )

            st.subheader(
                "Monthly Loss Energy Saving by Load"
            )

            saving_chart = (
                loss_energy_data
                .set_index("Load")
                ["Monthly_Loss_Saving_kWh"]
            )

            st.bar_chart(saving_chart)

        st.markdown("---")

        st.subheader(
            "Load-wise Loss Energy Results"
        )

        style_dataframe(loss_energy_data)


# ============================================================
# RECOMMENDATIONS
# ============================================================

elif page == "Recommendations":

    st.header(
        "Load Recommendations"
    )

    st.write(
        "Recommended actions based on load priority, "
        "power factor and reactive power analysis."
    )

    if recommendation_data is not None:

        style_dataframe(
            recommendation_data
        )

    else:

        st.warning(
            "Recommendation results are not available."
        )

    # --------------------------------------------------------
    # PRIORITY RESULTS
    # --------------------------------------------------------

    if priority_data is not None:

        st.markdown("---")

        st.subheader(
            "Load Priority Ranking"
        )

        style_dataframe(
            priority_data
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Industrial Power Monitoring System | "
    "Electrical Engineering Project | "
    "Python + Pandas + Streamlit"
)