import requests
import hashlib
import time
import json

TARGET_URL = 'http://localhost:3000/api/hate'
SALT = "Troy_Fallen_123"

def get_headers():
    timestamp = str(int(time.time() * 1000))
    payload = SALT + timestamp
    checksum = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    return {
        'X-Hate-Time': timestamp,
        'X-Hate-Checksum': checksum,
        'Content-Type': 'application/json'
    }

def test_phase2():
    print("[*] Testing Phase 2: Exact Payload Padding")

    # 1. Too light
    print("\n[*] Sending Too Light payload (< 13336 bytes)")
    too_light_payload = {"test": "aaa"}
    res = requests.post(TARGET_URL, headers=get_headers(), json=too_light_payload)
    print(f"[+] Status: {res.status_code}, Body: {res.text}")

    # 2. Too heavy
    print("\n[*] Sending Too Heavy payload (> 13337 bytes)")
    base_json = '{"padding":""}'
    padding_needed = 13338 - len(base_json)
    too_heavy_payload = '{"padding":"' + ('a' * padding_needed) + '"}'
    res = requests.post(TARGET_URL, headers=get_headers(), data=too_heavy_payload)
    print(f"[+] Status: {res.status_code}, Body: {res.text}")
    print(f"[+] Sent {len(too_heavy_payload.encode('utf-8'))} bytes")

    # 3. Almost there (13336 bytes)
    print("\n[*] Sending Almost There payload (13336 bytes)")
    padding_needed = 13336 - len(base_json)
    almost_there_payload = '{"padding":"' + ('a' * padding_needed) + '"}'
    res = requests.post(TARGET_URL, headers=get_headers(), data=almost_there_payload)
    print(f"[+] Status: {res.status_code}, Body: {res.text}")
    print(f"[+] Sent {len(almost_there_payload.encode('utf-8'))} bytes")

    # 4. Exact match (13337 bytes)
    print("\n[*] Sending Exact Match valid JSON payload (13337 bytes)")
    padding_needed = 13337 - len(base_json)
    exact_payload = '{"padding":"' + ('a' * padding_needed) + '"}'
    res = requests.post(TARGET_URL, headers=get_headers(), data=exact_payload)
    print(f"[+] Status: {res.status_code}, Body: {res.text}")
    print(f"[+] Sent {len(exact_payload.encode('utf-8'))} bytes")

if __name__ == '__main__':
    test_phase2()
