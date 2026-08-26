import pandas as pd
from pathlib import Path


# -----------------------------------
# Project paths
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "load_priority_results.csv"


# -----------------------------------
# Read priority results
# -----------------------------------

df = pd.read_csv(INPUT_FILE)


# -----------------------------------
# Display header
# -----------------------------------

print("\n")
print("=" * 70)
print("             INDUSTRIAL LOAD RECOMMENDATION")
print("=" * 70)


# -----------------------------------
# Generate recommendations
# -----------------------------------

recommendations = []


for _, row in df.iterrows():

    load = row["Load"]

    pf = row["PF"]

    q_kvar = row["Q_kVAR"]

    priority = row["PF_Priority"]

    score = row["Priority_Score"]


    # --------------------------------
    # Determine recommendation
    # --------------------------------

    if pf < 0.85:

        recommendation = (
            "High priority for power factor correction"
        )

    elif pf < 0.90:

        recommendation = (
            "Consider power factor correction"
        )

    else:

        recommendation = (
            "No immediate PF correction required"
        )


    # --------------------------------
    # Determine reason
    # --------------------------------

    if pf < 0.85 and q_kvar > 80:

        reason = (
            "Low power factor and high reactive power consumption"
        )

    elif pf < 0.85:

        reason = (
            "Low power factor"
        )

    elif pf < 0.90:

        reason = (
            "Moderately low power factor"
        )

    elif q_kvar > 80:

        reason = (
            "High reactive power consumption"
        )

    else:

        reason = (
            "Acceptable electrical performance"
        )


    recommendations.append({

        "Load": load,

        "PF": pf,

        "Q_kVAR": q_kvar,

        "Priority": priority,

        "Priority_Score": score,

        "Reason": reason,

        "Recommendation": recommendation
    })


# -----------------------------------
# Create recommendation table
# -----------------------------------

recommendations_df = pd.DataFrame(
    recommendations
)


# -----------------------------------
# Display results
# -----------------------------------

print(
    recommendations_df.to_string(
        index=False
    )
)


# -----------------------------------
# Key recommendation
# -----------------------------------

highest_priority = (
    recommendations_df
    .sort_values(
        "Priority_Score",
        ascending=False
    )
    .iloc[0]
)


print("\n")
print("=" * 70)
print("                 KEY ENGINEERING RECOMMENDATION")
print("=" * 70)


print(
    f"\nHighest Priority Load : "
    f"{highest_priority['Load']}"
)

print(
    f"Power Factor          : "
    f"{highest_priority['PF']:.2f}"
)

print(
    f"Reactive Power        : "
    f"{highest_priority['Q_kVAR']:.2f} kVAR"
)

print(
    f"Priority Score        : "
    f"{highest_priority['Priority_Score']:.2f}"
)

print(
    f"\nRecommendation        : "
    f"{highest_priority['Recommendation']}"
)


# -----------------------------------
# Save results
# -----------------------------------

OUTPUT_FILE = (
    BASE_DIR /
    "data" /
    "load_recommendations.csv"
)


recommendations_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n")
print(
    "Recommendation results saved to:"
)

print(OUTPUT_FILE)