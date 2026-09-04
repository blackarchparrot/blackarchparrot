import os
import numpy as np
from PIL import Image

ASCII_RAMP = list(" .:-=+*cs#%@")

def image_to_ascii(image_path: str, width: int = 68, height: int = 50) -> list:
    if not os.path.exists(image_path):
        return ["  . :-=+*cs#%@  " * 4 for _ in range(height)]
    
    img = Image.open(image_path).convert("LA")
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    ascii_lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            lum, alpha = img.getpixel((x, y))
            if alpha < 50:
                line += " "
            else:
                idx = int((lum / 255.0) * (len(ASCII_RAMP) - 1))
                line += ASCII_RAMP[idx]
        ascii_lines.append(line)
    return ascii_lines

def generate_ascii_svg():
    lines = image_to_ascii("source-prepped.png", width=68, height=48)
    line_height = 11.5
    start_y = 45
    card_width = 370
    card_height = 580

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {card_width} {card_height}" width="100%" height="100%">
  <defs>
    <linearGradient id="cardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d0d0d"/>
      <stop offset="100%" stop-color="#161616"/>
    </linearGradient>
    <linearGradient id="goldText" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFD700"/>
      <stop offset="100%" stop-color="#D4AF37"/>
    </linearGradient>
    <clipPath id="wipeClip">
      <rect x="0" y="0" width="{card_width}" height="0">
        <animate attributeName="height" from="0" to="{card_height}" dur="2.2s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1.0"/>
      </rect>
    </clipPath>
  </defs>

  <style>
    .terminal-bg {{ fill: url(#cardBg); stroke: #D4AF37; stroke-width: 1.5; rx: 12px; }}
    .dot {{ r: 5.5px; cy: 18px; }}
    .dot-red {{ fill: #FF5F56; cx: 20px; }}
    .dot-yellow {{ fill: #FFBD2E; cx: 38px; }}
    .dot-green {{ fill: #27C93F; cx: 56px; }}
    .header-text {{ font-family: 'Courier New', monospace; font-size: 11px; fill: #888888; font-weight: bold; }}
    .ascii-text {{ font-family: 'Courier New', Monaco, Consolas, monospace; font-size: 9.5px; fill: url(#goldText); white-space: pre; font-weight: 600; letter-spacing: 0.5px; }}
  </style>

  <rect width="{card_width - 2}" height="{card_height - 2}" x="1" y="1" class="terminal-bg"/>
  
  <circle class="dot dot-red"/>
  <circle class="dot dot-yellow"/>
  <circle class="dot dot-green"/>
  <text x="185" y="22" text-anchor="middle" class="header-text">hxni-ascii.matrix</text>
  <line x1="0" y1="32" x2="{card_width}" y2="32" stroke="#222222" stroke-width="1"/>

  <g clip-path="url(#wipeClip)">
    <text x="14" y="{start_y}" class="ascii-text">
'''
    for i, line in enumerate(lines):
        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        svg += f'      <tspan x="14" y="{start_y + i * line_height}">{safe_line}</tspan>\n'

    svg += '''    </text>
  </g>
</svg>'''

    with open("hxni-ascii.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("[+] Successfully generated 'hxni-ascii.svg'")

if __name__ == "__main__":
    generate_ascii_svg()
