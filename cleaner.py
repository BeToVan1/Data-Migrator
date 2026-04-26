import json
from datetime import datetime

def clean_data(ai_output):
    try:
        data = json.loads(ai_output)
        print(data)
        required_fields = ["full_name", "street", "city", "state", "signup_date"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing field: {field}")
            # Validate signup_date format   
        if data["signup_date"] is None or not isinstance(data["signup_date"], str):
            raise ValueError("signup_date must be a string in YYYY-MM-DD format.")
        try:
            datetime.strptime(data["signup_date"], "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format for signup_date. Expected YYYY-MM-DD.")
        return data

    except Exception as e:
        print(f"Error cleaning data: {e}")
        return None