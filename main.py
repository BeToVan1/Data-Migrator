import json
import time
from ai_mapper import transform_with_retry
from cleaner import clean_data

start = time.time()

def run_pipeline():
    success = 0
    failures = 0

    with open("data/input.json") as f:
        records = json.load(f)

    cleaned = []

    for record in records:
        print(f"Processing: {record}")

        ai_output = transform_with_retry(record)
        cleaned_record = clean_data(ai_output)

        if cleaned_record:
            success += 1
            cleaned.append(cleaned_record)
        else:
            failures += 1
            
    with open("output/cleaned.json", "w") as f:
        json.dump(cleaned, f, indent=2)

    print("Data migration complete!")
    print(f"Successes: {success}, Failures: {failures}")
    print(f"Total time: {time.time() - start:.2f} seconds") 

if __name__ == "__main__":
    run_pipeline()