def calculate_skin_care(skin_type, uv_index, humidity):
    """
    Formulates skin care advice based on Fitzpatrick skin type, UV index, and air humidity.
    """
    # Parse skin sensitivity
    is_sensitive = "Type I" in skin_type or "Type II" in skin_type
    
    # Humidity adjustments
    is_dry_air = humidity < 40
    is_humid_air = humidity > 75
    
    title = "General Skin Care"
    alert_level = "info"
    
    if is_sensitive:
        if uv_index >= 3:
            title = "Sensitive Skin UV Protection"
            text = f"Your skin type ({skin_type}) has high UV sensitivity. Apply zinc oxide sunscreen, wear full sleeves, and reapply every 2 hours."
            alert_level = "warning"
        elif is_dry_air:
            title = "Sensitive Dry Air Care"
            text = "Low humidity detected. Sensitive skin types should use a mild cream-based moisturizer and avoid harsh soap cleansers."
            alert_level = "info"
        else:
            title = "Sensitive Skin Routine"
            text = "Use hypoallergenic products and maintain a standard daily moisturizing routine."
            alert_level = "success"
    else:
        # Darker skin types / less sensitive to burn, but dry/wet air still affects barrier
        if is_dry_air:
            title = "Dry Air Moisturizing"
            text = "The air is dry. Use a hydrating serum or light moisturizer to protect your skin barrier from moisture loss."
            alert_level = "info"
        elif is_humid_air:
            title = "Humid Air Skin Cleansing"
            text = "High humidity can lead to excess oil production. Use a gentle foaming cleanser to keep pores clear."
            alert_level = "success"
        else:
            title = "Standard Skin Maintenance"
            text = "Skin conditions are balanced. Maintain your daily skin care and moisturizer routine."
            alert_level = "success"
            
    return {
        'title': title,
        'text': text,
        'alert_level': alert_level,
        'category': 'skincare',
        'icon': 'fa-spa'
    }
