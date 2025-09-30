import requests

url = "https://kerbal.sunshinectf.games/click"

# Start with your current cookie
cookies = {
    "clicker": "580212e06b5768bb3bcd3db20f7e1985a5e0145c967d7ded0aab6c027f9f559d"
}

for i in range(24611681):  # number of clicks to simulate
    response = requests.post(url, cookies=cookies)
    
    # update cookie if server set a new one
    if "clicker" in response.cookies:
        cookies["clicker"] = response.cookies["clicker"]
    
    print(f"Click {i+1}:")
    print(f"  Status: {response.status_code}")
    print(f"  Current cookie: {cookies['clicker']}")
