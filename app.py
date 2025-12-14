from mcstatus import MinecraftServer
import requests
import time
import schedule
import os

HOST = "your.minecraftserver.com"
PORT = 25565
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def check_server(host, port=25565):
    try:
        server = MinecraftServer.lookup(f"{host}:{port}")
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
        send_discord_alert(WEBHOOK_URL, f"⚠️ Minecraft server {HOST} is DOWN!")
    else:
        print(f"Server is up with {players} players online.")

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)