import requests
import hashlib
import time

TARGET_URL = 'http://localhost:3000/api/hate'

def test_phase1():
    print("[*] Testing Phase 1: Edge Middleware Gateway")
    
    # 1. Hit the endpoint without headers to trigger 418
    print("[*] Sending request without headers...")
    res = requests.get(TARGET_URL)
    
    if res.status_code == 418:
        print("[+] Got 418 I'm a Teapot response!")
        print(f"[+] Response body: {res.text}")
        
        # 2. Extract X-Hint time (not strictly needed since we can use local time, 
        # but the puzzle description mentions using it)
        x_hint = res.headers.get('X-Hint')
        server_header = res.headers.get('Server')
        
        if x_hint is None:
            print("[-] Error: Missing X-Hint header")
            return
            
        print(f"[+] Extracted X-Hint: {x_hint}")
        print(f"[+] Server Header: {server_header}")
        
    else:
        print(f"[-] Expected 418, got {res.status_code}")
        return

    # 3. Get the salt from robots.txt
    print("[*] Fetching robots.txt to extract SALT...")
    robots_res = requests.get('http://localhost:3000/robots.txt')
    salt = None
    for line in robots_res.text.split('\n'):
        if 'SALT=' in line:
            salt = line.split('SALT=')[1].strip().strip('"').strip("'")
            break
            
    if not salt:
        print("[-] Error: Could not find SALT in robots.txt")
        return
        
    print(f"[+] Found SALT: {salt}")
    
    # 4. Craft valid payload using the current time
    timestamp = str(int(time.time() * 1000))
    # Note: Javascript's Date.now() is in milliseconds. 
    # Valid window is +/- 5000ms.
    
    # Payload = SALT + timestamp
    # Hash using SHA-256 (as implemented in middleware.ts)
    payload = salt + timestamp
    checksum = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    
    print(f"[*] Sending request with valid X-Hate-Time={timestamp} and X-Hate-Checksum={checksum}...")
    headers = {
        'X-Hate-Time': timestamp,
        'X-Hate-Checksum': checksum
    }
    
    success_res = requests.get(TARGET_URL, headers=headers)
    print(f"[+] Response Status: {success_res.status_code}")
    print(f"[+] Response Body: {success_res.text}")
    
    if success_res.status_code == 200:
        print("[+] Phase 1 successfully bypassed!")
    else:
        print("[-] Phase 1 bypass failed")

if __name__ == '__main__':
    test_phase1()
