# Teste pentru stratul de calcul. Rulează fără Colab: python colab/test_nutritech.py
import nutritech as nt

# Mifflin-St Jeor: femeie, 30 ani, 70 kg, 170 cm -> BMR = 700 + 1062.5 - 150 - 161 = 1451.5
t = nt.targets("F", 30, 70, 170, 1.375, 0)
assert t["bmr"] == round(1451.5) and t["kcal"] == 2000, t
assert t["protein"] >= .83 * 70 and t["water"] == 2.3

# fiecare fel are date complete, un cod de moment valid și o țară cunoscută
for d in nt.DISHES:
    assert d.kcal > 0 and set(d.meal) <= set("DSPCG") and d.country in nt.FLAGS, d
assert sum(d.country == "RO" for d in nt.DISHES) > len(nt.DISHES) / 2   # bucătăria românească e prioritară

# meniul: un fel pe moment, fără repetări, stabil pentru același seed
menu = nt.day_menu(t, seed=1)
assert len(menu) == len(nt.SLOTS) and len({d for _, d in menu}) == len(menu)
assert menu == nt.day_menu(t, seed=1)

# filtrele de dietă se respectă în fiecare moment al zilei
for diet in ("veg", "post"):
    assert all(diet in d.tags for _, d in nt.day_menu(t, diet, seed=3)), diet
# o bucătărie fără ciorbe (Ungaria) nu lasă golă ciorba de la prânz
assert len(nt.day_menu(t, "", "HU", seed=2)) == len(nt.SLOTS)

# scorul e între 0 și 100, iar un meniu perfect potrivit cu ținta primește 100
assert 0 <= nt.score(nt.totals(menu), t) <= 100
perfect = {"kcal": 2000, "protein": 100, "carbs": 250, "fat": 2000 * .3 / 9, "fiber": 25}
assert nt.score(perfect, t) == 100

# sfaturile semnalează felurile grase
fatty = [("Cină", next(d for d in nt.DISHES if d.name == "Tochitură moldovenească"))]
assert any("Tochitură" in tip for tip in nt.tips(fatty, t))

# jurnalul stă într-un cookie; în teste îl ținem într-un dicționar, ca browserul
from datetime import date, timedelta
p, today, journal = nt.params(""), date(2026, 10, 29), {}   # joi

# „Alt meniu” schimbă meniul până bifezi primul fel, apoi nu mai are efect
nt.act(journal, p, "reroll", "", today)
assert journal[today.isoformat()]["seed"] == today.toordinal() + 1
day_menu = nt.day_menu(nt.targets_of(p), seed=today.toordinal() + 1)
nt.act(journal, p, "toggle", day_menu[0][1].name, today)
nt.act(journal, p, "reroll", "", today)
assert journal[today.isoformat()]["seed"] == today.toordinal() + 1
assert "Alt meniu" not in nt.render("tab=azi", journal, today) and "Alt meniu" not in nt.render("tab=saptamana", {})

# un fel bifat apare în istoric și în calorii; ziua devine completă doar cu toate felurile bifate
page = nt.render("tab=azi", journal, today)
assert "✓ Mâncat" in page and f"{day_menu[0][1].kcal} kcal" in page and not journal[today.isoformat()]["done"]
for _, d in day_menu[1:]:
    nt.act(journal, p, "toggle", d.name, today)
assert journal[today.isoformat()]["done"] and nt.streak(journal, today) == 1
week = nt.render("tab=saptamana", journal, today)
assert "Ai mâncat tot meniul" in week and "scor" not in week

# seria: ieri complet + azi complet = 2; o zi lipsă o rupe; debifarea scoate ziua de azi din serie
journal[(today - timedelta(1)).isoformat()] = {"seed": 0, "eaten": [], "done": True}
journal[(today - timedelta(3)).isoformat()] = {"seed": 0, "eaten": [], "done": True}
assert nt.streak(journal, today) == 2
nt.act(journal, p, "toggle", day_menu[0][1].name, today)
assert nt.streak(journal, today) == 1                      # azi nu mai e completă, ieri încă ține seria
nt.act(journal, p, "toggle", "Fel inexistent", today)      # nume necunoscut: ignorat

# cookie: dus și întors fără pierderi; 60 de zile pline încap în 4 KB; cookie stricat = jurnal gol
cookie = nt.dump(journal, today)
assert nt.load(f"alt=1; jurnal={cookie}") == journal
full = {(today - timedelta(i)).isoformat(): {"seed": 739000 + i, "eaten": [d.name for _, d in day_menu], "done": True}
        for i in range(120)}
assert len(nt.dump(full, today)) < 3800 and len(nt.load("jurnal=" + nt.dump(full, today))) == 61
assert nt.load("jurnal=stricat") == {} and nt.load("") == {}

# fiecare ecran al aplicației se randează, cu bara de navigare
for tab, text in [("profil", "Fă-mi meniul"), ("azi", "Am mâncat"), ("saptamana", "Seria ta"),
                  ("exploreaza", "feluri"), ("sfaturi", "Mifflin")]:
    page = nt.render(f"tab={tab}", {})
    assert text in page and "Explorează</a>" in page, tab
assert "Sarmale" in nt.render("tab=exploreaza&ex=RO&q=sarmale", {})

# URL-uri greșite sau răuvoitoare nu strică aplicația și nu injectează HTML
p = nt.params("age=abc&kg=999&tab=nimic&diet=x")
assert p["age"] == 30 and p["kg"] == 150 and p["tab"] == "azi" and p["diet"] == ""
assert "<script>" not in nt.render("tab=exploreaza&q=<script>alert(1)</script>", {})

# serverul pornește, răspunde și păstrează jurnalul în cookie între cereri (ca un browser)
import urllib.request
nt.run(port=8765)
browser = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
assert "Nutri-Tech" in browser.open("http://127.0.0.1:8765/?tab=azi").read().decode()
dish = nt.day_menu(nt.targets_of(nt.params("")), seed=nt.ro_today().toordinal())[0][1].name
post = "http://127.0.0.1:8765/?" + nt.urlencode({"tab": "azi", "action": "toggle", "dish": dish})
assert "✓ Mâncat" in browser.open(post, data=b"").read().decode()                                  # POST, apoi 303
assert "✓ Mâncat" in browser.open("http://127.0.0.1:8765/?tab=azi").read().decode()              # cookie-ul a rămas
assert "✓ Mâncat" not in urllib.request.urlopen("http://127.0.0.1:8765/?tab=azi").read().decode()  # alt vizitator: jurnal gol
nt.SERVER.shutdown()

print("OK: toate testele au trecut")
