#!/usr/bin/env python3
"""
etl/fetch_tfl.py

Downloads live streetcare (pothole + road defect) data from TfL.
"""

import requests

def fetch_streetcare():
    """Call the TfL API and get defect reports as JSON."""
    url = "https://api.tfl.gov.uk/Road/Streetcare"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def main():
    data = fetch_streetcare()
    print(f"✅ Got {len(data)} reports!")
    print("First 1 as example:")
    print(data[0])  # Print first one so we can see the structure

if __name__ == "__main__":
    main()
