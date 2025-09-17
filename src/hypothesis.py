from scipy.stats import f_oneway

def anova_shipmode_summary(dff):
    """
    One-way ANOVA: Sales ~ Ship Mode.
    Returns short text with p-value + decision (α=0.05). 
    """
    if dff is None or dff.empty or "Ship Mode" not in dff or "Sales" not in dff:
        return "ANOVA: missing columns or no data."
    groups = [g["Sales"].values for _, g in dff.groupby("Ship Mode") if len(g) > 1]
    if len(groups) < 2:
        return "ANOVA: need ≥2 non-empty ship-mode groups."
    f, p = f_oneway(*groups)
    decision = "Reject H₀" if p < 0.05 else "Fail to reject H₀"
    return f"ANOVA (Sales ~ Ship Mode): p = {p:.4f} → {decision} (α=0.05)"

