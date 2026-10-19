"""Turn the client's mannequin studio shots into two gallery photos per wig: front and back, each centred.

    python src/tools/import_mannequins.py "D:/Work/Chesed Hair/Images/Assets - Chesed Hair/Hair Styles"

Writes assets/p/<handle>-7-mannequin-front-{1024,560}.webp and <handle>-8-mannequin-back-{1024,560}.webp.
Needs Pillow, numpy and opencv-python-headless (the face finder tells the front shot from the back shot).
Shots the script can't sort out on its own are listed in PICKS below (checked by eye).
"""
import os, re, sys
import numpy as np, cv2
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "assets", "p")
STYLES = {"Body Wave": "body-wave", "Curly": "curly", "Kinky Straight": "kinky-straight",
          "Loose Deep": "loose-deep-wave", "Straight": "straight", "Virgin Curl": "virgin-curl"}
COLORS = {"1": "1", "1B": "1b", "350": "350", "530": "530", "99J": "99j", "HA": "honey-auburn", "HB": "honey-blonde",
          "NA": "natural-auburn", "Red": "red", "Virgin": "virgin"}
# (style, color folder) -> (front file, back file), where the folder has more than one pair or a different naming
PICKS = {
    ("Body Wave", "99J"): ("DSC00042-3.jpg", "DSC00033-4.jpg"),
    ("Body Wave", "Red"): ("DSC00003-9.jpg", "DSC00001-11.jpg"),
    ("Curly", "Virgin"): ("DSC00025-13.jpg", "DSC00021-13.jpg"),
    ("Kinky Straight", "Virgin"): ("DSC00068-2.jpg", "DSC00056-4.jpg"),
    ("Straight", "Virgin"): ("DSC00004-12 copy.jpg", "DSC00011-10 copy.jpg"),
    ("Virgin Curl", "1"): ("DSC_0810-2 copy.jpg", "DSC_0805-2 copy.jpg"),
    ("Virgin Curl", "1B"): ("DSC_0814-2 copy.jpg", "DSC_0813-2 copy.jpg"),
    ("Virgin Curl", "Virgin"): ("Color Logo.jpg", "IMG_2187.jpg"),
}
FACE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def small(path, w=600):
    """A reduced copy for measuring, and its scale relative to the full-size file."""
    im = Image.open(path); full_w = im.width
    im.draft("RGB", (w, w * 3)); im = im.convert("RGB")
    return im, im.width / full_w

def face_score(path):
    """How face-like the best match in the photo is (0 when nothing is found). Back shots score low or zero."""
    im, _ = small(path)
    g = cv2.cvtColor(np.asarray(im.resize((500, int(500 * im.height / im.width)))), cv2.COLOR_RGB2GRAY)
    _, _, weights = FACE.detectMultiScale3(g, 1.1, 3, minSize=(40, 40), outputRejectLevels=True)
    return float(max(weights)) if len(weights) else 0.0

def pair_in(folder):
    fs = [f for f in sorted(os.listdir(folder)) if f.startswith("DSC0") and "copy" not in f and not re.search(r"[ab]\.jpg$", f)]
    fs = [f for f in fs if (lambda s: s[1] >= 1.5 * s[0])(Image.open(os.path.join(folder, f)).size)]
    return fs

def wig_box(arr):
    """Bounding box (x0, y0, x1, y1) of the wig and bust: everything that differs from the plain backdrop. The thin stand is ignored."""
    h, w, _ = arr.shape
    edge = max(2, int(w * .04))
    bg = np.concatenate([arr[:, edge:edge * 2], arr[:, -edge * 2:-edge]], axis=1).astype(int).mean(axis=1)   # backdrop colour per row
    diff = np.abs(arr.astype(int) - bg[:, None, :]).max(axis=2) > 28
    diff[:, :edge] = diff[:, -edge:] = False
    cols = np.where(diff.sum(axis=0) > h * .03)[0]
    x0, x1 = cols.min(), cols.max()
    rows = np.where(diff[:, x0:x1 + 1].sum(axis=1) > w * .08)[0]      # the stand is narrower than this, so it drops out
    return x0, rows.min(), x1, rows.max()

def centred(path, size=(1024, 1536)):
    im, k = small(path, 700)
    arr = np.asarray(im)
    x0, y0, x1, y1 = wig_box(arr)
    full = Image.open(path).convert("RGB")
    s = 1 / k
    x0, y0, x1, y1 = [v * s for v in (x0, y0, x1, y1)]
    bw, bh = x1 - x0, y1 - y0
    cw = bw * 1.28; ch = cw * 1.5
    if ch < bh * 1.12: ch = bh * 1.12; cw = ch / 1.5
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    # stay inside the photo, away from its edges (a few shots are slightly rotated and have blank wedges in the corners)
    rx0, ry0, rx1, ry1 = full.width * .06, full.height * .04, full.width * .94, full.height * .96
    z = min(1.0, (rx1 - rx0) / cw, (ry1 - ry0) / ch)
    cw, ch = cw * z, ch * z
    cx = min(max(cx, rx0 + cw / 2), rx1 - cw / 2)
    cy = min(max(cy, ry0 + ch / 2), ry1 - ch / 2)
    left, top = int(round(cx - cw / 2)), int(round(cy - ch / 2))
    box = (left, top, int(round(left + cw)), int(round(top + ch)))
    bgc = tuple(int(v) for v in np.median(np.asarray(full.crop((0, 0, full.width, 40))).reshape(-1, 3), axis=0))
    canvas = Image.new("RGB", (box[2] - box[0], box[3] - box[1]), bgc)
    src = (max(0, box[0]), max(0, box[1]), min(full.width, box[2]), min(full.height, box[3]))
    canvas.paste(full.crop(src), (src[0] - box[0], src[1] - box[1]))
    return canvas.resize(size, Image.LANCZOS)

def save(im, name):
    im.save(os.path.join(OUT, f"{name}-1024.webp"), "WEBP", quality=84, method=6)
    im.resize((560, 840), Image.LANCZOS).save(os.path.join(OUT, f"{name}-560.webp"), "WEBP", quality=82, method=6)

def main(src, dry=False):
    n, review = 0, []
    for style, tslug in STYLES.items():
        for cdir, cslug in COLORS.items():
            folder = os.path.join(src, style, cdir)
            if not os.path.isdir(folder):
                continue
            if (style, cdir) in PICKS:
                front, back = PICKS[(style, cdir)]
            else:
                fs = pair_in(folder)
                if len(fs) != 2:
                    continue
                f0, f1 = face_score(os.path.join(folder, fs[0])), face_score(os.path.join(folder, fs[1]))
                if abs(f0 - f1) < 0.3:
                    review.append((style, cdir, fs, f0, f1)); continue
                front, back = (fs[0], fs[1]) if f0 > f1 else (fs[1], fs[0])
            handle = f"{cslug}-{tslug}-lace-front-wig"
            print(f"{handle}: front={front} back={back}")
            if not dry:
                save(centred(os.path.join(folder, front)), f"{handle}-7-mannequin-front")
                save(centred(os.path.join(folder, back)), f"{handle}-8-mannequin-back")
            n += 1
    print(f"Wrote front and back mannequin photos for {n} wigs")
    for r in review: print("NEEDS A LOOK:", r)

if __name__ == "__main__":
    main(sys.argv[1], dry="--dry" in sys.argv)
