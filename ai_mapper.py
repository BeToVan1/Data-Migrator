from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from dateutil import parser as date_parser

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) 

def normalize_date_value(val):
    if not isinstance(val, str):
        return val
    s = val.strip()
    # if already ISO-like, return as-is if parse succeeds and formatted matches
    try:
        dt = date_parser.parse(s, fuzzy=True, default=None)
        # if parse returns a datetime, format to YYYY-MM-DD
        return dt.date().isoformat()
    except Exception:
        return val

def normalize_record(record):
    # record expected to be a dict; normalize common date keys
    if not isinstance(record, dict):
        return record
    rec = dict(record)  # shallow copy
    # common keys to normalize; add more keys if needed
    for k in list(rec.keys()):
        if k.lower() in ("date", "date_paid", "transaction_date", "dt"):
            rec[k] = normalize_date_value(rec[k])
    # fallback: if no explicit date key, try to find any value that parses as a date
    if not any(k.lower() == "date" for k in rec):
        for k, v in rec.items():
            if isinstance(v, str):
                parsed = normalize_date_value(v)
                if parsed != v:
                    rec[k] = parsed
                    break
    return rec

def transform_with_ai(record):
    # if record is a dict, normalize dates and serialize
    if isinstance(record, dict):
        normalized = normalize_record(record)
        record_str = json.dumps(normalized, ensure_ascii=False)
    else:
        record_str = str(record)

    prompt = f"""
    Convert this data into the target schema:

    Target schema:
    - customerName (string with numbers)
    - amount (number)
    - date (YYYY-MM-DD)

    Input:
    {record_str}

    Return ONLY valid JSON.
    """

    response = client.responses.create(
        model="gpt-5.4-nano",
        input=prompt
    )

    return response.output_text