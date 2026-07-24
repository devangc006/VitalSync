def calculate_uv_safety(uv_index):
    """
    Formulates sun safety alerts and sunscreen application requirements based on the UV index.
    """
    if uv_index >= 8:
        title = "Extreme UV Warning"
        text = "UV index is extremely high. SPF 50+ sunscreen, wide-brimmed hat, and sunglasses are highly recommended. Avoid the sun between 11 AM and 4 PM."
        alert_level = "danger"
    elif uv_index >= 6:
        title = "High UV Alert"
        text = "High UV intensity. Apply SPF 30+ sunscreen, wear a cap, and seek shade during peak midday hours."
        alert_level = "warning"
    elif uv_index >= 3:
        title = "Moderate UV Notice"
        text = "Moderate UV intensity. Apply SPF 15+ sunscreen if outdoors for more than 45 minutes."
        alert_level = "info"
    else:
        title = "Low UV Intensity"
        text = "UV exposure risk is low. No special outdoor precautions are necessary."
        alert_level = "success"
        
    return {
        'title': title,
        'text': text,
        'uv_index': uv_index,
        'alert_level': alert_level,
        'category': 'uv',
        'icon': 'fa-sun'
    }
