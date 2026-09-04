import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_contributions(username: str = "blackarchparrot"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"[+] Scraping contribution calendar for '{username}'...")
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"[-] Failed to fetch data. HTTP {res.status_code}")
        sys.exit(1)

    soup = BeautifulSoup(res.text, "html.parser")
    days = soup.find_all("td", class_="ContributionCalendar-day")

    contributions = []
    total_count = 0
    current_streak = 0
    longest_streak = 0
    best_day = {"date": "", "count": 0}

    temp_streak = 0

    for day in days:
        date = day.get("data-date")
        if not date:
            continue
        
        count = 0
        level = int(day.get("data-level", 0))
        
        id_attr = day.get("id")
        if id_attr:
            tool_tip = soup.find("tool-tip", attrs={"for": id_attr})
            if tool_tip:
                txt = tool_tip.text.strip()
                if "no contribution" not in txt.lower():
                    count = int(txt.split()[0].replace(",", ""))

        contributions.append({
            "date": date,
            "count": count,
            "level": level
        })

        total_count += count
        if count > best_day["count"]:
            best_day = {"date": date, "count": count}

        if count > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    current_streak = temp_streak

    output = {
        "username": username,
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "metrics": {
            "total_contributions": total_count,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "best_day": best_day
        },
        "days": contributions
    }

    import os
    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"[+] Contributions saved! Total: {total_count} | Longest Streak: {longest_streak} days")

if __name__ == "__main__":
    uname = sys.argv[1] if len(sys.argv) > 1 else "blackarchparrot"
    fetch_contributions(uname)
