import requests
import hashlib
import time

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

def get_exact_payload():
    base_json = '{"padding":""}'
    padding_needed = 13337 - len(base_json)
    return '{"padding":"' + ('a' * padding_needed) + '"}'

def test_phase3():
    print("[*] Testing Phase 3: State-Machine 'Warm Up'")
    payload = get_exact_payload()

    for i in range(1, 4):
        print(f"\n[*] Sending Request {i}...")
        res = requests.post(TARGET_URL, headers=get_headers(), data=payload)
        print(f"[+] Status: {res.status_code}, Body: {res.text}")
        if "part_1" in res.text:
            print("[!!!] Retrieved Part 1 flag!")
        time.sleep(1)
        
    print("\n[*] Waiting 11 seconds to test cold start reset...")
    time.sleep(11)
    
    print("\n[*] Sending Request 4 (should be reset to Cold Hearted)...")
    res = requests.post(TARGET_URL, headers=get_headers(), data=payload)
    print(f"[+] Status: {res.status_code}, Body: {res.text}")

if __name__ == '__main__':
    test_phase3()
