"""Convert the client's mannequin photos (front and back on a stand) into gallery images.

    python src/tools/import_mannequins.py "D:/Work/Chesed Hair/Images/Assets - Chesed Hair/Hair Styles"

Writes assets/p/<handle>-7-mannequin-1024.webp and -560.webp for every wig that has a source photo.
The 13x5 lace variants are skipped (they are not separate products on the site).
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "assets", "p")
STYLES = {"Body Wave": "body-wave", "Curly": "curly", "Kinky Curly": "kinky-curly", "Kinky Straight": "kinky-straight",
          "Loose Deep": "loose-deep-wave", "Straight": "straight", "Virgin Curl": "virgin-curl"}
COLORS = {"1": "1", "1B": "1b", "350": "350", "530": "530", "99J": "99j", "HA": "honey-auburn", "HB": "honey-blonde",
          "NA": "natural-auburn", "Red": "red", "Virgin": "virgin"}

def main(src):
    n = 0
    for style, tslug in STYLES.items():
        for cdir, cslug in COLORS.items():
            folder = os.path.join(src, style, cdir)
            if not os.path.isdir(folder):
                continue
            files = [f for f in os.listdir(folder) if f.startswith("#") and f.lower().endswith(".jpg")]
            if not files:
                continue
            im = Image.open(os.path.join(folder, files[0])).convert("RGB")
            for w in (1024, 560):
                im.resize((w, w), Image.LANCZOS).save(os.path.join(OUT, f"{cslug}-{tslug}-lace-front-wig-7-mannequin-{w}.webp"), "WEBP", quality=82, method=6)
            n += 1
    print(f"Wrote mannequin photos for {n} wigs")

if __name__ == "__main__":
    main(sys.argv[1])
