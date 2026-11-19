"""Extraction des prédications PDF -> library.json pour l'application Man Child Ministry."""
import json, re, sys, unicodedata, warnings
warnings.filterwarnings("ignore")
import pymupdf  # pip install pymupdf
from pathlib import Path

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])

JOURS = {"lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"}

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

# ---------- Livres bibliques (FR) ----------
BOOKS = [
 ("Genèse",["genese"]),("Exode",["exode"]),("Lévitique",["levitique"]),("Nombres",["nombres"]),
 ("Deutéronome",["deuteronome"]),("Josué",["josue"]),("Juges",["juges"]),("Ruth",["ruth"]),
 ("1 Samuel",["1 samuel","premier samuel"]),("2 Samuel",["2 samuel","deuxieme samuel"]),
 ("1 Rois",["1 rois"]),("2 Rois",["2 rois"]),("1 Chroniques",["1 chroniques"]),("2 Chroniques",["2 chroniques"]),
 ("Esdras",["esdras"]),("Néhémie",["nehemie"]),("Esther",["esther"]),("Job",["job"]),
 ("Psaumes",["psaumes","psaume"]),("Proverbes",["proverbes"]),("Ecclésiaste",["ecclesiaste"]),
 ("Cantique des cantiques",["cantique des cantiques"]),("Ésaïe",["esaie","isaie"]),("Jérémie",["jeremie"]),
 ("Lamentations",["lamentations"]),("Ézéchiel",["ezechiel"]),("Daniel",["daniel"]),("Osée",["osee"]),
 ("Joël",["joel"]),("Amos",["amos"]),("Abdias",["abdias"]),("Jonas",["jonas"]),("Michée",["michee"]),
 ("Nahum",["nahum"]),("Habacuc",["habacuc"]),("Sophonie",["sophonie"]),("Aggée",["aggee"]),
 ("Zacharie",["zacharie"]),("Malachie",["malachie"]),
 ("Matthieu",["matthieu"]),("Marc",["marc"]),("Luc",["luc"]),("Jean",["jean"]),("Actes",["actes"]),
 ("Romains",["romains"]),("1 Corinthiens",["1 corinthiens","premier corinthiens"]),
 ("2 Corinthiens",["2 corinthiens","deuxieme corinthiens"]),("Galates",["galates"]),
 ("Éphésiens",["ephesiens"]),("Philippiens",["philippiens"]),("Colossiens",["colossiens"]),
 ("1 Thessaloniciens",["1 thessaloniciens"]),("2 Thessaloniciens",["2 thessaloniciens"]),
 ("1 Timothée",["1 timothee"]),("2 Timothée",["2 timothee"]),("Tite",["tite"]),("Philémon",["philemon"]),
 ("Hébreux",["hebreux"]),("Jacques",["jacques"]),("1 Pierre",["1 pierre"]),("2 Pierre",["2 pierre"]),
 ("1 Jean",["1 jean"]),("2 Jean",["2 jean"]),("3 Jean",["3 jean"]),("Jude",["jude"]),
 ("Apocalypse",["apocalypse"]),
]
alias = {}
for name, al in BOOKS:
    for a in al: alias[a] = name
alts = sorted(alias, key=len, reverse=True)
NUMW = {"un":1,"une":1,"deux":2,"trois":3,"quatre":4,"cinq":5,"six":6,"sept":7,"huit":8,"neuf":9,"dix":10,"onze":11,"douze":12,"treize":13,"quatorze":14,"quinze":15,"seize":16,"vingt":20}
NUM = r"(\d{1,3}|" + "|".join(NUMW) + r")\b"
alias.update({"romain":"Romains","psaume":"Psaumes","esaie":"Ésaïe"})
alts = sorted(alias, key=len, reverse=True)
REF_RE = re.compile(r"\b(" + "|".join(re.escape(a) for a in alts) + r")\b,?\s+(?:le\s+|au\s+)?(chapitre\s+)?" + NUM + r"(?:\s*[:,.]?\s*(?:le\s+|au\s+)?(?:versets?\s+|v\.?\s*)" + NUM + r"|\s*[:,.]\s*(\d{1,3})\b)?")
def tonum(x):
    return int(x) if x and x.isdigit() else NUMW.get(x)

def find_refs(text):
    n = norm(text)
    refs = []
    for m in REF_RE.finditer(n):
        book = alias[m.group(1)]
        # "Jean", "Marc", "Luc", "Jacques", "Daniel"... sont aussi des prénoms : exiger "chapitre" ou ":"
        ch = tonum(m.group(3)); v = tonum(m.group(4) or m.group(5))
        explicit = bool(m.group(2)) or "verset" in m.group(0) or ":" in m.group(0)
        if not m.group(3).isdigit() and not m.group(2): continue
        if book in ("Jean","Marc","Luc","Jacques","Daniel","Jude","Job","Amos","Ruth","Esther","Tite","Actes","Juges","Nombres") and not explicit:
            continue
        if not ch or ch > 150: continue
        refs.append(f"{book} {ch}" + (f":{v}" if v else ""))
    return refs

# ---------- Thèmes ----------
THEMES = [
 ("melchisedech","Ordre de Melchisédech",["melchisedech","melchisedek","roi de salem"]),
 ("enfant-male","L'enfant mâle",["enfant-male","enfant male","enfants males","fils manifestes","fils de dieu manifest"]),
 ("tonnerres","Les sept tonnerres",["sept tonnerres","7 tonnerres","tonnerre"]),
 ("sceaux","Le 7ème sceau",["septieme sceau","7eme sceau","7e sceau","sceau"]),
 ("pierre-faite","La Pierre de faîte",["pierre de faite","pierre angulaire","capstone","head stone"]),
 ("gloire","Gloire et corps glorifié",["glorifie","corps glorieux","gloire","transfigur"]),
 ("immortalite","Immortalité et vie éternelle",["immortalit","ne mourra","mourir plus","vie eternelle","arbre de vie","incorruptib"]),
 ("feu","Le feu de Dieu",["feu"]),
 ("lumiere","La lumière",["lumiere"]),
 ("plenitude","Plénitude des temps",["plenitude","dispensation"]),
 ("vengeance","Le jour de vengeance",["vengeance","jugement"]),
 ("epouse","L'Épouse de Christ",["epouse"]),
 ("ministere","Ministères (apôtre, prophète…)",["quintuple","apostolique","prophetique","apotre","prophete"]),
 ("branham","Frère Branham et le message",["branham","prophete du temps"]),
 ("adam","Adam et la chute",["adam","eden","chute"]),
 ("priere","Prière et adoration",["priere","prions","adorons","adorez"]),
]
def theme_scores(text):
    n = norm(text)
    return {tid: sum(n.count(k) for k in kws) for tid, _, kws in THEMES}

# ---------- Lecture PDF ----------
def pdf_text(pdf):
    pages = []
    for page in pymupdf.open(pdf):
        lines = [l.strip() for l in page.get_text(sort=True).splitlines()]
        # pied de page "Titre        12" -> deux lignes "Titre" / "12"
        for k in range(len(lines) - 1, -1, -1):
            if lines[k]:
                m = re.match(r"^(.*\S)\s{2,}(\d{1,3})$", lines[k])
                if m: lines[k:k+1] = [m.group(1), "", m.group(2)]
                break
        pages.append("\n".join(lines))
    return "\f".join(pages)

def docx_text(path):
    import docx  # pip install python-docx
    return "\n".join(p.text.strip() for p in docx.Document(path).paragraphs)

# ---------- Parsing ----------
def parse(pdf):
    raw = docx_text(pdf) if pdf.suffix.lower() == ".docx" else pdf_text(pdf)
    pages = raw.split("\f")
    lines_all = raw.splitlines()
    series = lines_all[0].strip()
    # en-tête : jusqu'à la ligne de soulignés
    head = []
    i = 1
    while i < len(lines_all) and not lines_all[i].startswith("____") and len(head) < 8:
        if lines_all[i].strip(): head.append(lines_all[i].strip())
        if re.search(r"(?i)\b(19|20)\d\d\b", lines_all[i]) and any(h.lower().startswith("pasteur") for h in head):
            # ligne de date atteinte : la suivante est le lieu
            j = i + 1
            while j < len(lines_all) and not lines_all[j].strip(): j += 1
            if j < len(lines_all) and not lines_all[j].startswith("____"): head.append(lines_all[j].strip())
            i = j
            break
        i += 1
    # head = [TITRE (1-2 lignes)..., Pasteur..., Jour moment, date, Lieu]
    idx_p = next(k for k, l in enumerate(head) if l.lower().startswith("pasteur"))
    title_upper = " ".join(head[:idx_p])
    preacher = head[idx_p]
    when = head[idx_p + 1]
    place_raw = head[idx_p + 2] if len(head) > idx_p + 2 else ""
    parts = [x.strip() for x in re.split(r"\s+_\s+|,\s*", place_raw) if x.strip()]
    loc = parts[-1] if parts else ""
    venue = ", ".join(parts[:-1])
    city, _, country = loc.partition("-")
    city, country = city.strip(), country.strip().replace("’", "'")
    place = ", ".join(x for x in [venue, city, country] if x)

    # titre lisible : depuis le nom de fichier (casse correcte)
    stem = pdf.stem
    m = re.match(r"(\d{4}) (\d{2})(\d{2})([MS])\s+(.*?)\s+_\s+(.*)$", stem)
    year, mm, dd, ms, ftitle, _ = m.groups()
    sid = f"{year}-{mm}-{dd}{ms}"
    body_lines = []
    footer_title = None
    for p_i, page in enumerate(pages):
        pl = [l.rstrip() for l in page.splitlines()]
        if any(l.replace(" ", "").startswith("Cemessagedu") for l in [x for x in pl if x.strip()][:6]):
            break  # colophon
        # retirer en-tête de série, n° de page, titre de pied de page
        nonempty = [l for l in pl if l.strip()]
        if len(nonempty) >= 2 and nonempty[-1].strip().isdigit():
            footer_title = nonempty[-2].strip()
        out = []
        for l in pl:
            s = l.strip()
            if s == series or s.isdigit() or (footer_title and s == footer_title):
                continue
            out.append(s)
        if p_i == 0:
            k = next((j for j, l in enumerate(out) if l.startswith("____")), None)
            if k is None:  # pas de ligne de séparation : sauter l'en-tête
                k = next(j for j, l in enumerate(out) if l == head[-1])
            out = out[k + 1:]
        body_lines.extend(out)

    # titre : le vrai titre du PDF (pied de page) si le nom de fichier est générique
    title = ftitle.strip()
    if norm(title) in ("predication",):
        title = title_upper.title() if norm(title_upper) != "predication" else "Prédication"
    # paragraphes : numéro explicite OU fin de ligne courte + ponctuation finale
    widths = sorted(len(l) for l in body_lines if len(l) > 20)
    p90 = widths[int(len(widths) * .9)] if widths else 80
    P, buf, num = [], [], None
    expected = 2
    def flush():
        nonlocal buf, num
        t = re.sub(r"\s+", " ", " ".join(buf)).strip()
        t = re.sub(r"(\w)- (\w)", r"\1-\2", t)  # mots coupés en fin de ligne (Saint- Esprit)
        if t: P.append({"i": len(P) + 1, "n": num, "t": t})
        buf, num = [], None
    for l in body_lines:
        if not l:
            continue
        mnum = re.match(r"^(\d{1,3})\s*[.)]?\s+(.*)$", l)
        if mnum and int(mnum.group(1)) in range(expected, expected + 3):
            flush(); num = int(mnum.group(1)); expected = num + 1
            buf.append(mnum.group(2)); continue
        if re.match(r"^(\[|Cantique|Le pasteur chante|Chant\b)", l):
            flush(); P.append({"i": len(P) + 1, "n": None, "t": l, "k": "note"}); continue
        buf.append(l)
        if len(l) < p90 * .82 and re.search(r"[.!?»…)\"]\s*$", l):
            n_keep = num; flush()
    flush()
    # découper les blocs trop longs (transcriptions sans retour à la ligne) en ~120 mots
    Q = []
    for p in P:
        if len(p["t"].split()) <= 220 or p.get("k"):
            Q.append(p); continue
        sents = re.split(r"(?<=[.!?»])\s+", p["t"])
        cur = []
        for se in sents:
            cur.append(se)
            if len(" ".join(cur).split()) >= 120:
                Q.append({"n": None, "t": " ".join(cur)}); cur = []
        if cur: Q.append({"n": None, "t": " ".join(cur)})
    P = []
    for k, p in enumerate(Q, 1):
        d = {"i": k, "t": p["t"]}
        if p.get("k"): d["k"] = p["k"]
        P.append(d)
    full = " ".join(p["t"] for p in P)
    refs = []
    for p in P:
        r = find_refs(p["t"])
        if r: p["refs"] = sorted(set(r))
        refs += r
    sc = theme_scores(full)
    words = len(full.split())
    jour, moment = when.split(",")[0].split()
    return {
        "id": sid, "date": f"{year}-{mm}-{dd}", "moment": "Matin" if ms == "M" else "Soir",
        "jour": jour.capitalize(), "dateLabel": when, "title": title, "titleUpper": title_upper,
        "preacher": preacher, "place": place, "venue": venue, "city": city, "country": country, "series": series,
        "words": words, "minutes": round(words / 200),
        "refs": sorted(set(refs), key=lambda r: refs.index(r)),
        "themes": {k: v for k, v in sc.items() if v},
        "paragraphs": P,
    }

MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
def slug(x):
    return re.sub(r"[^a-z0-9]+", "-", norm(x)).strip("-")

files = sorted(f for f in SRC.rglob("*") if f.suffix.lower() in (".pdf", ".docx") and not f.name.startswith("~$"))
groups = {}
for f in files:
    s_ = parse(f)
    rel = f.parent.relative_to(SRC)
    # 1 sous-dossier = 1 convention ; à la racine : regroupement par série + ville + mois
    key = str(rel) if str(rel) != "." else f"{s_['series']}|{s_['city']}|{s_['date'][:7]}"
    groups.setdefault(key, {"folder": str(rel) if str(rel) != "." else "", "sermons": []})["sermons"].append(s_)

conventions, sermons, seen = [], [], set()
for key, g in groups.items():
    ss = sorted(g["sermons"], key=lambda x: (x["date"], x["moment"] != "Matin"))
    # titres identiques dans une convention -> numéroter les parties
    same = {}
    for x in ss: same.setdefault(norm(x["title"]), []).append(x)
    for grp in same.values():
        if len(grp) > 1:
            for k, x in enumerate(grp, 1):
                x["title"] += f" ({k}{'re' if k == 1 else 'e'} partie)"
    first, last = ss[0], ss[-1]
    y, m = first["date"][:4], int(first["date"][5:7])
    city = first["city"] or g["folder"] or "Convention"
    cid = slug(f"{y}-{m:02d}-{city}")
    d1, d2 = int(first["date"][8:]), int(last["date"][8:])
    same_month = first["date"][:7] == last["date"][:7]
    dates = (f"du {d1} au {d2} {MOIS[m-1]} {y}" if same_month and d1 != d2 else
             f"{d1} {MOIS[m-1]} {y}" if d1 == d2 and same_month else
             f"du {d1} {MOIS[m-1]} au {d2} {MOIS[int(last['date'][5:7])-1]} {last['date'][:4]}")
    conv = {"id": cid, "name": ("Convention d'" + city if norm(city[:1]) in "aeiouyh" else "Convention de " + city), "city": city,
            "country": first["country"], "venue": first["venue"], "series": first["series"],
            "start": first["date"], "end": last["date"], "dates": dates,
            "preachers": sorted({x["preacher"] for x in ss}), "count": len(ss)}
    conventions.append(conv)
    for x in ss:
        x["conv"] = cid
        base = x["id"]; n = 2
        while x["id"] in seen: x["id"] = f"{base}-{n}"; n += 1
        seen.add(x["id"]); sermons.append(x)
conventions.sort(key=lambda c: c["start"], reverse=True)
import datetime
lib = {
    "app": "Man Child Ministry",
    "version": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
    "conventions": conventions,
    "themes": [{"id": t, "label": l, "kws": k} for t, l, k in THEMES],
    "sermons": sermons,
}
OUT.write_text(json.dumps(lib, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
for s in sermons:
    top = sorted(s["themes"].items(), key=lambda x: -x[1])[:5]
    print(s["id"], "|", s["title"], "|", len(s["paragraphs"]), "§", s["words"], "mots |", len(s["refs"]), "réf |", top)
print("taille", OUT.stat().st_size // 1024, "Ko")
