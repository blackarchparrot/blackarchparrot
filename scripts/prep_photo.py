import sys
import os
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def prep_photo(input_path: str, output_path: str = "source-prepped.png"):
    if not os.path.exists(input_path):
        print(f"[-] Input file '{input_path}' not found. Creating a synthetic high-contrast hero image...")
        img = np.zeros((400, 400, 3), dtype=np.uint8)
        cv2.putText(img, "SANI", (80, 220), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 8)
        cv2.imwrite("temp_input.png", img)
        input_path = "temp_input.png"

    print("[+] Loading input image...")
    input_img = Image.open(input_path)

    print("[+] Removing background using rembg (U2Net)...")
    nobg_img = remove(input_img)

    nobg_np = np.array(nobg_img)
    if nobg_np.shape[2] == 4:
        b, g, r, a = cv2.split(nobg_np)
    else:
        b, g, r = cv2.split(nobg_np)
        a = np.full(b.shape, 255, dtype=np.uint8)

    gray = cv2.cvtColor(cv2.merge([b, g, r]), cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(gray)

    final_np = cv2.merge([enhanced_gray, enhanced_gray, enhanced_gray, a])
    final_img = Image.fromarray(final_np)

    w, h = final_img.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    cropped = final_img.crop((left, top, left + min_dim, top + min_dim))
    resized = cropped.resize((240, 240), Image.Resampling.LANCZOS)

    resized.save(output_path, "PNG")
    print(f"[+] Successfully saved prepped portrait to '{output_path}'")

    if os.path.exists("temp_input.png"):
        os.remove("temp_input.png")

if __name__ == "__main__":
    src_file = sys.argv[1] if len(sys.argv) > 1 else "hero.png"
    prep_photo(src_file)
