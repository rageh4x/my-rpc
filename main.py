import json
import websocket
import threading
import time

TOKEN = "MTM3Njk1Mzc2ODYXNjEzMjYjYOMA.GBijKN.KdtmouadKHwkQE_dEdQtAsVwXsAN2SyKjeIYKE"
CLIENT_ID = "1552641681617326110"

def run_rpc():
    while True:
        try:
            ws_url = "wss://gateway.discord.gg/?v=10&encoding=json"
            ws = websocket.create_connection(ws_url)
            
            event = json.loads(ws.recv())
            heartbeat_interval = event['d']['heartbeat_interval'] / 1000

            def heartbeat(interval, ws_conn):
                while True:
                    time.sleep(interval)
                    try:
                        ws_conn.send(json.dumps({"op": 1, "d": None}))
                    except:
                        break

            threading.Thread(target=heartbeat, args=(heartbeat_interval, ws), daemon=True).start()

            identify_payload = {
                "op": 2,
                "d": {
                    "token": TOKEN,
                    "properties": {
                        "os": "Windows",
                        "browser": "Chrome",
                        "device": ""
                    }
                }
            }
            ws.send(json.dumps(identify_payload))

            presence_payload = {
                "op": 3,
                "d": {
                    "since": int(time.time() * 1000),
                    "activities": [{
                        "name": "Fast Client",
                        "type": 0,  # 0 = Playing
                        "state": "In Game",
                        "details": "Playing Minecraft 1.21.11",
                        "application_id": CLIENT_ID,
                        "timestamps": {
                            "start": int(time.time())
                        }
                    }],
                    "status": "online",
                    "afk": False
                }
            }
            
            time.sleep(2)
            ws.send(json.dumps(presence_payload))
            print("RPC Successfully Connected and Active!")

            while True:
                time.sleep(1)
        except Exception as e:
            print(f"Error: {e}, Reconnecting in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    run_rpc()
