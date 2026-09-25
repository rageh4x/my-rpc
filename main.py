import json
import websocket
import threading
import time

# Apni Discord App ki Client ID yahan dalein
CLIENT_ID = "1552641681617326110"

def run_rpc():
    while True:
        try:
            # Discord Gateway WebSocket URL
            ws_url = "wss://gateway.discord.gg/?v=10&encoding=json"
            ws = websocket.create_connection(ws_url)
            
            # Hello payload ka wait karein
            event = json.loads(ws.recv())
            heartbeat_interval = event['d']['heartbeat_interval'] / 1000

            # Heartbeat thread start karein taaki connection zinda rahe
            def heartbeat(interval, ws_conn):
                while True:
                    time.sleep(interval)
                    try:
                        ws_conn.send(json.dumps({"op": 1, "d": None}))
                    except:
                        break

            threading.Thread(target=heartbeat, args=(heartbeat_interval, ws), daemon=True).start()

            # Presence (Rich Presence) payload bhejein
            payload = {
                "op": 3,
                "d": {
                    "since": int(time.time() * 1000),
                    "activities": [{
                        "name": "Custom RPC",
                        "type": 0,  # 0 matlab Playing
                        "state": "Free Fire khel raha hu",
                        "details": "Rank Push",
                        "application_id": CLIENT_ID,
                        "timestamps": {
                            "start": int(time.time())
                        }
                    }],
                    "status": "online",
                    "afk": False
                }
            }
            
            ws.send(json.dumps(payload))
            print("RPC Successfully Connected and Active!")

            while True:
                time.sleep(1)
        except Exception as e:
            print(f"Error: {e}, Reconnecting in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    run_rpc()
