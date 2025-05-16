from hashlib import sha256
import json

server_hash_db = {}

for i in range(2 ** 17):
    server_seed = sha256(bytes(i)).hexdigest()
    server_seed_hash = sha256(server_seed.encode()).hexdigest()
    
    for j in range(1000):
        combined = f"{server_seed}:{j}"
        game_hash = sha256(combined.encode()).hexdigest()
        hash_int = int(game_hash, 16)
        if hash_int % 37 == 13:
            server_hash_db[server_seed_hash] = j
            break

with open("sol-server_seeds.json", "w") as f:
    json.dump(server_hash_db, f, indent=2)