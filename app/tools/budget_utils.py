def calculate_estimated_budget(days: int, tier: str = "budget"):
    # Mock rates for April 2026
    rates = {
        "budget": {"food": 500, "travel": 300, "buffer": 200},
        "mid": {"food": 1500, "travel": 800, "buffer": 500},
        "luxury": {"food": 5000, "travel": 2500, "buffer": 2000}
    }
    
    selected = rates.get(tier, rates["budget"])
    total_per_day = selected["food"] + selected["travel"] + selected["buffer"]
    
    return {
        "daily_breakdown": selected,
        "total_estimated": total_per_day * days,
        "currency": "INR"
    }