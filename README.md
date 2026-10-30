# 🥘 Nutri-Tech v2.0

**Meniuri tradiționale europene, cu bucătăria românească pe primul loc, și recomandări pentru o alimentație echilibrată.**

[![Deschide în Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raressandu-alt/nutritech/blob/main/colab/NutriTech.ipynb)

**Aplicația online:** https://nutri-tech-five.vercel.app

Nutri-Tech este o aplicație scrisă în Python. Îți calculează necesarul zilnic, îți propune în fiecare zi un meniu din preparate tradiționale și te lasă să notezi ce ai mâncat. Te ghidează Kip, o focă simpatică, iar aplicația arată ca o aplicație de telefon, cu o bară de navigare jos.

Codul folosește doar biblioteca standard Python, deci nu trebuie instalat nimic. E comentat în întregime, în română.

> Informațiile sunt generale, pentru adulți sănătoși. Nu înlocuiesc sfatul unui medic sau al unui nutriționist.
> Valorile nutriționale sunt estimări pe o porție obișnuită.

---

## Cum o rulezi

| Unde | Cum |
|---|---|
| **Pe web** | Deschide https://nutri-tech-five.vercel.app |
| **În Google Colab** | Apasă butonul „Open in Colab” de mai sus, apoi `Runtime → Run all`. Aplicația apare sub ultima celulă, împreună cu un link care o deschide într-un tab nou. |
| **Pe calculator** | `python colab/nutritech.py`. Se deschide singură la http://localhost:8000. Oprești serverul cu Ctrl+C. Ai nevoie de Python 3.9 sau mai nou. |

---

## Ce face aplicația

### 👤 Profil
- Completezi sexul, vârsta, greutatea, înălțimea, nivelul de activitate și obiectivul: slăbire lentă, menținere sau creștere în greutate.
- Alegi dieta (oricare, vegetariană sau de post) și bucătăria (toată Europa sau o anumită țară).
- Din aceste date, aplicația calculează câte calorii, proteine, carbohidrați, grăsimi, fibre și câtă apă îți trebuie pe zi.

### 🍽️ Azi
- Primești meniul zilei în 5 mese: mic dejun, ciorbă, felul doi, gustare și cină. Prânzul are două feluri, ca în tradiția românească.
- La fiecare fel apeși **„Am mâncat”**. Dacă te-ai înșelat, apeși din nou și bifa dispare.
- Inelul de calorii și barele pentru proteine, carbohidrați, grăsimi și fibre arată **ce ai mâncat** față de cât îți trebuie.
- Cardul **„Ce ai mâncat azi”** este istoricul zilei: fiecare fel bifat, cu caloriile lui, și totalul.
- Kip îți spune pe înțeles cât de echilibrat e meniul („foarte echilibrat”, „destul de echilibrat”, „puțin dezechilibrat”) și îți dă un sfat.
- Cu **„🎲 Alt meniu”** primești altă propunere. Butonul apare doar pe pagina Azi și doar până bifezi primul fel, ca să nu se schimbe meniul pe jumătate mâncat.
- Când bifezi toate felurile, ziua intră în seria ta.

### 📅 Săptămâna
- Vezi zilele săptămânii curente, de luni până duminică, fiecare cu data și meniul ei.
- Fiecare zi îți spune ce ai făcut:
  - **✅ Ai mâncat tot meniul**, cu totalul de calorii (cardul devine verde);
  - **Ai mâncat 3 din 5 feluri**;
  - **Nimic notat în ziua asta**.
- Pentru zilele care urmează vezi meniul propus și cât e de echilibrat.
- **Seria 🔥** numără câte zile la rând ai mâncat tot meniul. Apare și în colțul de sus, pe toate paginile. Cât timp nu ai terminat încă meniul de azi, seria se numără până ieri, ca să nu se rupă dimineața.

### 🔎 Explorează
- 38 de preparate din 9 țări, dintre care 23 românești: sarmale, ciorbă de perișoare, ciorbă de burtă, mămăligă cu brânză, zacuscă, fasole bătută, tochitură, papanași, cozonac și altele. Din restul Europei: gulaș, pierogi, musaka, paella, ratatouille, minestrone și altele.
- Le poți filtra după țară și după momentul zilei, sau le poți căuta după nume. Preparatele românești apar primele.
- Fiecare preparat are o descriere, etichete (vegetarian, de post) și valorile nutriționale pe porție.

### 💡 Sfaturi
- Îți explică cum a fost calculat necesarul tău zilnic.
- Îți dă sfaturi pentru meniul de azi, de exemplu când are prea multe grăsimi, prea puține fibre sau prea puține proteine, cu înlocuiri românești mai ușoare.
- Primești și reguli generale: cât să bei apă, cum arată o farfurie echilibrată, cât să limitezi sarea.

### Unde se păstrează ce ai mâncat
Istoricul stă într-un **cookie din browserul tău**, nu pe server. Fiecare vizitator are istoricul lui, fără cont și fără bază de date. Se păstrează ultimele 60 de zile. Dacă ștergi cookie-urile sau schimbi browserul, istoricul pornește de la zero.

---

## Cum funcționează

### Calculele
- **Metabolismul bazal**, cu formula Mifflin-St Jeor: `10 × kg + 6,25 × cm − 5 × vârstă + 5` la bărbați, respectiv `− 161` la femei.
- **Necesarul zilnic** = metabolismul bazal × nivelul de activitate (1,2 / 1,375 / 1,55 / 1,725). La slăbire scade cu 15%, la creștere urcă cu 10%.
- **Macronutrienți**, în intervalele EFSA: 50% carbohidrați, 30% grăsimi, 20% proteine, dar cel puțin 0,83 g proteine pe kilogram corp.
- **Fibre:** cel puțin 25 g pe zi (EFSA). **Apă:** în jur de 33 ml pe kilogram. **Sare:** cel mult 5 g pe zi (OMS).

### Meniul zilei
- Ziua are 5 momente, fiecare cu o parte din calorii: mic dejun 25%, ciorbă 12%, felul doi 23%, gustare 10%, cină 30%.
- Pentru fiecare moment, fiecare preparat primește un cost. Costul crește cu cât preparatul e mai departe de caloriile țintă și cu cât grăsimile trec de 35% din caloriile lui. Scade pentru fibre, iar preparatele românești primesc un bonus.
- Aplicația alege la întâmplare dintre primele 3 preparate. Așa meniurile variază, iar în medie 3-4 din cele 5 feluri sunt românești.
- Fiecare zi are meniul ei, stabil: dacă deschizi aplicația de mai multe ori în aceeași zi, vezi același meniu.

### Scorul de echilibru
Aplicația pornește de la 100 și scade puncte pentru:
- fiecare procent cu care meniul se abate de la caloriile țintă;
- fiecare procent din energie cu care proteinele, carbohidrații și grăsimile se abat de la împărțirea 20/50/30;
- fiecare gram de fibre care lipsește.

Scorul nu e afișat ca număr. Aplicația îl spune în cuvinte.

### Tehnic
- **Un singur fișier**, `colab/nutritech.py` (aproximativ 560 de linii, comentate), împărțit în 7 secțiuni: date, calcule, HTML, jurnal, ecrane, aplicație, pornire.
- **Server web din biblioteca standard** (`http.server`). Python construiește fiecare pagină ca HTML, fără JavaScript și fără framework-uri.
- **Profilul și filtrele stau în link-ul paginii** (`?tab=azi&kg=70...`), deci o pagină se poate salva sau trimite.
- **Butoanele „Am mâncat” și „Alt meniu”** trimit o cerere POST și apoi te întorc pe aceeași pagină. Astfel, un refresh nu repetă acțiunea.
- **Ziua se schimbă la miezul nopții după ora României**, chiar dacă serverul rulează pe altă oră.
- **Aceeași cod rulează în trei locuri:** în Colab (afișat în notebook), pe calculator (http://localhost:8000) și pe Vercel (ca funcție Python, prin `colab/api/index.py`).
- **Designul** reia mascota și culorile aplicației Kip din acest repo. Ecranele urmează aplicații de nutriție studiate pe Mobbin: Yazio, Lifesum, MacroFactor, Crouton.

---

## Fișiere

| Fișier | Rol |
|---|---|
| `colab/nutritech.py` | Toată aplicația: date, calcule, jurnal, ecrane, server |
| `colab/NutriTech.ipynb` | Notebook-ul pentru Colab, generat din `nutritech.py`. Nu îl edita de mână. |
| `colab/build_notebook.py` | Refă notebook-ul: `python colab/build_notebook.py` |
| `colab/test_nutritech.py` | Testele: `cd colab`, apoi `python test_nutritech.py` |
| `colab/api/index.py`, `colab/vercel.json` | Publicarea pe Vercel: `cd colab`, apoi `vercel deploy --prod` |
| `docs/nutritech-v2-plan.md` | Planul aplicației și referințele de design |

**Testele** verifică:
- formula și țintele zilnice;
- datele fiecărui preparat;
- meniul (fără repetări, același meniu pentru aceeași zi, respectarea dietei);
- scorul și sfaturile;
- jurnalul: bifare, debifare, ziua completă, seria, „Alt meniu” blocat după primul fel;
- cookie-ul: se citește corect, încape în 4 KB, iar un cookie stricat nu strică aplicația;
- link-urile greșite sau rău intenționate;
- un server adevărat, cu un browser simulat.

---

## Restul repo-ului

Nutri-Tech pornește de la **Kip**, o aplicație de economisire pentru studenți (React + Supabase), care se află tot aici, în `app/` și `supabase/`. De la Kip a preluat mascota, culorile și ideea de serie zilnică. Descrierea aplicației Kip: [docs/kip.md](docs/kip.md).
