#!/usr/bin/env python3
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/.env_file')

# Base URL and endpoint
indexer_url = "https://wazuh.indexer:9200"  # Changed from localhost
endpoint = "/wazuh-alerts*/_search"
url = indexer_url + endpoint

# Use Basic Auth with indexer credentials
username = os.environ.get('INDEXER_USERNAME')
password = os.environ.get('INDEXER_PASSWORD')

headers = {
    "Content-Type": "application/json"
}

# Query payload
payload = {
    "size": 0,
    "query": {
        "match": {
            "rule.description": "PAM: Login session opened."
        }
    },
    "aggs": {
        "successful_logins_by_user": {
            "terms": {
                "field": "data.dstuser",
                "size": 3,
                "order": {
                    "_count": "desc"
                }
            }
        }
    }
}

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Execute the API request
try:
    response = requests.post(
        url, 
        headers=headers, 
        auth=(username, password),  # Add Basic Auth
        data=json.dumps(payload), 
        verify=False
    )
    response.raise_for_status()
    result = response.json()
    
    # Process and display the results
    print("Top three (3) Users with Most Successful Login Sessions:")
    if "aggregations" in result and "successful_logins_by_user" in result["aggregations"]:
        buckets = result["aggregations"]["successful_logins_by_user"]["buckets"]
        if buckets:
            for user in buckets:
                print(f"User: {user['key']}, Count: {user['doc_count']}")
        else:
            print("No data found for the query.")
    else:
        print("Unexpected response format.")
except requests.exceptions.RequestException as e:
    print(f"Error querying Wazuh API: {e}")
