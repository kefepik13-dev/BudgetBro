def calculate_budget_health_score(raw):
    """
    Berechnet einen Budget Health Score (0-100) basierend auf mehreren Faktoren.
    """
    # Werte aus Dictionary holen und sicherstellen dass sie Zahlen sind
    monthly_income = float(raw.get("monthly_income", 0) or 0)
    monthly_fixed_costs = float(raw.get("monthly_fixed_costs", 0) or 0)
    monthly_savings = float(raw.get("monthly_savings", 0) or 0)
    
    # Sicherstellen dass keine negativen Werte
    if monthly_income < 0:
        monthly_income = 0
    if monthly_fixed_costs < 0:
        monthly_fixed_costs = 0
    if monthly_savings < 0:
        monthly_savings = 0

    # 1) Savings Rate Score (30% Gewichtung)
    if monthly_income > 0:
        savings_rate = monthly_savings / monthly_income
    else:
        savings_rate = 0
    
    # Score berechnen: 20% Sparquote = 100 Punkte
    savings_rate_score = savings_rate * 500
    if savings_rate_score > 100:
        savings_rate_score = 100
    if savings_rate_score < 0:
        savings_rate_score = 0
    savings_rate_score = int(round(savings_rate_score))

    # 2) Fixed Cost Ratio Score (25% Gewichtung)
    if monthly_income > 0:
        fixed_ratio = monthly_fixed_costs / monthly_income
    else:
        fixed_ratio = 1.0
    
    # Score berechnen: <=50% = 100, >=90% = 0
    if fixed_ratio <= 0.5:
        fixed_ratio_score = 100
    elif fixed_ratio >= 0.9:
        fixed_ratio_score = 0
    else:
        # Linear zwischen 50% und 90%
        fixed_ratio_score = 100 - ((fixed_ratio - 0.5) / 0.4) * 100
        if fixed_ratio_score > 100:
            fixed_ratio_score = 100
        if fixed_ratio_score < 0:
            fixed_ratio_score = 0
    fixed_ratio_score = int(round(fixed_ratio_score))

    # 3) Monthly Surplus Score (20% Gewichtung)
    monthly_surplus = monthly_income - monthly_fixed_costs - monthly_savings
    if monthly_income > 0:
        surplus_ratio = monthly_surplus / monthly_income
    else:
        surplus_ratio = 0
    
    # Score berechnen: >=10% Überschuss = 100, negativ = 0
    if monthly_surplus >= 0:
        surplus_score = 50 + (surplus_ratio * 500)
        if surplus_score > 100:
            surplus_score = 100
        if surplus_score < 0:
            surplus_score = 0
    else:
        surplus_score = 0
    surplus_score = int(round(surplus_score))

    # Gewichteter Durchschnitt berechnen
    weights = {
        "savings_rate": 0.4,      # 40%
        "fixed_cost_ratio": 0.33,  # 33%
        "monthly_surplus": 0.27,   # 27%
    }
    
    final_score = (
        savings_rate_score * weights["savings_rate"] +
        fixed_ratio_score * weights["fixed_cost_ratio"] +
        surplus_score * weights["monthly_surplus"]
    )
    final_score = int(round(final_score))

    return {
        "score": final_score,
        "weights": weights,
        "subscores": {
            "savings_rate": {
                "score": savings_rate_score,
                "explanation": "Wie viel Prozent deines Einkommens du monatlich sparst. ~20% oder mehr ist sehr gut.",
                "value": {"savings_rate": savings_rate},
            },
            "fixed_cost_ratio": {
                "score": fixed_ratio_score,
                "explanation": "Anteil Fixkosten am Einkommen. <=50% ist top; ab ~90% wird es kritisch.",
                "value": {"fixed_cost_ratio": fixed_ratio},
            },
            "monthly_surplus": {
                "score": surplus_score,
                "explanation": "Was nach Fixkosten und geplantem Sparen übrig bleibt. Positiver Puffer ist stabiler.",
                "value": {
                    "monthly_surplus": monthly_surplus,
                    "monthly_surplus_ratio": surplus_ratio,
                },
            },
        },
    }
