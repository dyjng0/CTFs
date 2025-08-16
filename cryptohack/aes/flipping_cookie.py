import requests


def check_admin(cookie, iv):
    r = requests.get(
        f"https://aes.cryptohack.org/flipping_cookie/check_admin/{cookie}/{iv}/"
    )
    check = r.json()
    if "flag" in check:
        return check["flag"]
    else:
        return check["error"]


def get_cookie():
    r = requests.get('https://aes.cryptohack.org/flipping_cookie/get_cookie')
    return r.json()['cookie']

# admin=Fa
# lse;expi
# ry={expires_at}
