#!/usr/bin/env python3
import sys
import os

# Add clients/python to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "clients", "python")))
from waifus import WaifuClient

def main():
    print("🌸 Initializing WaifuClient...")
    client = WaifuClient()

    # 1. Ping
    ping = client.ping()
    print("📡 Ping:", ping)

    # 2. Database Stats
    stats = client.stats()
    print(f"📊 Total Waifus in Database: {stats.get('total_records', 'Unknown')} ({stats.get('database', '')})")

    # 3. Random Gacha Roll
    print("\n🎲 Pulling a Random Waifu (Gacha)...")
    random_waifu = client.random()
    data = random_waifu.get("data", {})
    print(f"   Name:     {data.get('name')}")
    print(f"   Rarity:   {data.get('rarity')}")
    print(f"   Event:    {data.get('event_tag')}")
    print(f"   Image:    {data.get('img_url')}")

    # 4. Search Waifu
    print("\n🔍 Searching for 'Komi'...")
    search_res = client.find_by_name("Komi")
    if search_res.get("status") == "success":
        s_data = search_res.get("data")
        if isinstance(s_data, list) and len(s_data) > 0:
            for item in s_data[:3]:
                print(f"   Found: {item.get('name')} | Rarity: {item.get('rarity')}")
        elif isinstance(s_data, dict):
            print(f"   Found: {s_data.get('name')} | Rarity: {s_data.get('rarity')}")

if __name__ == "__main__":
    main()
