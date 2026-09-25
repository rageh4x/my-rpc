import time
from pypresence import Presence

# Aapki Discord Application ki Client ID yahan set hai
client_id = "1552641681617326110" 
RPC = Presence(client_id)

try:
    RPC.connect()
    print("Connected!")
    
    while True:
        RPC.update(
            state="Playing Game",
            details="Custom 24/7 RPC",
            start=time.time()
        )
        time.sleep(15)
except Exception as e:
    print(e)
