"""Turn the client's mannequin studio shots into two gallery photos per wig: front and back, cut out, centred on a plain background.

    python src/tools/import_mannequins.py "D:/Work/Chesed Hair/Images/Assets - Chesed Hair/Hair Styles"

Writes assets/p/<handle>-7-mannequin-front-{1024,560}.webp and <handle>-8-mannequin-back-{1024,560}.webp.
Needs Pillow, numpy, opencv-python-headless (the face finder tells the front shot from the back shot)
and rembg[cpu] (cuts the wig and bust out of the studio backdrop; downloads its model on first run).
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

BG = (243, 242, 241)          # the site's --pearl, so the photos sit flush on the page
SIZE = (1024, 1536)
_session = None

def drop_stand(alpha):
    """Remove the metal stand under the bust: everything below the lowest hair or bust pixel that sits outside the stand's column."""
    a = alpha > 128
    h, w = a.shape
    bottom = np.where(a[int(h * .97):].any(axis=0))[0]
    if not len(bottom) or (bottom.max() - bottom.min()) > w * .12:
        return alpha                              # nothing narrow touches the bottom edge (e.g. a torso form): no stand
    x0, x1 = bottom.min(), bottom.max()
    pad = max(int((x1 - x0) * 1.6), int(w * .03))
    out = a.copy(); out[:, max(0, x0 - pad):x1 + pad + 1] = False
    rows = np.where(out.sum(axis=1) > w * .004)[0]
    if not len(rows):
        return alpha
    alpha = alpha.copy(); alpha[rows.max() + 1:, :] = 0
    return alpha

def centred(path):
    """Cut the wig and bust out of the studio shot, drop the stand, and centre it on the plain background."""
    global _session
    from rembg import remove, new_session
    if _session is None:
        _session = new_session("birefnet-general-lite")
    im = Image.open(path); im.draft("RGB", (1400, 2800)); im = im.convert("RGB")
    if im.height > 2400:
        im = im.resize((int(im.width * 2400 / im.height), 2400), Image.LANCZOS)
    cut = remove(im, session=_session)
    alpha = drop_stand(np.asarray(cut.split()[3]))
    rows, cols = np.where(alpha > 40)
    y0, y1, x0, x1 = rows.min(), rows.max(), cols.min(), cols.max()
    sub = cut.crop((x0, y0, x1 + 1, y1 + 1)); sub.putalpha(Image.fromarray(alpha[y0:y1 + 1, x0:x1 + 1]))
    k = min(SIZE[0] * .80 / sub.width, SIZE[1] * .84 / sub.height)
    sub = sub.resize((max(1, int(sub.width * k)), max(1, int(sub.height * k))), Image.LANCZOS)
    canvas = Image.new("RGB", SIZE, BG)
    canvas.paste(sub, ((SIZE[0] - sub.width) // 2, (SIZE[1] - sub.height) // 2), sub)
    return canvas

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
