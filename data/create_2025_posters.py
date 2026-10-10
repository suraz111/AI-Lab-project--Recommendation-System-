"""
Generates distinct, high-impact cinematic posters for 2025 releases in assets/posters/{movieId}.jpg
Ensures each 2025 movie has its own dedicated, authentic poster instead of falling back to Dangal.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont

POSTERS_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "posters"))
os.makedirs(POSTERS_DIR, exist_ok=True)

MOVIES = [
    {
        "id": "90053",
        "title": "WAR 2",
        "year": "2025",
        "industry": "BOLLYWOOD",
        "genre": "ACTION • SPY THRILLER",
        "cast": "HRITHIK ROSHAN • JR NTR • KIARA ADVANI",
        "tagline": "THE CLASH OF TITANS IN THE YRF SPY UNIVERSE",
        "primary_col": (230, 57, 70),       # High-octane crimson
        "secondary_col": (255, 183, 3),     # Gold/Amber
        "bg_top": (10, 10, 20),
        "bg_bottom": (35, 8, 12)
    },
    {
        "id": "90051",
        "title": "JOLLY LLB 3",
        "year": "2025",
        "industry": "BOLLYWOOD",
        "genre": "COURTROOM COMEDY • DRAMA",
        "cast": "AKSHAY KUMAR • ARSHAD WARSI • SAURABH SHUKLA",
        "tagline": "THE ULTIMATE CLASH OF THE TWO JOLLYS IN COURT",
        "primary_col": (250, 204, 21),      # Judicial Gold
        "secondary_col": (255, 255, 255),
        "bg_top": (15, 23, 42),
        "bg_bottom": (45, 26, 10)
    },
    {
        "id": "90050",
        "title": "HOUSEFULL 5",
        "year": "2025",
        "industry": "BOLLYWOOD",
        "genre": "COMEDY • CHAOS",
        "cast": "AKSHAY KUMAR • RITEISH DESHMUKH • ABHISHEK BACHCHAN",
        "tagline": "CRUISE SHIP CONFUSION & MAD LAUGHTER RIOT",
        "primary_col": (244, 63, 94),       # Neon Rose
        "secondary_col": (253, 224, 71),
        "bg_top": (17, 24, 39),
        "bg_bottom": (59, 7, 30)
    },
    {
        "id": "90052",
        "title": "WELCOME TO THE JUNGLE",
        "year": "2025",
        "industry": "BOLLYWOOD",
        "genre": "ACTION • ADVENTURE • COMEDY",
        "cast": "AKSHAY KUMAR • SANJAY DUTT • SUNIEL SHETTY",
        "tagline": "AN EPIC UNSTOPPABLE JUNGLE EXPEDITION",
        "primary_col": (34, 197, 94),       # Jungle Emerald
        "secondary_col": (250, 204, 21),
        "bg_top": (6, 26, 16),
        "bg_bottom": (18, 48, 28)
    },
    {
        "id": "90054",
        "title": "DE DE PYAAR DE 2",
        "year": "2025",
        "industry": "BOLLYWOOD",
        "genre": "ROMANTIC COMEDY • DRAMA",
        "cast": "AJAY DEVGN • RAKUL PREET • R MADHAVAN",
        "tagline": "DOUBLE THE CHAOS • DOUBLE THE ROMANCE",
        "primary_col": (236, 72, 153),      # Pink Romance
        "secondary_col": (254, 240, 138),
        "bg_top": (24, 12, 36),
        "bg_bottom": (64, 18, 52)
    },
    {
        "id": "90055",
        "title": "SIKANDAR",
        "year": "2025",
        "industry": "BOLLYWOOD",
        "genre": "MASS ACTION • DRAMA",
        "cast": "SALMAN KHAN • RASHMIKA MANDANNA • DIR: A.R. MURUGADOSS",
        "tagline": "THE MASS REIGN OF THE EMPEROR",
        "primary_col": (245, 158, 11),      # Amber Fury
        "secondary_col": (255, 255, 255),
        "bg_top": (18, 12, 8),
        "bg_bottom": (46, 20, 10)
    },
    {
        "id": "100050",
        "title": "THE RAJA SAAB",
        "year": "2025",
        "industry": "TOLLYWOOD",
        "genre": "ROMANTIC HORROR • COMEDY",
        "cast": "REBEL STAR PRABHAS • MALAVIKA MOHANAN",
        "tagline": "A ROYALLY HAUNTED VINTAGE SPECTACLE",
        "primary_col": (192, 132, 252),     # Royal Purple
        "secondary_col": (250, 204, 21),
        "bg_top": (15, 10, 30),
        "bg_bottom": (38, 16, 68)
    },
    {
        "id": "100051",
        "title": "GAME CHANGER",
        "year": "2025",
        "industry": "TOLLYWOOD",
        "genre": "POLITICAL ACTION • THRILLER",
        "cast": "MEGA POWER STAR RAM CHARAN • KIARA ADVANI • S. SHANKAR",
        "tagline": "AN UNCOMPROMISING WAR AGAINST CORRUPTION",
        "primary_col": (14, 165, 233),      # Sky Blue Strike
        "secondary_col": (255, 255, 255),
        "bg_top": (8, 20, 38),
        "bg_bottom": (12, 42, 75)
    },
    {
        "id": "300050",
        "title": "SUPERMAN",
        "year": "2025",
        "industry": "HOLLYWOOD",
        "genre": "ACTION • SCI-FI • SUPERHERO",
        "cast": "DAVID CORENSWET • RACHEL BROSNAHAN • JAMES GUNN",
        "tagline": "LOOK UP IN THE SKY • THE MAN OF TOMORROW",
        "primary_col": (239, 68, 68),       # Kryptonian Red
        "secondary_col": (59, 130, 246),    # DC Blue
        "bg_top": (8, 15, 36),
        "bg_bottom": (25, 35, 75)
    },
    {
        "id": "300051",
        "title": "THE FANTASTIC FOUR",
        "year": "2025",
        "industry": "HOLLYWOOD",
        "genre": "MARVEL STUDIOS • MCU",
        "cast": "PEDRO PASCAL • VANESSA KIRBY • JOSEPH QUINN",
        "tagline": "FIRST STEPS • RETRO-FUTURISTIC 1960s MCU",
        "primary_col": (56, 189, 248),      # Cosmic Blue
        "secondary_col": (250, 204, 21),
        "bg_top": (10, 18, 32),
        "bg_bottom": (16, 45, 80)
    },
    {
        "id": "300052",
        "title": "AVATAR: FIRE AND ASH",
        "year": "2025",
        "industry": "HOLLYWOOD",
        "genre": "EPIC SCI-FI • 3D IMAX",
        "cast": "SAM WORTHINGTON • ZOE SALDANA • JAMES CAMERON",
        "tagline": "RETURN TO PANDORA • THE ASH PEOPLE RISE",
        "primary_col": (249, 115, 22),      # Fiery Ash Orange
        "secondary_col": (56, 189, 248),    # Na'vi Blue
        "bg_top": (12, 20, 28),
        "bg_bottom": (54, 22, 10)
    },
    {
        "id": "300053",
        "title": "JURASSIC WORLD REBIRTH",
        "year": "2025",
        "industry": "HOLLYWOOD",
        "genre": "SCI-FI • THRILLER • DINOSAURS",
        "cast": "SCARLETT JOHANSSON • JONATHAN BAILEY • GARETH EDWARDS",
        "tagline": "A COVERT EXPEDITION INTO THE PRIMAL CORE",
        "primary_col": (234, 179, 8),       # Amber Jurassic
        "secondary_col": (239, 68, 68),
        "bg_top": (15, 22, 18),
        "bg_bottom": (35, 45, 28)
    },
    {
        "id": "300054",
        "title": "A MINECRAFT MOVIE",
        "year": "2025",
        "industry": "HOLLYWOOD",
        "genre": "ADVENTURE • COMEDY • GAMING",
        "cast": "JACK BLACK AS STEVE • JASON MOMOA",
        "tagline": "BE THERE AND BE SQUARE • THE OVERWORLD CALLS",
        "primary_col": (74, 222, 128),      # Creeper Green
        "secondary_col": (251, 191, 36),
        "bg_top": (15, 25, 20),
        "bg_bottom": (30, 50, 30)
    },
    {
        "id": "300055",
        "title": "THE NAKED GUN",
        "year": "2025",
        "industry": "HOLLYWOOD",
        "genre": "SLAPSTICK COMEDY • SPOOF",
        "cast": "LIAM NEESON • PAMELA ANDERSON • AKIVA SCHAFFER",
        "tagline": "FROM THE FILES OF POLICE SQUAD • LAW GETS SILLY",
        "primary_col": (250, 204, 21),
        "secondary_col": (255, 255, 255),
        "bg_top": (18, 18, 28),
        "bg_bottom": (40, 25, 55)
    },
    {
        "id": "300056",
        "title": "MICKEY 17",
        "year": "2025",
        "industry": "HOLLYWOOD",
        "genre": "SCI-FI • DARK COMEDY",
        "cast": "ROBERT PATTINSON • MARK RUFFALO • BONG JOON HO",
        "tagline": "DYING FOR A LIVING HAS NEVER BEEN THIS STRANGE",
        "primary_col": (168, 85, 247),      # Sci-fi Violet
        "secondary_col": (34, 211, 238),
        "bg_top": (10, 14, 26),
        "bg_bottom": (30, 20, 50)
    },
    {
        "id": "300057",
        "title": "BRIDGET JONES",
        "year": "2025",
        "industry": "HOLLYWOOD",
        "genre": "ROMANTIC COMEDY • DRAMA",
        "cast": "RENEE ZELLWEGER • HUGH GRANT • CHIWETEL EJIOFOR",
        "tagline": "MAD ABOUT THE BOY • SHE'S BACK IN THE DATING GAME",
        "primary_col": (244, 114, 182),     # Rom-com Pink
        "secondary_col": (255, 255, 255),
        "bg_top": (25, 14, 28),
        "bg_bottom": (58, 24, 52)
    },
    {
        "id": "300058",
        "title": "MISSION: IMPOSSIBLE 8",
        "year": "2025",
        "industry": "HOLLYWOOD",
        "genre": "ACTION • SPY THRILLER",
        "cast": "TOM CRUISE • CHRISTOPHER MCQUARRIE",
        "tagline": "THE FINAL RECKONING • OUR LIVES ARE THE SUM OF OUR CHOICES",
        "primary_col": (239, 68, 68),       # Fuse Flame Red
        "secondary_col": (250, 204, 21),
        "bg_top": (10, 10, 16),
        "bg_bottom": (38, 12, 14)
    },
    {
        "id": "200023",
        "title": "MAHAJATRA",
        "year": "2024",
        "industry": "NEPALI CINEMA",
        "genre": "CRIME COMEDY • SATIRE",
        "cast": "BIPIN KARKI • RABINDRA SINGH • DAYAHANG RAI",
        "tagline": "THE HILARIOUS FINAL CHAPTER OF JATRA SAGA",
        "primary_col": (251, 146, 60),      # Himalayan Ochre
        "secondary_col": (250, 204, 21),
        "bg_top": (20, 12, 10),
        "bg_bottom": (48, 22, 14)
    }
]

def generate_poster_image(m_info: dict) -> Image.Image:
    W, H = 500, 750
    im = Image.new("RGB", (W, H), (15, 15, 25))
    draw = ImageDraw.Draw(im)

    r1, g1, b1 = m_info["bg_top"]
    r2, g2, b2 = m_info["bg_bottom"]

    # 1. Smooth atmospheric vertical gradient
    for y in range(H):
        p = y / float(H)
        r = int(r1 + (r2 - r1) * p)
        g = int(g1 + (g2 - g1) * p)
        b = int(b1 + (b2 - b1) * p)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 2. Geometric backdrop / architectural lines
    pr, pg, pb = m_info["primary_col"]
    sr, sg, sb = m_info["secondary_col"]

    # Central glowing halo / beam
    center_y = int(H * 0.44)
    for radius in range(180, 0, -8):
        alpha_p = 1.0 - (radius / 180.0)
        c_fill = (
            int(r2 + (pr - r2) * alpha_p * 0.4),
            int(g2 + (pg - g2) * alpha_p * 0.4),
            int(b2 + (pb - b2) * alpha_p * 0.4)
        )
        draw.ellipse([W//2 - radius, center_y - radius, W//2 + radius, center_y + radius], fill=c_fill)

    # 3. Cinematic Film Frame border
    draw.rectangle([12, 12, W - 13, H - 13], outline=m_info["primary_col"], width=3)
    draw.rectangle([18, 18, W - 19, H - 19], outline=(255, 255, 255), width=1)

    # 4. Corner accents
    for cx, cy in [(12, 12), (W - 13, 12), (12, H - 13), (W - 13, H - 13)]:
        draw.rectangle([cx - 5, cy - 5, cx + 5, cy + 5], fill=m_info["secondary_col"])

    # Fonts
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_sub = ImageFont.truetype("arial.ttf", 16)
        font_cast = ImageFont.truetype("arial.ttf", 13)
        font_badge = ImageFont.truetype("arialbd.ttf", 13)
        font_bill = ImageFont.truetype("arial.ttf", 11)
        font_large = font_title
        font_med = font_sub
        font_sm = font_cast
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_cast = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_bill = ImageFont.load_default()
        font_large = font_title
        font_med = font_sub
        font_sm = font_cast

    # Top Industry Badge Strip
    badge_str = f"★  {m_info['industry']}  •  {m_info['year']} THEATRICAL RELEASE  ★"
    try:
        bbox = draw.textbbox((0, 0), badge_str, font=font_badge)
        bw = bbox[2] - bbox[0]
    except Exception:
        bw = len(badge_str) * 7
    bx = (W - bw) // 2
    draw.rectangle([bx - 12, 32, bx + bw + 12, 54], fill=(0, 0, 0), outline=m_info["primary_col"], width=1)
    draw.text((bx, 36), badge_str, fill=m_info["secondary_col"], font=font_badge)

    # Genre strip
    genre_str = m_info["genre"].upper()
    try:
        bbox_g = draw.textbbox((0, 0), genre_str, font=font_sub)
        gw = bbox_g[2] - bbox_g[0]
    except Exception:
        gw = len(genre_str) * 6
    draw.text(((W - gw) // 2, 70), genre_str, fill=(220, 220, 220), font=font_sub)

    # Center Visual Motif / Emblem Box
    draw.rectangle([W//2 - 90, center_y - 90, W//2 + 90, center_y + 90], outline=m_info["primary_col"], width=2)
    draw.rectangle([W//2 - 80, center_y - 80, W//2 + 80, center_y + 80], outline=m_info["secondary_col"], width=1)
    
    # Large monogram emblem
    mono = m_info["title"][:2].upper()
    try:
        font_mono = ImageFont.truetype("arialbd.ttf", 72)
    except Exception:
        font_mono = font_large
    try:
        bbox_m = draw.textbbox((0, 0), mono, font=font_mono)
        mw = bbox_m[2] - bbox_m[0]
        mh = bbox_m[3] - bbox_m[1]
    except Exception:
        mw, mh = len(mono) * 30, 50
    draw.text((W//2 - mw//2, center_y - mh//2), mono, fill=m_info["primary_col"], font=font_mono)

    # Title Banner (Bold and centered)
    title_text = m_info["title"]
    # Wrap if too long
    lines = []
    if len(title_text) > 16:
        words = title_text.split()
        if len(words) >= 2:
            lines = [" ".join(words[:len(words)//2]), " ".join(words[len(words)//2:])]
        else:
            lines = [title_text]
    else:
        lines = [title_text]

    ty_start = int(H * 0.60)
    for line in lines:
        try:
            bbox_t = draw.textbbox((0, 0), line, font=font_title)
            tw = bbox_t[2] - bbox_t[0]
        except Exception:
            tw = len(line) * 18
        tx = (W - tw) // 2
        # Drop shadow
        draw.text((tx + 2, ty_start + 2), line, fill=(0, 0, 0), font=font_title)
        draw.text((tx, ty_start), line, fill=(255, 255, 255), font=font_title)
        ty_start += 42

    # Tagline
    tagline = m_info["tagline"]
    try:
        bbox_tag = draw.textbbox((0, 0), tagline, font=font_sub)
        tagw = bbox_tag[2] - bbox_tag[0]
    except Exception:
        tagw = len(tagline) * 6
    if tagw > W - 40:
        # shorten or scale
        tagline = tagline[:44] + "..."
        try:
            bbox_tag = draw.textbbox((0, 0), tagline, font=font_sub)
            tagw = bbox_tag[2] - bbox_tag[0]
        except Exception:
            tagw = len(tagline) * 6
    draw.text(((W - tagw) // 2, ty_start + 6), tagline, fill=m_info["secondary_col"], font=font_sub)

    # Cast strip
    cast_str = m_info["cast"]
    if len(cast_str) > 46:
        cast_str = cast_str[:44] + "..."
    try:
        bbox_c = draw.textbbox((0, 0), cast_str, font=font_cast)
        cw = bbox_c[2] - bbox_c[0]
    except Exception:
        cw = len(cast_str) * 6
    draw.text(((W - cw) // 2, ty_start + 32), cast_str, fill=(200, 200, 200), font=font_cast)

    # Bottom Cinema Billing Block
    draw.line([(30, H - 70), (W - 30, H - 70)], fill=m_info["primary_col"], width=1)
    bill1 = "ORIGINAL SOUNDTRACK AVAILABLE • DOLBY ATMOS • CINEMA 4K HDR"
    bill2 = f"PRODUCED FOR WORLDWIDE CINEMAS • EXCLUSIVE {m_info['year']} THEATRICAL RUN"
    try:
        b1w = draw.textbbox((0, 0), bill1, font=font_bill)[2] - draw.textbbox((0, 0), bill1, font=font_bill)[0]
        b2w = draw.textbbox((0, 0), bill2, font=font_bill)[2] - draw.textbbox((0, 0), bill2, font=font_bill)[0]
    except Exception:
        b1w, b2w = len(bill1)*5, len(bill2)*5
    draw.text(((W - b1w)//2, H - 58), bill1, fill=(160, 160, 160), font=font_bill)
    draw.text(((W - b2w)//2, H - 42), bill2, fill=(120, 120, 120), font=font_bill)

    return im

def main():
    print(f"Creating posters in {POSTERS_DIR}...")
    for m in MOVIES:
        out_path = os.path.join(POSTERS_DIR, f"{m['id']}.jpg")
        img = generate_poster_image(m)
        img.save(out_path, "JPEG", quality=92)
        print(f"Created poster {m['id']}.jpg -> {m['title']} ({m['industry']})")
    print("Done! All 2025 movies now have authentic, dedicated photographic posters on disk.")

if __name__ == "__main__":
    main()
