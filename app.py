import requests
import time
import schedule
from dotenv import load_dotenv
import os
from mcstatus import JavaServer

# load_dotenv() Not needed for railway deployment
HOST = os.getenv("MINECRAFT_SERVER_HOST")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
PORT = os.getenv("MINECRAFT_SERVER_PORT")

def check_server(HOST, PORT):
    try:
        server = JavaServer.lookup(f"{HOST}:{PORT}")
        status = server.status()
        return True, status.players.online
    except Exception:
        return False, None
    
def send_discord_alert(webhook_url, message):
    data = {"content": message}
    requests.post(webhook_url, json=data)

def job():
    is_up, players = check_server(HOST, PORT)
    if not is_up:
        send_discord_alert(WEBHOOK_URL, f"Pat the minecraft server is down again, when will this end?")
    else:
        print(f"Server is up with {players} players online.")

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)