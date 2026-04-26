from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from dateutil import parser as date_parser

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) 

def transform_with_ai(record):
    record_str = json.dumps(record)
    #print(record_str)
    prompt = f"""
    Convert this data into the target schema:
    CRITICAL RULES:
    - Do NOT encode, compress, or transform values into numbers or IDs.
    - Preserve all text exactly as it appears in the input unless explicitly reformatted.
    - Only split fields when explicitly instructed and based on clear delimiters.
    - Do NOT infer or guess values that are not directly present.

    Transformation rules:
    - full_name = cust_name (copy exactly)
    - signup_date = convert signup_dt to YYYY-MM-DD format only
    - addr format is: "street, city, state"
    - street = text before first comma
    - city = text between first and second comma
    - state = text after second comma (trim spaces)

    Target schema:
    - full_name(string)
    - street (string with number)
    - city (string)
    - state (string)
    - signup_date (YYYY-MM-DD)

    Input:
    {record_str}

    Return ONLY valid JSON.
    """

    response = client.responses.create(
        model="gpt-5.4-nano",
        input=prompt
    )

    return response.output_text

def transform_with_retry(record, retries=3):
    for attempt in range(retries):
        try:
            return transform_with_ai(record)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
    print("All attempts failed. Returning None.")
    return None