"""Extraction des prédications (PDF / Word) -> library.json pour l'application Man Child Ministry.

Usage : python extract.py <dossier source> <fichier library.json>
Chaque sous-dossier du dossier source = une convention. Les fichiers à la racine sont
regroupés par ville et mois. Les en-têtes variés sont tolérés (voir GUIDE-TECHNIQUE.md).
"""
import json, re, sys, unicodedata, warnings
warnings.filterwarnings("ignore")
import pymupdf  # pip install pymupdf
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
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

# ---------- Lecture des fichiers ----------
def pdf_pages(pdf):
    """Liste de pages, chaque page = liste de lignes (pied de page « Titre   12 » séparé)."""
    pages = []
    for page in pymupdf.open(pdf):
        lines = [l.strip() for l in page.get_text(sort=True).splitlines()]
        for k in range(len(lines) - 1, -1, -1):
            if lines[k]:
                m = re.match(r"^(.*\S)\s{2,}(\d{1,3})$", lines[k]) or re.match(r"^(\d{1,3})\s{2,}(.*\S)$", lines[k])
                if m: lines[k:k+1] = [m.group(1), m.group(2)]
                break
        pages.append([re.sub(r"\s+", " ", l) for l in lines])
    return pages

def docx_pages(path):
    import docx  # pip install python-docx
    return [[p.text.strip() for p in docx.Document(path).paragraphs]]

# ---------- Outils de date et de lieu ----------
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
MOIS_N = {norm(m): i + 1 for i, m in enumerate(MOIS)}
JOURS_FR = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
DATE_RE = re.compile(r"\b(\d{1,2})(?:er)?\s+(" + "|".join(MOIS_N) + r")\s+(\d{4})\b")
PAYS = {"cote d'ivoire": "Côte d'Ivoire", "cote divoire": "Côte d'Ivoire", "madagascar": "Madagascar", "togo": "Togo",
        "benin": "Bénin", "burkina faso": "Burkina Faso", "burkina": "Burkina Faso", "mali": "Mali", "senegal": "Sénégal",
        "ghana": "Ghana", "cameroun": "Cameroun", "gabon": "Gabon", "rdc": "RD Congo", "congo": "Congo", "guinee": "Guinée",
        "niger": "Niger", "nigeria": "Nigeria", "liberia": "Liberia", "sierra leone": "Sierra Leone", "france": "France",
        "belgique": "Belgique", "suisse": "Suisse", "canada": "Canada", "etats-unis": "États-Unis", "usa": "États-Unis",
        "kenya": "Kenya", "ouganda": "Ouganda", "zambie": "Zambie", "afrique du sud": "Afrique du Sud", "tchad": "Tchad",
        "centrafrique": "Centrafrique", "haiti": "Haïti", "maurice": "Maurice", "reunion": "La Réunion"}

def n2(s):  # normalisation pour comparaison (accents, apostrophes)
    return norm(s).replace("’", "'").replace("`", "'")

def find_date(text):
    m = DATE_RE.search(n2(text))
    if not m: return None
    return f"{int(m.group(3)):04d}-{MOIS_N[m.group(2)]:02d}-{int(m.group(1)):02d}"

def find_moment(text):
    t = n2(text)
    if re.search(r"\bmatin\b", t): return "M"
    if re.search(r"\b(soir|soiree)\b", t): return "S"
    return None

def parse_place(text):
    """'ACL Dynastie Éternelle _ Abidjan-Côte d’Ivoire', 'Tananarive, Madagascar - Jeudi 14 Août 2025 _ Matin',
       'Le 24 Décembre 2021 / Dabou - Côte D’Ivoire', 'Abidjan – Côte d’Ivoire, 28 Mai 2023 Matin' -> (lieu, ville, pays)"""
    t = text.replace("’", "'")
    t = re.sub(r"(?i)\b(le\s+)?\d{1,2}(er)?\s+[a-zéû]+\s+\d{4}\b", " ", t)          # date
    t = re.sub(r"(?i)\b(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)\b", " ", t)
    t = re.sub(r"(?i)\b(matin|soir|soirée)\b", " ", t)
    nt = n2(t)
    country = ""; cpos = -1
    for k in sorted(PAYS, key=len, reverse=True):
        i = nt.find(k)
        if i >= 0: country, cpos = PAYS[k], i; break
    before = t[:cpos] if cpos >= 0 else t
    parts = [x.strip(" ,.;:-–") for x in re.split(r"\s+[-–_/]\s+|\s*[,/_]\s*|-(?=[A-ZÉ])|–", before) if x.strip(" ,.;:-–_/")]
    city = parts[-1] if parts else ""
    venue = ", ".join(parts[:-1])
    return venue.strip(), city.strip(), country

def is_upper_line(l):
    letters = [c for c in l if c.isalpha()]
    return len(letters) >= 4 and sum(c.isupper() for c in letters) / len(letters) > .85

def clean_title(stem):
    t = re.sub(r"^\d{4}\s*[-_ ]?\s*\d{3,5}(?:[MS](?=[\s_-]))?\s*[-–_]?\s*", "", stem)          # date en tête
    t = re.split(r"\s*_\s*(?:pst|pasteur|part|$)", t, flags=re.I)[0] if "_" in t else t
    t = re.sub(r"(?i)\b(docx?|pdf|conv)\b", " ", t)
    t = re.sub(r"(?i)\(?\s*\b(prt|part|partie)\s*\d+\b\s*\)?", " ", t)
    t = re.sub(r"\s+", " ", t).strip(" ._-–")
    return t[:1].upper() + t[1:] if t else "Prédication"

# Lignes d'en-tête à ignorer (bandeaux, numéros de brochure…). Elles ne sont jamais reprises dans le texte.
IGNORE_RE = re.compile(r"(?i)^(l.ordre de melchis[ée]d(ech|ek|eck)\b|broch\b|sujet\s*:|inspiration\s*:)")

# ---------- Analyse d'un document ----------
def parse(path):
    pages = docx_pages(path) if path.suffix.lower() == ".docx" else pdf_pages(path)
    is_docx = path.suffix.lower() == ".docx"
    first = [l for l in pages[0] if l]
    head = first[:16]

    # lignes répétées en haut/bas de page (en-têtes et pieds de page) -> à retirer
    repeated = set()
    if len(pages) > 3:
        from collections import Counter
        cnt = Counter()
        for pg in pages:
            ne = [l for l in pg if l]
            for l in set(ne[:4] + ne[-4:]): cnt[l] += 1
        repeated = {l for l, c in cnt.items() if c >= max(3, .3 * len(pages))}

    # --- en-tête : date, moment, prédicateur, lieu
    i_date = next((k for k, l in enumerate(head) if find_date(l)), None)
    i_pst = next((k for k, l in enumerate(head) if re.match(r"(?i)^(pasteur|pst\.?|fr[eè]re|rev|ap[oô]tre|proph[eè]te)\b", l)), None)
    stem = path.stem
    fm = re.match(r"^(\d{4})\s*[-_ ]?\s*(\d{2})(\d{2,3})\s*([MS])?\b", stem)
    date = find_date(head[i_date]) if i_date is not None else None
    if not date and fm:
        date = f"{fm.group(1)}-{fm.group(2)}-{fm.group(3)[-2:]}"
    moment = None
    if i_date is not None:
        moment = find_moment(head[i_date]) or (find_moment(head[i_date + 1]) if i_date + 1 < len(head) and not head[i_date + 1].startswith("___") else None)
    if not moment and fm and fm.group(4): moment = fm.group(4)
    preacher = head[i_pst] if i_pst is not None else ""
    preacher = re.sub(r"(?i)^pst\.?\s*", "Pasteur ", preacher)
    preacher = " ".join(w.capitalize() if w.isupper() and len(w) > 2 else w for w in preacher.split())
    if not preacher:
        m = re.search(r"_\s*(?:Part\s*\d+)?\s*(P(?:st|asteur)\.?\s+[^_]+?)\.*$", stem, re.I)
        preacher = re.sub(r"(?i)^pst\.?\s*", "Pasteur ", m.group(1)).strip() if m else "Pasteur John Conteh"

    # lieu : la ligne de date et/ou la suivante
    place_src = ""
    if i_date is not None:
        cand = [head[i_date]]
        if i_date + 1 < len(head) and not head[i_date + 1].startswith("___") and not is_upper_line(head[i_date + 1]):
            cand.append(head[i_date + 1])
        for c in cand:
            v, c_, p_ = parse_place(c)
            if c_ or p_:
                place_src = c; venue, city, country = v, c_, p_; break
    if not place_src:
        venue, city, country = "", "", ""

    # titre en majuscules ; les lignes placées avant (bandeaux) sont ignorées.
    # Le thème de la série ne vient PAS du document : il est saisi dans conventions.xlsx.
    i_title = next((k for k, l in enumerate(head) if is_upper_line(l) and not IGNORE_RE.match(l)), None)
    series = ""
    banner = set(head[:i_title]) if i_title is not None else set()
    title_upper = ""
    if i_title is not None:
        k = i_title; tl = []
        while k < len(head) and is_upper_line(head[k]): tl.append(head[k]); k += 1
        title_upper = " ".join(tl)

    # --- corps du texte : après la ligne de soulignés, sinon après la dernière ligne d'en-tête
    body_start_line = None
    for k, l in enumerate(first[:20]):
        if l.startswith("____"): body_start_line = k; break
    if body_start_line is None:
        last = max([x for x in [i_date, i_pst, i_title] if x is not None] or [-1])
        # en-tête répété (fichiers Word) : sauter jusqu'à la dernière ligne identique à la ligne de date
        if i_date is not None:
            dl = head[i_date]
            last = max(last, max(k for k, l in enumerate(first[:20]) if l == dl))
            if last + 1 < len(first) and place_src and first[last + 1] == place_src: last += 1
        body_start_line = last
    footer_titles = set()
    body = []
    skipped = 0
    for p_i, pg in enumerate(pages):
        ne = [l for l in pg if l]
        if any(l.replace(" ", "").startswith("Cemessagedu") for l in ne[:6]):
            break  # page finale (colophon)
        if len(ne) >= 2 and ne[-1].isdigit(): footer_titles.add(ne[-2])
        for l in pg:
            if p_i == 0 and l:
                if skipped <= body_start_line:
                    skipped += 1; continue
            if l in repeated or (l.isdigit() and len(l) <= 3) or l in footer_titles or l in banner or IGNORE_RE.match(l):
                continue
            body.append(l)

    # --- paragraphes
    widths = sorted(len(l) for l in body if len(l) > 20)
    p90 = widths[int(len(widths) * .9)] if widths else 80
    P, buf = [], []
    def flush():
        nonlocal buf
        t = re.sub(r"\s+", " ", " ".join(buf)).strip()
        t = re.sub(r"(\w)- (\w)", r"\1-\2", t)
        t = re.sub(r"^\d{1,3}\s*[.)]?\s+(?=[A-ZÀ-ÖØ-Þ«\"'(\[])", "", t)   # numéro de paragraphe d'origine
        if t: P.append({"t": t})
        buf = []
    for l in body:
        if not l:
            if is_docx: flush()
            continue
        if re.match(r"^\d{1,3}\s*[.)]?\s+\S", l) and buf:
            flush()
        if re.match(r"^(\[|\(Cantique|Cantique|Chant\b|Le pasteur chante)", l) and len(l.split()) < 40:
            flush(); P.append({"t": l, "k": "note"}); continue
        buf.append(l)
        if is_docx or (len(l) < p90 * .82 and re.search(r"[.!?»…)\"]\s*$", l)):
            flush()
    flush()
    # découper les blocs trop longs en ~120 mots
    Q = []
    for p in P:
        if len(p["t"].split()) <= 220 or p.get("k"): Q.append(p); continue
        cur = []
        pieces = []
        for se in re.split(r"(?<=[.!?»])\s+", p["t"]):
            if len(se.split()) <= 160: pieces.append(se); continue
            # transcription sans ponctuation : couper aux virgules, sinon tous les 100 mots
            for sub in re.split(r"(?<=,)\s+", se):
                ws = sub.split()
                pieces += [" ".join(ws[j:j + 100]) for j in range(0, len(ws), 100)]
        for se in pieces:
            cur.append(se)
            if len(" ".join(cur).split()) >= 120: Q.append({"t": " ".join(cur)}); cur = []
        if cur: Q.append({"t": " ".join(cur)})
    paras = []
    for k, p in enumerate(Q, 1):
        d = {"i": k, "t": p["t"]}
        if p.get("k"): d["k"] = p["k"]
        r = find_refs(p["t"])
        if r: d["refs"] = sorted(set(r))
        paras.append(d)

    full = " ".join(p["t"] for p in paras)
    refs = [r for p in paras for r in p.get("refs", [])]
    words = len(full.split())
    title = clean_title(stem)
    if norm(title) in ("predication", "") and title_upper:
        title = title_upper.capitalize()
    part = re.search(r"(?i)\b(?:prt|part|partie)\s*(\d+)", stem + " " + title_upper)
    if part and "partie" not in norm(title): title += f" (partie {part.group(1)})"
    import datetime
    y, mo, dd = map(int, date.split("-")) if date else (1900, 1, 1)
    try: jour = JOURS_FR[datetime.date(y, mo, dd).weekday()]
    except ValueError: jour = ""
    mlabel = {"M": "Matin", "S": "Soir"}.get(moment, "")
    date_label = f"{jour} {mlabel.lower()}, {dd} {MOIS[mo-1]} {y}".replace("  ", " ").replace(" ,", ",")
    return {
        "id": f"{date}{moment or ''}", "date": date, "moment": mlabel, "jour": jour, "dateLabel": date_label,
        "title": title, "preacher": preacher, "venue": venue, "city": city, "country": country,
        "place": ", ".join(x for x in [venue, city, country] if x), "series": series,
        "words": words, "minutes": max(1, round(words / 200)),
        "refs": sorted(set(refs), key=lambda r: refs.index(r)),
        "themes": {k: v for k, v in theme_scores(full).items() if v},
        "paragraphs": paras, "file": str(path.relative_to(SRC)),
    }

# ---------- Regroupement par convention ----------
def slug(x):
    return re.sub(r"[^a-z0-9]+", "-", norm(x)).strip("-")

# ---------- Thèmes de série saisis à la main : conventions.xlsx ----------
CONV_XLSX = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(__file__).resolve().parent.parent / "conventions.xlsx"
COL_DOSSIER, COL_THEME = "Dossier", "Thème de la série"

def read_themes(path):
    if not path.exists(): return {}
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True)["Conventions"]
    rows = list(ws.iter_rows(values_only=True))
    h = [str(x or "").strip() for x in rows[0]]
    i_d, i_t = h.index(COL_DOSSIER), h.index(COL_THEME)
    return {str(r[i_d]).strip(): str(r[i_t] or "").strip() for r in rows[1:] if r[i_d]}

def sync_xlsx(path, convs):
    """Ajoute les nouveaux dossiers et met à jour les colonnes d'information (ville, pays, dates, nombre)."""
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    if not path.exists(): return "absent"
    wb = openpyxl.load_workbook(path)
    ws = wb["Conventions"]
    h = [str(c.value or "").strip() for c in ws[1]]
    col = {name: h.index(name) + 1 for name in h if name}
    rows = {str(ws.cell(r, col[COL_DOSSIER]).value).strip(): r for r in range(2, ws.max_row + 1) if ws.cell(r, col[COL_DOSSIER]).value}
    changed = False
    thin = Side(style="thin", color="D9D2C3")
    for c in convs:
        r = rows.get(c["folder"])
        if r is None:
            r = ws.max_row + 1; rows[c["folder"]] = r
            ws.cell(r, col[COL_DOSSIER], c["folder"]); changed = True
            for k in col.values():
                cell = ws.cell(r, k); cell.font = Font(name="Arial", size=10); cell.border = Border(bottom=thin)
                cell.alignment = Alignment(vertical="top", wrap_text=True)
            ws.cell(r, col[COL_THEME]).fill = PatternFill("solid", fgColor="FFF4CC")
        for name, val in (("Ville", c["city"]), ("Pays", c["country"]), ("Dates", c["dates"]), ("Prédications", c["count"])):
            if name in col and ws.cell(r, col[name]).value != val:
                ws.cell(r, col[name], val); changed = True
    if changed:
        try: wb.save(path)
        except PermissionError: return "ouvert"
    return "ok"

THEMES_SERIE = read_themes(CONV_XLSX)

files = sorted(f for f in SRC.rglob("*") if f.suffix.lower() in (".pdf", ".docx") and not f.name.startswith("~$"))
groups, problems = {}, []
for f in files:
    try:
        s_ = parse(f)
    except Exception as e:
        problems.append(f"{f.relative_to(SRC)} : {e}"); continue
    if not s_["paragraphs"]:
        problems.append(f"{f.relative_to(SRC)} : aucun texte extrait (PDF scanné ?)"); continue
    rel = f.parent.relative_to(SRC)
    folder = "" if str(rel) == "." else str(rel)
    key = folder or f"{s_['city']}|{s_['date'][:7]}"
    groups.setdefault(key, {"folder": folder, "sermons": []})["sermons"].append(s_)

from collections import Counter
order = {"Matin": 0, "Soir": 1, "": 2}
conventions, sermons, seen, warnings_ = [], [], set(), []
for key, g in groups.items():
    ss = sorted(g["sermons"], key=lambda x: (x["date"], order[x["moment"]]))
    same = {}
    for x in ss: same.setdefault(norm(x["title"]), []).append(x)
    for grp in same.values():
        if len(grp) > 1 and not any("partie" in norm(x["title"]) for x in grp):
            for k, x in enumerate(grp, 1): x["title"] += f" (partie {k})"
    first, last = ss[0], ss[-1]
    # ville : celle du dossier « AAAA-MM Ville » si présente, sinon la plus fréquente des en-têtes
    fm = re.match(r"^\d{4}[-_ ]\d{2}\s+(.+)$", g["folder"])
    head_city = Counter(x["city"] for x in ss if x["city"]).most_common(1)
    head_city = head_city[0][0] if head_city else ""
    city = fm.group(1).strip() if fm else (head_city or g["folder"] or "Convention")
    if fm and head_city and n2(head_city) != n2(city):
        warnings_.append(f"{g['folder']} : le dossier indique « {city} » mais les en-têtes indiquent « {head_city} »")
    country = Counter(x["country"] for x in ss if x["country"]).most_common(1)
    country = country[0][0] if country else ""
    venue = Counter(x["venue"] for x in ss if x["venue"]).most_common(1)
    venue = venue[0][0] if venue else ""
    series = THEMES_SERIE.get(g["folder"] or key, "")
    for x in ss:
        x["series"] = series
        x["city"] = city
        if not x["country"]: x["country"] = country
        x["place"] = ", ".join(v for v in [x["venue"], city, x["country"]] if v)
    y, m = first["date"][:4], int(first["date"][5:7])
    cid = slug(f"{y}-{m:02d}-{city}")
    while any(c["id"] == cid for c in conventions): cid += "-b"
    d1, d2 = int(first["date"][8:]), int(last["date"][8:])
    m2 = int(last["date"][5:7])
    if first["date"] == last["date"]: dates = f"{d1} {MOIS[m-1]} {y}"
    elif m == m2: dates = f"du {d1} au {d2} {MOIS[m-1]} {y}"
    else: dates = f"du {d1} {MOIS[m-1]} au {d2} {MOIS[m2-1]} {last['date'][:4]}"
    name = ("Convention d'" if norm(city[:1]) in "aeiouyh" else "Convention de ") + city
    conventions.append({"folder": g["folder"] or key, "id": cid, "name": name, "city": city, "country": country, "venue": venue,
                        "series": series, "start": first["date"], "end": last["date"], "dates": dates,
                        "preachers": sorted({x["preacher"] for x in ss}), "count": len(ss)})
    for x in ss:
        x["conv"] = cid
        base = x["id"]; n = 2
        while x["id"] in seen: x["id"] = f"{base}-{n}"; n += 1
        seen.add(x["id"]); sermons.append(x)
conventions.sort(key=lambda c: c["start"], reverse=True)
xl_state = sync_xlsx(CONV_XLSX, conventions)

import datetime
lib = {
    "app": "Man Child Ministry",
    "version": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
    "conventions": conventions,
    "themes": [{"id": t, "label": l, "kws": k} for t, l, k in THEMES],
    "sermons": sermons,
}
OUT.write_text(json.dumps(lib, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

for c in conventions:
    print(f"\n■ {c['name']} ({c['country'] or 'pays ?'}) — {c['dates']} — {c['count']} prédication(s)")
    if c["series"]: print(f"  Thème : {c['series']}")
    for x in [s for s in sermons if s["conv"] == c["id"]]:
        print(f"  {x['date']} {x['moment'] or '—':5} | {x['title'][:70]} | {len(x['paragraphs'])} §, {len(x['refs'])} réf.")
sans_theme = [c["folder"] for c in conventions if not c["series"]]
if sans_theme: print(f"\nℹ Thème de série non renseigné pour : {', '.join(sans_theme)} (fichier {CONV_XLSX.name})")
if xl_state == "ouvert": print(f"\n⚠ {CONV_XLSX.name} est ouvert dans Excel : les nouveaux dossiers n'ont pas pu y être ajoutés. Fermez-le et relancez.")
if xl_state == "absent": print(f"\n⚠ Fichier {CONV_XLSX} introuvable : aucun thème de série appliqué.")
for w in warnings_: print("\n⚠", w)
for p_ in problems: print("\n✖ Ignoré :", p_)
print(f"\nTotal : {len(conventions)} conventions, {len(sermons)} prédications — {OUT.stat().st_size // 1024} Ko")
