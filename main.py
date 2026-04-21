import json
from ai_mapper import transform_with_ai
from cleaner import clean_data

def run_pipeline():
    with open("data/input.json") as f:
        records = json.load(f)

    cleaned = []

    for record in records:
        print(f"Processing: {record}")

        ai_output = transform_with_ai(record)
        cleaned_record = clean_data(ai_output)

        cleaned.append(cleaned_record)

    with open("output/cleaned.json", "w") as f:
        json.dump(cleaned, f, indent=2)

    print("Data migration complete!")

if __name__ == "__main__":
    run_pipeline()