import json
from datetime import datetime

def clean_data(ai_output):
    try:
        data = json.loads(ai_output)

        # Ensure required fields exist
        required_fields = ["customerName", "amount", "date"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing field: {field}")

        # Convert amount to float
        data["amount"] = float(data["amount"])

        # Normalize date
        data["date"] = datetime.strptime(data["date"], "%Y-%m-%d").strftime("%Y-%m-%d")

        return data

    except Exception as e:
        print(f"Error cleaning data: {e}")
        return None