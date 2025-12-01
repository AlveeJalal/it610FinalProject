import requests
import json

# Base URL and endpoint
indexer_url = "https://localhost:9200"
endpoint = "/wazuh-alerts*/_search"
url = indexer_url + endpoint

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer <WAZUH_INDEXER_JWT>"
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
    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    response.raise_for_status()  # Raise an exception for HTTP errors
    result = response.json()  # Parse the JSON response

    # Process and display the results
    print("Top three (3) Users with Most Successful Login Sessions:")
    if "aggregations" in result and "successful_logins_by_users" in result["aggregations"]:
        buckets = result["aggregations"]["successful_logins_by_users"]["buckets"]
        if buckets:
            for user in buckets:
                print(f"User: {user['key']}, Count: {user['doc_count']}")
        else:
            print("No data found for the query.")
    else:
        print("Unexpected response format.")
except requests.exceptions.RequestException as e:
    print(f"Error querying Wazuh API: {e}")