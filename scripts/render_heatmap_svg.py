import json
import os

COLOR_MAP = {
    0: "#161616",
    1: "#3a2e05",
    2: "#735c09",
    3: "#b8930c",
    4: "#FFD700"
}

def render_heatmap():
    json_path = "data/contributions.json"
    if not os.path.exists(json_path):
        print("[-] Contributions data not found. Run fetch_contributions.py first.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    metrics = data.get("metrics", {})

    width = 860
    height = 210
    box_size = 11
    box_gap = 3.5
    start_x = 35
    start_y = 65

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d0d0d"/>
      <stop offset="100%" stop-color="#181818"/>
    </linearGradient>
  </defs>

  <style>
    .bg {{ fill: url(#bgGrad); stroke: #D4AF37; stroke-width: 1.2; rx: 10px; }}
    .title {{ font-family: 'Courier New', monospace; font-size: 13px; fill: #FFD700; font-weight: bold; }}
    .metric-title {{ font-family: 'Segoe UI', sans-serif; font-size: 10px; fill: #888888; }}
    .metric-val {{ font-family: 'Courier New', monospace; font-size: 14px; fill: #FFFFFF; font-weight: bold; }}
    .day-box {{ rx: 2px; transition: all 0.2s; }}
    .day-box:hover {{ stroke: #FFFFFF; stroke-width: 1px; }}
    .label {{ font-family: sans-serif; font-size: 9px; fill: #666666; }}
  </style>

  <rect width="{width - 2}" height="{height - 2}" x="1" y="1" class="bg"/>

  <text x="20" y="32" class="title">⚡ ACTIVITY HEATMAP</text>

  <g transform="translate(380, 18)">
    <text x="0" y="10" class="metric-title">TOTAL</text>
    <text x="0" y="26" class="metric-val">{metrics.get('total_contributions', 0):,}</text>
  </g>

  <g transform="translate(500, 18)">
    <text x="0" y="10" class="metric-title">CURRENT STREAK</text>
    <text x="0" y="26" class="metric-val">{metrics.get('current_streak', 0)} days</text>
  </g>

  <g transform="translate(640, 18)">
    <text x="0" y="10" class="metric-title">LONGEST STREAK</text>
    <text x="0" y="26" class="metric-val">{metrics.get('longest_streak', 0)} days</text>
  </g>

  <line x1="20" y1="48" x2="{width - 20}" y2="48" stroke="#222222" stroke-width="1"/>
'''

    col = 0
    row = 0
    for day in days:
        x = start_x + (col * (box_size + box_gap))
        y = start_y + (row * (box_size + box_gap))
        level = day.get("level", 0)
        color = COLOR_MAP.get(level, COLOR_MAP[0])

        svg += f'  <rect x="{x:.1f}" y="{y:.1f}" width="{box_size}" height="{box_size}" fill="{color}" class="day-box"><title>{day["date"]}: {day["count"]} contributions</title></rect>\n'

        row += 1
        if row >= 7:
            row = 0
            col += 1

    svg += f'''
  <g transform="translate({width - 150}, {height - 20})">
    <text x="-30" y="9" class="label">Less</text>
    <rect x="0" y="0" width="10" height="10" fill="{COLOR_MAP[0]}" rx="2"/>
    <rect x="14" y="0" width="10" height="10" fill="{COLOR_MAP[1]}" rx="2"/>
    <rect x="28" y="0" width="10" height="10" fill="{COLOR_MAP[2]}" rx="2"/>
    <rect x="42" y="0" width="10" height="10" fill="{COLOR_MAP[3]}" rx="2"/>
    <rect x="56" y="0" width="10" height="10" fill="{COLOR_MAP[4]}" rx="2"/>
    <text x="72" y="9" class="label">More</text>
  </g>
</svg>'''

    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("[+] Successfully generated 'contrib-heatmap.svg'")

if __name__ == "__main__":
    render_heatmap()
