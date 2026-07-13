import requests
import json

# The network address of your Django API gateway
url = "http://127.0.0.1:8000/api/predict-satisfaction/"

# Sample employee record parameters to feed to your Random Forest model
payload = {
    "Career_Progression": 4.2,
    "Compensation": 3.8,
    "Manager_Relationship": 4.5,
    "Work_Life_Balance": 3.9
}

headers = {
    "Content-Type": "application/json"
}

print("📡 Sending data payload to EngageIQ Machine Learning Engine...")

try:
    # Trigger the live POST network request
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    print(f"🔒 Server Response Code: {response.status_code}")
    print("\n📊 Model Prediction Output Matrix:")
    print(json.dumps(response.json(), indent=4))

except Exception as e:
    print(f"❌ Connection failed! Ensure your django server is running. Error: {e}")