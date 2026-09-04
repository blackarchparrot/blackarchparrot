def generate_info_card():
    card_width = 490
    card_height = 580

    items = [
        ("USER", "Aftab Ahammad Sani (blackarchparrot)"),
        ("OS", "Arch Linux x86_64 / macOS Sonoma"),
        ("HOST", "Dhaka, Bangladesh (UTC+06:00)"),
        ("ROLE", "AI/ML Developer & Full-Stack Engineer"),
        ("FOCUS", "LLM Pipelines, 3D Web & Distributed Systems"),
        ("FRONTEND", "React, TypeScript, Vite, Tailwind, Three.js"),
        ("BACKEND", "Node.js, Express, Python, MySQL, Supabase"),
        ("MOBILE", "React Native, Kotlin"),
        ("TOOLS", "Git, Docker, Postman, Vercel, Cloudflare"),
        ("EMAIL", "blackparrotfedora@gmail.com"),
        ("PORTFOLIO", "three-bugs-portfolio.vercel.app/sunny.html"),
        ("STATUS", "⚡ Open to High-Impact Opportunities")
    ]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {card_width} {card_height}" width="100%" height="100%">
  <defs>
    <linearGradient id="infoBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d0d0d"/>
      <stop offset="100%" stop-color="#141414"/>
    </linearGradient>
  </defs>

  <style>
    .card-bg {{ fill: url(#infoBg); stroke: #D4AF37; stroke-width: 1.5; rx: 12px; }}
    .dot {{ r: 5.5px; cy: 18px; }}
    .dot-red {{ fill: #FF5F56; cx: 20px; }}
    .dot-yellow {{ fill: #FFBD2E; cx: 38px; }}
    .dot-green {{ fill: #27C93F; cx: 56px; }}
    .header-text {{ font-family: 'Courier New', monospace; font-size: 11px; fill: #888888; font-weight: bold; }}
    
    .lbl {{ font-family: 'Courier New', Monaco, monospace; font-size: 11.5px; fill: #FFD700; font-weight: bold; }}
    .val {{ font-family: 'Segoe UI', Ubuntu, sans-serif; font-size: 11.5px; fill: #E0E0E0; font-weight: 500; }}
    .prompt {{ font-family: monospace; font-size: 12px; fill: #27C93F; font-weight: bold; }}

    .row {{ opacity: 0; animation: fadeIn 0.4s ease-out forwards; }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(4px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>

  <rect width="{card_width - 2}" height="{card_height - 2}" x="1" y="1" class="card-bg"/>
  
  <circle class="dot dot-red"/>
  <circle class="dot dot-yellow"/>
  <circle class="dot dot-green"/>
  <text x="{card_width // 2}" y="22" text-anchor="middle" class="header-text">The Cipher Stack v2.4.0</text>
  <line x1="0" y1="32" x2="{card_width}" y2="32" stroke="#222222" stroke-width="1"/>

  <text x="20" y="58" class="prompt">blackarchparrot@dhaka-node:~$ <tspan fill="#FFFFFF">neofetch --sysinfo</tspan></text>
'''

    start_y = 90
    y_gap = 38

    for i, (key, val) in enumerate(items):
        delay = 0.15 + (i * 0.1)
        y_pos = start_y + (i * y_gap)
        svg += f'''  <g class="row" style="animation-delay: {delay:.2f}s;">
    <text x="20" y="{y_pos}">
      <tspan class="lbl">{key}:</tspan>
      <tspan x="125" class="val">{val}</tspan>
    </text>
    <line x1="20" y1="{y_pos + 10}" x2="{card_width - 20}" y2="{y_pos + 10}" stroke="#1f1f1f" stroke-width="1"/>
  </g>\n'''

    last_y = start_y + (len(items) * y_gap) + 15
    svg += f'''  <text x="20" y="{last_y}" class="prompt">blackarchparrot@dhaka-node:~$ <tspan fill="#FFD700">█</tspan></text>
</svg>'''

    with open("info-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("[+] Successfully generated 'info-card.svg'")

if __name__ == "__main__":
    generate_info_card()
