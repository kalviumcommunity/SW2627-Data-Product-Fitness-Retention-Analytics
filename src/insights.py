def generate_insights(summary, anomalies_df, churn_df):
    insights = []

    if summary["churn_rate"] > 0.5:
        insights.append("⚠️ High churn rate detected")

    if not anomalies_df.empty:
        insights.append("⚠️ Unusual user activity detected")

    high_risk = churn_df[churn_df["churn_risk"] == True]

    if len(high_risk) > 0:
        insights.append(f"🚨 {len(high_risk)} users likely to churn")

    if not insights:
        insights.append("✅ No major issues detected")

    return insights