# %% [markdown]
# # 🥘 Nutri-Tech v2.0
# Meniuri tradiționale europene (întâi cele românești) și recomandări generale pentru o alimentație echilibrată.
#
# **Cum rulezi:** `Runtime → Run all` (sau Ctrl+F9). Aplicația apare la finalul notebook-ului,
# plus un link care o deschide într-un tab nou. Pe calculator: `python nutritech.py` → http://localhost:8000
#
# > Informațiile sunt generale, pentru adulți sănătoși. Nu înlocuiesc sfatul unui medic sau nutriționist.
# > Valorile nutriționale sunt estimări pe o porție obișnuită.

# %%
# ── 1. DATE ─────────────────────────────────────────────────────────────────────────────────────
# Doar biblioteca standard aici, ca logica să poată fi testată și fără Colab.
import random
from collections import namedtuple

# Un fel de mâncare = un tuplu cu nume (namedtuple): ocupă puțină memorie și se citește ușor (d.kcal).
# meal = în ce moment al zilei poate fi servit:
#   D = mic dejun, S = ciorbă/supă (la prânz), P = fel principal la prânz, C = cină, G = gustare
# tags: veg = vegetarian, post = de post (fără produse animale), gras = prăjit sau mezel (apare în sfaturi)
Dish = namedtuple("Dish", "name country meal kcal protein carbs fat fiber tags desc")

DISHES = [Dish(*row) for row in [
    # ── România: bucătăria pe care o punem pe primul loc ──
    ("Sarmale cu mămăligă", "RO", "PC", 620, 28, 45, 36, 6, "", "Foi de varză murată umplute cu carne și orez, fierte încet."),
    ("Ciorbă de perișoare", "RO", "S", 320, 18, 28, 14, 4, "", "Perișoare de carne cu orez, în zeamă acrită cu borș și leuștean."),
    ("Ciorbă de legume", "RO", "S", 180, 5, 28, 5, 7, "veg post", "Legume de sezon acrite cu borș, cu pătrunjel verde."),
    ("Ciorbă de burtă", "RO", "S", 380, 22, 12, 26, 1, "gras", "Ciorbă cu smântână și gălbenuș, servită cu ardei iute și mujdei."),
    ("Ciorbă de pui à la grec", "RO", "S", 290, 22, 20, 12, 2, "", "Supă de pui cu orez, dreasă cu ou și lămâie."),
    ("Mămăligă cu brânză și smântână", "RO", "DC", 520, 20, 50, 26, 3, "veg", "Mămăligă caldă cu telemea și o lingură de smântână."),
    ("Mici cu muștar", "RO", "PC", 560, 30, 6, 46, 0, "gras", "Trei mici la grătar, cu muștar și pâine."),
    ("Tochitură moldovenească", "RO", "PC", 780, 38, 48, 48, 3, "gras", "Carne de porc cu cârnați, mămăligă, brânză și ou ochi."),
    ("Zacuscă pe pâine integrală", "RO", "DG", 260, 6, 34, 11, 7, "veg post", "Zacuscă de vinete și ardei copți, pe două felii de pâine integrală."),
    ("Salată de vinete cu roșii", "RO", "DG", 220, 4, 18, 15, 6, "veg post", "Vinete coapte pe plită, cu ceapă, ulei și roșii."),
    ("Fasole bătută cu ceapă călită", "RO", "PC", 360, 15, 44, 13, 14, "veg post", "Piure de fasole cu usturoi și ceapă rumenită."),
    ("Iahnie de fasole", "RO", "PC", 340, 16, 48, 9, 15, "veg post", "Fasole albă cu ceapă, morcov, roșii și cimbru."),
    ("Ardei umpluți cu sos de roșii", "RO", "PC", 450, 22, 38, 22, 5, "", "Ardei grași umpluți cu carne și orez, copți în sos de roșii."),
    ("Tocăniță de legume cu mămăligă", "RO", "PC", 380, 9, 58, 12, 10, "veg post", "Cartofi, ardei, ciuperci și roșii înăbușite, cu mămăligă."),
    ("Ciulama de ciuperci cu mămăligă", "RO", "PC", 410, 10, 50, 18, 5, "veg", "Ciuperci într-un sos alb cu mărar, alături de mămăligă."),
    ("Pește la grătar cu mujdei", "RO", "PC", 420, 38, 10, 24, 4, "", "Crap sau păstrăv la grătar, cu mujdei și salată de varză."),
    ("Musaca de cartofi", "RO", "PC", 560, 26, 40, 32, 4, "", "Straturi de cartofi și carne tocată, gratinate cu ou și lapte."),
    ("Ouă ochiuri cu telemea și roșii", "RO", "D", 350, 20, 8, 26, 2, "veg", "Două ouă, telemea de vacă și roșii românești."),
    ("Plăcintă cu brânză", "RO", "DG", 380, 13, 40, 18, 1, "veg", "Foi subțiri cu brânză dulce de vaci și mărar."),
    ("Iaurt de casă cu mere și nuci", "RO", "DG", 240, 9, 26, 11, 3, "veg", "Iaurt gras, măr ras, nuci și un strop de miere."),
    ("Fructe de sezon", "RO", "G", 120, 1, 30, 0, 5, "veg post", "Mere, pere sau prune românești."),
    ("Papanași cu smântână și dulceață", "RO", "G", 620, 16, 78, 26, 2, "veg", "Gogoși de brânză cu smântână și dulceață de afine."),
    ("Cozonac cu nucă", "RO", "G", 330, 7, 46, 13, 2, "veg", "O felie de cozonac de casă cu umplutură de nucă."),
    # ── restul Europei ──
    ("Gulaș", "HU", "PC", 450, 32, 30, 20, 5, "", "Tocană ungurească de vită cu boia, cartofi și ardei."),
    ("Lecsó", "HU", "PC", 260, 8, 20, 16, 5, "veg", "Ardei, roșii și ceapă înăbușite, cu un ou bătut."),
    ("Pierogi ruskie", "PL", "PC", 480, 14, 66, 17, 4, "veg", "Colțunași polonezi cu cartofi și brânză, cu ceapă rumenită."),
    ("Musaka grecească", "GR", "PC", 560, 26, 30, 36, 6, "", "Vinete, carne tocată și sos bechamel, la cuptor."),
    ("Salată grecească", "GR", "PC", 320, 9, 12, 26, 4, "veg", "Roșii, castraveți, măsline, ceapă roșie și feta."),
    ("Iaurt grecesc cu miere", "GR", "DG", 220, 15, 22, 8, 1, "veg", "Iaurt strecurat, miere de cimbru și nuci."),
    ("Minestrone", "IT", "S", 230, 8, 34, 6, 8, "veg post", "Supă italiană de legume cu fasole și paste mici."),
    ("Risotto cu ciuperci", "IT", "PC", 520, 12, 72, 18, 3, "veg", "Orez arborio gătit încet, cu ciuperci și parmezan."),
    ("Paella cu fructe de mare", "ES", "PC", 560, 32, 66, 16, 4, "", "Orez cu șofran, creveți, midii și ardei."),
    ("Gazpacho", "ES", "SG", 150, 3, 16, 9, 4, "veg post", "Supă rece de roșii, castraveți și ardei."),
    ("Ratatouille", "FR", "PC", 220, 4, 22, 13, 7, "veg post", "Dovlecei, vinete, ardei și roșii cu ierburi provensale."),
    ("Omletă cu ierburi", "FR", "D", 300, 20, 2, 23, 0, "veg", "Omletă franțuzească moale, cu arpagic și pătrunjel."),
    ("Banița", "BG", "D", 420, 14, 38, 24, 1, "veg", "Plăcintă bulgărească cu sirene, coaptă în foi."),
    ("Salată șopska", "BG", "PC", 260, 9, 12, 20, 4, "veg", "Roșii, castraveți, ardei copți și brânză sirene rasă."),
    ("Müsli Bircher", "CH", "D", 330, 11, 48, 10, 7, "veg", "Ovăz înmuiat peste noapte cu iaurt, măr și nuci."),
]]

FLAGS = {"RO": "🇷🇴 România", "HU": "🇭🇺 Ungaria", "PL": "🇵🇱 Polonia", "GR": "🇬🇷 Grecia", "IT": "🇮🇹 Italia",
         "ES": "🇪🇸 Spania", "FR": "🇫🇷 Franța", "BG": "🇧🇬 Bulgaria", "CH": "🇨🇭 Elveția"}

# Ziua e împărțită în momente: (eticheta afișată, codul din câmpul meal, partea din caloriile zilei).
# Prânzul are două feluri, ca în tradiția românească: întâi ciorbă, apoi felul doi.
SLOTS = [("Mic dejun", "D", .25), ("Prânz · ciorbă", "S", .12), ("Prânz · felul doi", "P", .23),
         ("Gustare", "G", .10), ("Cină", "C", .30)]

# %%
# ── 2. CALCUL ───────────────────────────────────────────────────────────────────────────────────
def targets(sex, age, kg, cm, activity, goal):
    """Ținta zilnică pentru un adult sănătos.

    BMR (metabolismul bazal) cu formula Mifflin-St Jeor, înmulțit cu nivelul de activitate (TDEE),
    apoi ajustat după obiectiv (de ex. -0.15 = slăbire lentă). Macronutrienții urmează intervalele EFSA:
    50% carbohidrați, 30% grăsimi, 20% proteine, dar nu mai puțin de 0.83 g proteine pe kg corp.
    """
    bmr = 10 * kg + 6.25 * cm - 5 * age + (5 if sex == "M" else -161)
    kcal = round(bmr * activity * (1 + goal) / 10) * 10          # rotunjim la 10 kcal: cifrele exacte ar minți
    return {"bmr": round(bmr), "tdee": round(bmr * activity), "kcal": kcal,
            "protein": round(max(kcal * .20 / 4, .83 * kg)),        # 1 g proteine = 4 kcal
            "carbs": round(kcal * .50 / 4),                         # 1 g carbohidrați = 4 kcal
            "fat": round(kcal * .30 / 9),                           # 1 g grăsimi = 9 kcal
            "fiber": 25, "water": round(kg * .033, 1)}              # EFSA: 25 g fibre; ~33 ml apă pe kg


def allowed(d, diet, cuisine):
    """True dacă felul respectă dieta aleasă și bucătăria aleasă ("" = toată Europa)."""
    return (diet == "" or diet in d.tags) and (cuisine == "" or d.country == cuisine)


def day_menu(t, diet="", cuisine="", seed=0):
    """Meniul unei zile: câte un fel pentru fiecare moment din SLOTS.

    Pentru fiecare moment dăm fiecărui fel un cost: cât de departe e de caloriile țintă, plus o
    penalizare dacă grăsimile trec de 35% din caloriile lui, minus un bonus pentru fibre. Alegem la
    întâmplare dintre primele 3, ca meniurile să varieze. Felurile românești primesc un bonus fix de
    0.15 (adunat, nu înmulțit, pentru că un cost poate fi negativ), deci în medie 3-4 din 5 feluri
    sunt românești. Același seed dă mereu același meniu.
    Cost: O(feluri × momente), adică microsecunde.
    """
    def cost(d, goal):
        balance = abs(d.kcal - goal) / goal + max(0, d.fat * 9 / d.kcal - .35) - d.fiber / 100
        return balance - (.15 if d.country == "RO" else 0)

    rng, menu = random.Random(seed), []
    for label, code, share in SLOTS:
        pool = [d for d in DISHES if code in d.meal and d not in (m for _, m in menu)]
        # dacă bucătăria aleasă nu are nimic pentru acest moment, păstrăm dieta și renunțăm la bucătărie
        pool = [d for d in pool if allowed(d, diet, cuisine)] or [d for d in pool if allowed(d, diet, "")]
        if pool:
            goal = t["kcal"] * share
            pool.sort(key=lambda d: cost(d, goal))
            menu.append((label, rng.choice(pool[:3])))
    return menu


def totals(menu):
    """Suma calorii, macronutrienți și fibre pentru toate felurile din meniu."""
    keys = ("kcal", "protein", "carbs", "fat", "fiber")
    return {k: sum(getattr(d, k) for _, d in menu) for k in keys}


def score(tot, t):
    """Scor de echilibru 0-100: pornim de la 100 și scădem pentru fiecare abatere.

    1 punct pentru fiecare 1% abatere de la caloriile țintă, 1 punct pentru fiecare procent din
    energie care se abate de la împărțirea 20/50/30, 1 punct pentru fiecare gram de fibre lipsă.
    """
    kcal = max(tot["kcal"], 1)
    split = {"protein": (4, .20), "carbs": (4, .50), "fat": (9, .30)}   # (kcal pe gram, procent țintă)
    penalty = abs(tot["kcal"] / t["kcal"] - 1) * 100
    penalty += sum(abs(tot[k] * per_g / kcal - share) * 100 for k, (per_g, share) in split.items())
    penalty += max(0, t["fiber"] - tot["fiber"])
    return max(0, round(100 - penalty))


def tips(menu, t):
    """Sfaturi scurte, bazate pe reguli simple: fiecare regulă verifică o problemă și propune o variantă românească."""
    tot = totals(menu)
    fat_pct = tot["fat"] * 9 / max(tot["kcal"], 1) * 100
    out = []
    if fat_pct > 35:
        out.append(f"Grăsimile dau {fat_pct:.0f}% din calorii (ținta e sub 35%). Pune iaurt în loc de smântână și gătește la cuptor, nu prăjit.")
    if tot["fiber"] < t["fiber"]:
        out.append(f"Fibre: {tot['fiber']} g din {t['fiber']} g. O salată de varză, o fasole bătută sau pâinea integrală le completează.")
    if tot["protein"] < t["protein"] * .9:
        out.append(f"Proteine: {tot['protein']} g din {t['protein']} g. Adaugă brânză de vaci, ouă, pește sau fasole.")
    if tot["kcal"] > t["kcal"] * 1.1:
        out.append(f"Meniul trece cu {tot['kcal'] - t['kcal']} kcal peste țintă. Împarte porția de desert sau păstreaz-o pentru weekend.")
    elif tot["kcal"] < t["kcal"] * .9:
        out.append(f"Meniul are cu {t['kcal'] - tot['kcal']} kcal sub țintă. O gustare în plus ajută: un măr și o mână de nuci.")
    out += [f"{d.name}: gustos, dar gras sau procesat. Merge de 1-2 ori pe lună, cu o salată alături."
            for _, d in menu if "gras" in d.tags]
    # sfaturi generale, valabile pentru oricine
    out += [f"Apă: în jur de {t['water']} L pe zi. Ceaiurile neîndulcite se pun la socoteală.",
            "Farfuria echilibrată: jumătate legume, un sfert proteine, un sfert cereale integrale sau cartofi.",
            "Sare: maximum 5 g pe zi (OMS). Murăturile, telemeaua și mezelurile au deja multă sare."]
    return out

# %%
# ── 3. HTML ─────────────────────────────────────────────────────────────────────────────────────
# Aplicația e o pagină web randată pe server: Python construiește HTML-ul, browserul doar îl afișează.
# Fără JavaScript și fără framework-uri: fiecare apăsare e un link sau un formular, iar starea stă în
# URL (?tab=azi&kg=70...). Culorile vin din tokenii aplicației Kip (app/src/styles/tokens.css), iar
# ecranele urmează referințe Mobbin: inelul de calorii din Yazio, cardurile de mese din Lifesum,
# planul pe zile din Crouton, sfaturile cu mascotă din Yazio, bara de jos din aplicația Kip.
from html import escape
from urllib.parse import parse_qs, urlencode, urlsplit

KIP = "https://raw.githubusercontent.com/raressandu-alt/nutritech/main/app/public/mascot/"
CSS = """<style>@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;700;900&display=swap');
*{box-sizing:border-box}body{margin:0;font-family:Archivo,system-ui,sans-serif;color:#0F2540;background:#0F2540}
.phone{max-width:430px;height:100vh;margin:0 auto;background:#EAF4FF;display:flex;flex-direction:column}
@media(min-width:600px){.phone{height:min(860px,calc(100vh - 40px));margin:20px auto;border-radius:44px;border:12px solid #000;overflow:hidden}}
header{display:flex;justify-content:space-between;align-items:center;padding:14px 16px;font-size:18px}
main{flex:1;overflow-y:auto;padding:0 16px 16px}h2{font-weight:900;margin:4px 0 10px}
nav{display:flex;background:#fff;border-top:1px solid #D6E4F7}
nav a{flex:1;text-align:center;padding:8px 0 10px;font-size:11px;color:#5E6A79;text-decoration:none}
nav a b{display:block;font-size:22px}nav a.on{color:#1747C4;font-weight:700}
.dice{font-size:13px;font-weight:700;color:#0F2540;background:#FFB020;padding:6px 12px;border-radius:99px;text-decoration:none;box-shadow:0 2px 0 #B86E00}
.card{background:#fff;border-radius:16px;padding:12px 14px;margin:8px 0;border:1px solid #D6E4F7}
.row{display:flex;gap:12px;align-items:center;flex-wrap:wrap}.grow{flex:1;min-width:150px}
.chip{display:inline-block;padding:2px 9px;border-radius:99px;background:#DFE9FF;color:#1747C4;font-size:12px;margin:2px 4px 0 0}
.chip.ro{background:#FFF4D6;color:#7A4B00}.muted{color:#5E6A79;font-size:13px}
.lbl{font-size:11px;font-weight:700;color:#5E6A79;text-transform:uppercase;letter-spacing:.05em}
.ring{width:130px;height:130px;border-radius:50%;display:grid;place-items:center}
.ring>div{width:100px;height:100px;border-radius:50%;background:#fff;display:grid;place-items:center;text-align:center}
.big{font-size:26px;font-weight:900}.bar{height:8px;border-radius:9px;background:#E0EBFC;overflow:hidden;margin:3px 0 8px}
.bar>i{display:block;height:100%}.kip{display:flex;gap:12px;align-items:center;margin:4px 0 8px}.kip img{width:72px}
.bubble{background:#fff;border-radius:16px;padding:10px 14px;border:1px solid #D6E4F7}
label{display:block;margin:12px 0 4px;font-weight:700;font-size:13px}
input,select{width:100%;padding:11px;border-radius:12px;border:1px solid #B9CDE9;font:inherit;background:#fff;color:inherit}
.seg{display:flex;gap:6px}.seg label{flex:1;margin:0}.seg input{display:none}
.seg span{display:block;text-align:center;padding:10px 4px;border-radius:12px;background:#fff;border:1px solid #B9CDE9;font-weight:700;font-size:14px}
.seg input:checked+span{background:#1F5FD6;color:#fff;border-color:#1F5FD6}
button.dice{border:0;font-family:inherit;cursor:pointer}.streak{font-weight:900;font-size:15px}
.eat{margin-top:8px;width:100%;padding:10px;border-radius:12px;border:1px solid #1F5FD6;background:#fff;color:#1F5FD6;font:inherit;font-weight:700;cursor:pointer}
.eat.on{background:#0B7A57;border-color:#0B7A57;color:#fff}.card.today{border:2px solid #1F5FD6}.card.done{border:2px solid #0B7A57}
.btn{display:block;width:100%;margin-top:16px;padding:14px;border:0;border-radius:14px;background:#FFB020;color:#0F2540;font:inherit;font-weight:900;font-size:16px;box-shadow:0 3px 0 #B86E00;cursor:pointer}
</style>"""
COLORS = {"protein": "#1F5FD6", "carbs": "#FFB020", "fat": "#B86E00", "fiber": "#0B7A57"}
NAMES = {"protein": "Proteine", "carbs": "Carbohidrați", "fat": "Grăsimi", "fiber": "Fibre"}


def kip(mood, text):
    """Kip, foca din aplicația-mamă, devine ghidul de nutriție: o imagine și un balon de text."""
    return f'<div class="kip"><img src="{KIP}{mood}.webp" alt="Kip"><div class="bubble">{text}</div></div>'


def ring(value, target):
    """Inel de progres pentru calorii, desenat doar cu CSS (conic-gradient), fără biblioteci de grafice."""
    pct = min(value / target, 1) * 360
    return (f'<div class="ring" style="background:conic-gradient(#0B7A57 {pct}deg,#E0EBFC 0)"><div>'
            f'<span class="big">{value}</span><span class="muted">din {target} kcal<br>mâncate</span></div></div>')


def bar(key, value, target):
    """O bară orizontală pentru un macronutrient: valoarea meniului față de țintă."""
    width = min(value / target * 100, 100)
    return (f'<div class="row muted" style="flex-wrap:nowrap"><b style="flex:1">{NAMES[key]}</b>{value} / {target} g</div>'
            f'<div class="bar"><i style="width:{width}%;background:{COLORS[key]}"></i></div>')


def card(d, label="", extra=""):
    """Fișa unui fel: steagul țării, descrierea, etichetele și valorile nutriționale pe porție.
    `extra` e HTML pus la final, de exemplu butonul „Am mâncat” de pe ecranul „Azi”."""
    chips = f'<span class="chip {"ro" if d.country == "RO" else ""}">{FLAGS[d.country]}</span>'
    chips += "".join(f'<span class="chip">{tag}</span>' for tag in d.tags.split() if tag != "gras")
    return (f'<div class="card">{f"<div class=lbl>{label}</div>" if label else ""}'
            f'<div class="row"><b class="grow">{d.name}</b><b>{d.kcal} kcal</b></div>'
            f'<div class="muted">{d.desc}</div><div>{chips}</div>'
            f'<div class="muted">P {d.protein} g · C {d.carbs} g · G {d.fat} g · fibre {d.fiber} g</div>{extra}</div>')


# Câmpurile de formular. Valorile permise stau într-un singur loc și servesc de două ori:
# pentru a desena formularul și pentru a valida ce vine din URL.
OPTIONS = {
    "sex": [("Femeie", "F"), ("Bărbat", "M")],
    "act": [("Sedentar", "1.2"), ("Ușor activ (1-3 zile/săpt.)", "1.375"), ("Activ (3-5 zile/săpt.)", "1.55"), ("Foarte activ", "1.725")],
    "goal": [("Slăbire lentă", "-0.15"), ("Menținere", "0"), ("Creștere în greutate", "0.1")],
    "diet": [("Oricare", ""), ("Vegetarian", "veg"), ("De post", "post")],
    "cuisine": [("🇪🇺 Toată Europa", "")] + [(v, k) for k, v in FLAGS.items()],
    "meal": [("Orice moment", ""), ("Mic dejun", "D"), ("Ciorbe și supe", "S"), ("Prânz", "P"), ("Cină", "C"), ("Gustări", "G")],
}
OPTIONS["ex"] = OPTIONS["cuisine"]                                   # filtrul de țară din „Explorează”
RANGES = {"age": (18, 80, 30), "kg": (40, 150, 70), "cm": (140, 210, 170)}   # (minim, maxim, implicit)


def seg(name, p):
    """Butoane-pastilă (radio) pentru opțiuni puține, ca în onboarding-ul MacroFactor."""
    return '<div class="seg">' + "".join(f'<label><input type="radio" name="{name}" value="{v}"'
                                         f'{" checked" if v == p[name] else ""}><span>{l}</span></label>'
                                         for l, v in OPTIONS[name]) + "</div>"


def select(name, p):
    """Listă derulantă pentru opțiuni multe."""
    return f'<select name="{name}">' + "".join(f'<option value="{v}"{" selected" if v == p[name] else ""}>{l}</option>'
                                               for l, v in OPTIONS[name]) + "</select>"


def hidden(p, *skip):
    """Câmpuri ascunse: un formular trimite mai departe și restul stării, ca să nu se piardă profilul."""
    return "".join(f'<input type="hidden" name="{k}" value="{escape(str(v))}">' for k, v in p.items() if k not in skip)

# %%
# ── 4. JURNAL ───────────────────────────────────────────────────────────────────────────────────
# Ce ai mâncat se salvează într-un fișier JSON, o intrare pe zi:
#   {"2026-10-29": {"seed": 739918, "eaten": ["Sarmale cu mămăligă", ...], "done": true}}
# seed = ce meniu ți s-a propus în ziua aceea; done = ai bifat toate felurile, deci ziua intră în serie.
# În Colab fișierul rămâne cât timp rulează sesiunea; pe calculator rămâne pentru totdeauna.
import json
import pathlib
import threading
from datetime import date, timedelta

JOURNAL = pathlib.Path("nutritech_jurnal.json")
LOCK = threading.Lock()                      # serverul răspunde în paralel: scrierile trec pe rând
BY_NAME = {d.name: d for d in DISHES}        # căutare rapidă a unui fel după nume


def load():
    """Citește jurnalul; dacă fișierul lipsește sau e stricat, pornim cu unul gol."""
    try:
        return json.loads(JOURNAL.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def day_entry(journal, day):
    """Intrarea unei zile. O zi fără intrare primește meniul ei implicit (seed = numărul zilei)."""
    return journal.get(day.isoformat(), {"seed": day.toordinal(), "eaten": [], "done": False})


def streak(journal, today):
    """Seria de foc, ca în aplicația Kip: câte zile la rând ai mâncat tot meniul.
    Dacă azi nu e gata încă, seria pornește de ieri, ca să nu se rupă dimineața."""
    day = today if day_entry(journal, today)["done"] else today - timedelta(1)
    n = 0
    while day_entry(journal, day)["done"]:
        n, day = n + 1, day - timedelta(1)
    return n


def act(p, action, dish, today):
    """Schimbă ziua de azi în jurnal: bifează/debifează un fel („toggle”) sau propune alt meniu („reroll”)."""
    with LOCK:
        journal = load()
        entry = day_entry(journal, today)
        if action == "reroll" and not entry["eaten"]:   # meniul se schimbă doar până bifezi primul fel
            entry["seed"] += 1
        elif action == "toggle" and dish in BY_NAME:
            entry["eaten"].remove(dish) if dish in entry["eaten"] else entry["eaten"].append(dish)
        menu = day_menu(targets_of(p), p["diet"], p["cuisine"], entry["seed"])
        entry["done"] = all(d.name in entry["eaten"] for _, d in menu)
        journal[today.isoformat()] = entry
        JOURNAL.write_text(json.dumps(journal, ensure_ascii=False, indent=1), encoding="utf-8")

# %%
# ── 5. ECRANE ───────────────────────────────────────────────────────────────────────────────────
DAYS = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
MONTHS = "ian feb mar apr mai iun iul aug sep oct nov dec".split()


def mood(s):
    """Starea lui Kip după scor: aceeași idee ca în aplicația Kip, încurajare fără vină."""
    return "celebrate-face" if s >= 85 else "happy-face" if s >= 70 else "think-face"


def balance(s):
    """Scorul spus în cuvinte: nimeni nu trebuie să ghicească ce înseamnă „80 din 100”."""
    return "foarte echilibrat" if s >= 80 else "destul de echilibrat" if s >= 60 else "puțin dezechilibrat"


def days(n):
    """„1 zi”, „2 zile”: forma corectă în română."""
    return f"{n} {'zi' if n == 1 else 'zile'}"


def post_button(p, label, cls, **fields):
    """Un buton care trimite o acțiune (POST) și se întoarce pe aceeași pagină, cu același profil."""
    inputs = "".join(f'<input type="hidden" name="{k}" value="{escape(v)}">' for k, v in fields.items())
    return f'<form method="post" action="?{escape(urlencode(p))}">{inputs}<button class="{cls}">{label}</button></form>'


def screen_profile(p):
    """Ecranul „Profil”: puține întrebări, apoi meniul (ca onboarding-ul MacroFactor și Cal AI)."""
    fields = [("Sex", seg("sex", p)), ("Vârstă (ani)", ""), ("Greutate (kg)", ""), ("Înălțime (cm)", ""),
              ("Activitate", select("act", p)), ("Obiectiv", select("goal", p)),
              ("Dietă", seg("diet", p)), ("Bucătărie", select("cuisine", p))]
    for i, key in enumerate(RANGES, start=1):   # cele trei câmpuri numerice, cu limitele din RANGES
        lo, hi, _ = RANGES[key]
        fields[i] = (fields[i][0], f'<input type="number" name="{key}" min="{lo}" max="{hi}" value="{p[key]}">')
    form = "".join(f"<label>{label}</label>{widget}" for label, widget in fields)
    return (kip("wave-face", "Salut! Sunt Kip. Spune-mi câte ceva despre tine și îți fac meniul zilei.")
            + f'<form class="card">{hidden(p, "tab", *OPTIONS, *RANGES)}<input type="hidden" name="tab" value="azi">'
            + form + '<button class="btn">Fă-mi meniul</button></form>')


def screen_today(menu, t, entry, p, series):
    """Ecranul „Azi”: meniul propus, cu „Am mâncat” pe fiecare fel, și ce ai mâncat până acum.

    Inelul și barele arată ce ai mâncat (ca la Yazio), nu ce e în meniu: așa vezi cât mai ai până la țintă.
    """
    eaten = [BY_NAME[n] for n in entry["eaten"] if n in BY_NAME]
    got = totals([("", d) for d in eaten])
    s = score(totals(menu), t)
    if entry["done"]:
        bubble = kip("celebrate-face", f"<b>Ai mâncat tot meniul de azi!</b> Ziua intră în serie: 🔥 {days(series)} la rând.")
    else:
        hint = tips(menu, t)[0] if eaten else "Apasă „Am mâncat” după fiecare fel și îți țin eu socoteala."
        bubble = kip(mood(s), f"<b>Meniul de azi e {balance(s)}.</b> {hint}")
    bars = "".join(bar(k, got[k], t[k]) for k in COLORS)
    log = "".join(f'<div class="row muted" style="flex-wrap:nowrap"><span style="flex:1">✓ {d.name}</span>{d.kcal} kcal</div>'
                  for d in eaten) or '<div class="muted">Nimic încă.</div>'
    history = (f'<div class="card"><div class="lbl">Ce ai mâncat azi</div>{log}'
               f'<div class="row" style="flex-wrap:nowrap;margin-top:6px"><b style="flex:1">Total</b><b>{got["kcal"]} kcal</b></div></div>')
    cards = "".join(card(d, label, post_button(p, "✓ Mâncat" if d.name in entry["eaten"] else "Am mâncat",
                                               "eat on" if d.name in entry["eaten"] else "eat", action="toggle", dish=d.name))
                    for label, d in menu)
    return (bubble + f'<div class="card row">{ring(got["kcal"], t["kcal"])}<div class="grow">{bars}</div></div>'
            + history + cards)


def screen_week(t, p, journal, today, series):
    """Ecranul „Săptămâna”: zilele săptămânii curente, ce ai mâncat în fiecare și seria ta (ca streak-ul din Kip)."""
    html = ""
    for i, name in enumerate(DAYS):
        day = today + timedelta(i - today.weekday())   # luni + i
        entry = day_entry(journal, day)
        menu = day_menu(t, p["diet"], p["cuisine"], entry["seed"])
        kcal = sum(BY_NAME[n].kcal for n in entry["eaten"] if n in BY_NAME)
        if entry["done"]:
            status = f"✅ Ai mâncat tot meniul · {kcal} kcal"
        elif entry["eaten"]:
            status = f"Ai mâncat {len(entry['eaten'])} din {len(menu)} feluri · {kcal} kcal"
        elif day < today:
            status = "Nimic notat în ziua asta"
        elif day == today:
            status = "Bifează felurile pe pagina Azi"
        else:
            status = f"Meniu propus, {balance(score(totals(menu), t))}"
        rows = "".join(f'<div class="row muted" style="flex-wrap:nowrap;margin-top:4px"><span class="lbl" style="width:90px">{label}</span>'
                       f'<span style="flex:1">{"✓ " if d.name in entry["eaten"] else ""}{d.name}</span>{d.kcal}</div>' for label, d in menu)
        cls = "done" if entry["done"] else "today" if day == today else ""
        html += (f'<div class="card {cls}"><b>{name}, {day.day} {MONTHS[day.month - 1]}{" · azi" if day == today else ""}</b>'
                 f'<div class="muted">{status}</div>{rows}</div>')
    return (kip("pose-feed", f"🔥 <b>Seria ta: {days(series)} la rând.</b> O zi intră în serie când bifezi toate felurile din meniul ei.")
            + '<div class="muted">„Echilibrat” = meniul are aproape cât îți trebuie din calorii, proteine, carbohidrați, grăsimi și fibre.</div>'
            + html)


def screen_explore(p):
    """Ecranul „Explorează”: toate felurile, filtrate după țară, moment al zilei și text; cele românești primele."""
    found = [d for d in DISHES if (not p["ex"] or d.country == p["ex"]) and (not p["meal"] or p["meal"] in d.meal)
             and p["q"].lower() in (d.name + d.desc).lower()]
    found.sort(key=lambda d: (d.country != "RO", d.name))
    form = (f'<form class="card">{hidden(p, "ex", "meal", "q")}<label>Țara</label>{select("ex", p)}'
            f'<label>Moment</label>{select("meal", p)}<label>Caută</label>'
            f'<input name="q" value="{escape(p["q"])}" placeholder="sarmale, fasole..."><button class="btn">Caută</button></form>')
    return form + f"<h2>{len(found)} feluri</h2>" + "".join(map(card, found))


def screen_tips(menu, t):
    """Ecranul „Sfaturi”: ținta calculată, explicată pe înțeles, apoi sfaturile pentru meniul zilei."""
    how = (f"Metabolism bazal (Mifflin-St Jeor): <b>{t['bmr']} kcal</b>. Cu activitatea ta: <b>{t['tdee']} kcal</b>. "
           f"După obiectiv: <b>{t['kcal']} kcal</b>, din care {t['protein']} g proteine, {t['carbs']} g carbohidrați, {t['fat']} g grăsimi.")
    items = "".join(f"<li>{x}</li>" for x in tips(menu, t))
    return (kip("pose-guide", "Sfaturi pentru tine. Informații generale, nu sfat medical.")
            + f'<div class="card"><div class="lbl">Cum am calculat</div>{how}</div>'
            + f'<div class="card"><div class="lbl">Pentru meniul de azi</div><ul>{items}</ul></div>')

# %%
# ── 6. APLICAȚIA ────────────────────────────────────────────────────────────────────────────────
# Un server web din biblioteca standard. GET întoarce pagina calculată din URL și din jurnal; POST
# (butoanele „Am mâncat” și „Alt meniu”) schimbă jurnalul și trimite înapoi la aceeași pagină.
import builtins
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TABS = [("profil", "👤", "Profil"), ("azi", "🍽️", "Azi"), ("saptamana", "📅", "Săptămâna"),
        ("exploreaza", "🔎", "Explorează"), ("sfaturi", "💡", "Sfaturi")]
DEFAULT = {"act": "1.375", "goal": "0"}   # opțiunile implicite care nu sunt primele din listă


def params(query):
    """Citește profilul și filtrele din URL și le validează: orice valoare necunoscută revine la cea implicită."""
    q = {k: v[0] for k, v in parse_qs(query).items()}
    p = {k: q[k] if q.get(k) in {v for _, v in opts} else DEFAULT.get(k, opts[0][1]) for k, opts in OPTIONS.items()}
    p["tab"] = q.get("tab") if q.get("tab") in {key for key, _, _ in TABS} else "azi"
    for key, (lo, hi, default) in RANGES.items():
        try:
            p[key] = min(max(int(q[key]), lo), hi)   # cifre în afara limitelor sunt aduse la limită
        except (KeyError, ValueError):
            p[key] = default
    p["q"] = q.get("q", "")[:40]
    return p


def targets_of(p):
    """Ținta zilnică pentru profilul din URL."""
    return targets(p["sex"], p["age"], p["kg"], p["cm"], float(p["act"]), float(p["goal"]))


def render(query, today=None):
    """Pagina completă pentru un URL: antetul cu seria, ecranul cerut și bara de navigare de jos."""
    p, today, journal = params(query), today or date.today(), load()
    entry, series, t = day_entry(journal, today), streak(journal, today), targets_of(p)
    menu = day_menu(t, p["diet"], p["cuisine"], entry["seed"])
    screens = {"profil": lambda: screen_profile(p), "azi": lambda: screen_today(menu, t, entry, p, series),
               "saptamana": lambda: screen_week(t, p, journal, today, series),
               "exploreaza": lambda: screen_explore(p), "sfaturi": lambda: screen_tips(menu, t)}
    nav = "".join(f'<a href="?{urlencode({**p, "tab": key})}" class="{"on" if key == p["tab"] else ""}"><b>{icon}</b>{label}</a>'
                  for key, icon, label in TABS)
    # „Alt meniu” doar pe „Azi” și doar până bifezi primul fel, ca seria să nu se încurce
    dice = post_button(p, "🎲 Alt meniu", "dice", action="reroll") if p["tab"] == "azi" and not entry["eaten"] else ""
    return ('<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Nutri-Tech</title>{CSS}<div class="phone"><header><b>🥘 Nutri-Tech</b>'
            f'<div class="row" style="gap:10px">{dice}<span class="streak">🔥 {series}</span></div></header>'
            f'<main>{screens[p["tab"]]()}</main><nav>{nav}</nav></div></html>')


class Handler(BaseHTTPRequestHandler):
    """GET: pagina randată. POST: o acțiune în jurnal, apoi redirect (303) înapoi la aceeași pagină."""

    def do_GET(self):
        page = render(urlsplit(self.path).query).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self):
        form = parse_qs(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode())
        act(params(urlsplit(self.path).query), form.get("action", [""])[0], form.get("dish", [""])[0], date.today())
        self.send_response(303)   # după POST, browserul face GET: un refresh nu mai trimite acțiunea de două ori
        self.send_header("Location", self.path)
        self.end_headers()

    def log_message(self, *args):   # fără un rând în consolă pentru fiecare cerere
        pass


SERVER = None


def run(port=8000, block=False):
    """Pornește serverul. În Colab aplicația apare sub celulă; local se deschide în browser."""
    global SERVER
    if SERVER:   # celula rulată din nou: oprim serverul vechi ca să eliberăm portul
        SERVER.shutdown()
        SERVER.server_close()
    SERVER = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    if not block:   # în notebook: server într-un fir separat, ca celula să se termine
        threading.Thread(target=SERVER.serve_forever, daemon=True).start()
    try:
        from google.colab import output   # există doar în Colab
        output.serve_kernel_port_as_iframe(port, height=880)
        output.serve_kernel_port_as_window(port, anchor_text="↗ Deschide Nutri-Tech într-un tab nou")
    except ImportError:
        print(f"Nutri-Tech rulează la http://localhost:{port}")
    if block:   # în terminal: deschidem browserul și servim până la Ctrl+C
        webbrowser.open(f"http://localhost:{port}")
        SERVER.serve_forever()

# %%
# ── 7. PORNIRE ──────────────────────────────────────────────────────────────────────────────────
# Într-un notebook (Colab sau Jupyter) serverul merge în fundal; în terminal ține programul deschis.
if __name__ == "__main__":
    run(block=not getattr(builtins, "__IPYTHON__", False))
