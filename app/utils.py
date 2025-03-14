from typing import Tuple, List, Dict, Any

def process_user_query(user_message: str) -> Tuple[str, int]:
    """Extract category and limit from user message"""
    category = None
    limit = None

    if "smartphone" in user_message.lower():
        category = "Smartphone"
    if "first" in user_message.lower() and "assets" in user_message.lower():
        limit = 5

    return category, limit

def map_fieldsets_to_models(models: List[Dict[str, Any]], fieldsets: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Map fieldsets to models"""
    fieldset_map = {fieldset["id"]: fieldset["fields"] for fieldset in fieldsets}
    model_fieldset_map = {model["id"]: fieldset_map.get(model["fieldset_id"], []) for model in models}
    return model_fieldset_map

def summarize_data(data: List[Dict[str, Any]], model_fieldset_map: Dict[str, Any], category=None, limit=None) -> str:
    """Summarize data for OpenAI processing"""
    if category:
        data = [item for item in data if item.get('category', {}).get('name') == category]
    if limit:
        data = data[:limit]
    
    summary_items = []
    for item in data:
        custom_fields = []
        for k, v in item.get('custom_fields', {}).items():
            if k in model_fieldset_map.get(item.get('model', {}).get('id', 'N/A'), []):
                custom_fields.append(f'{k}: {v.get("value", "N/A")}')
        
        summary_items.append(
            f"ID: {item.get('id', 'N/A')}, Name: {item.get('name', 'N/A')}, "
            f"Tag: {item.get('asset_tag', 'N/A')}, Model: {item.get('model', {}).get('name', 'N/A')}, "
            f"Category: {item.get('category', {}).get('name', 'N/A')}, "
            f"Status: {item.get('status_label', {}).get('name', 'N/A')}, "
            f"Assigned To: {item.get('assigned_to', {}).get('name', 'N/A')}, "
            f"Location: {item.get('location', {}).get('name', 'N/A')}, "
            f"Custom Fields: {', '.join(custom_fields)}"
        )
    
    return "\n".join(summary_items)