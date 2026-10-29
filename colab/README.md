# Nutri-Tech v2.0

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raressandu-alt/nutritech/blob/main/colab/NutriTech.ipynb)

Aplicație Python care rulează online în Google Colab. Afișează meniuri tradiționale europene, cu bucătăria
românească pe primul loc, și dă recomandări generale pentru o alimentație echilibrată. Ghidul este Kip, foca
din aplicația Kip din acest repo.

**Cum rulezi:**
- **Online (Colab):** apasă butonul „Open in Colab”, apoi `Runtime → Run all`. Aplicația apare sub ultima celulă, plus un link care o deschide într-un tab nou. Nu trebuie instalat nimic.
- **Pe calculator:** `python colab/nutritech.py` → se deschide singur http://localhost:8000. Oprire: Ctrl+C.

Aplicația e o pagină web cu aspect de telefon și bară de navigare jos, ca aplicația Kip. Serverul e din
biblioteca standard Python (`http.server`), deci nu are dependențe.

## Ce face

| Ecran | Ce arată |
|---|---|
| 👤 Profil | Sex, vârstă, greutate, înălțime, activitate, obiectiv, dietă (oricare, vegetarian, de post), bucătărie |
| 🍽️ Azi | Meniul zilei în 5 momente (mic dejun, ciorbă, felul doi, gustare, cină). Buton „Am mâncat” pe fiecare fel; inelul și barele arată ce ai mâncat, plus istoricul zilei. „🎲 Alt meniu” merge doar până bifezi primul fel. |
| 📅 Săptămâna | Zilele săptămânii curente: ✅ pentru zilele în care ai mâncat tot meniul, ce ai bifat în rest, și seria 🔥 de zile complete |
| 🔎 Explorează | 38 de feluri din 9 țări (23 românești), cu filtre după țară, moment al zilei și text |
| 💡 Sfaturi | Cum a fost calculată ținta și sfaturi pentru meniul zilei |

## Fișiere

| Fișier | Rol |
|---|---|
| `nutritech.py` | Tot codul: date, calcule, HTML, interfață. Sursa unică. |
| `NutriTech.ipynb` | Notebook-ul pentru Colab, generat din `nutritech.py`. Nu îl edita de mână. |
| `build_notebook.py` | Refă notebook-ul: `python colab/build_notebook.py` |
| `test_nutritech.py` | Teste pentru calcule, jurnal și server, fără Colab: `cd colab && python test_nutritech.py` |
| `nutritech_jurnal.json` | Creat la rulare, în folderul din care pornești: ce ai mâncat în fiecare zi. Nu intră în git. |

## Metodă

- Metabolism bazal: Mifflin-St Jeor. Necesar zilnic: metabolism × activitate, ajustat după obiectiv.
- Macronutrienți: 50% carbohidrați, 30% grăsimi, 20% proteine (în intervalele EFSA), minimum 0,83 g proteine/kg.
- Fibre: minimum 25 g (EFSA). Apă: aproximativ 33 ml/kg. Sare: maximum 5 g (OMS).
- Scorul de echilibru (0-100) scade pentru abaterea de la calorii, de la împărțirea macronutrienților și pentru fibrele lipsă.

> Informații generale pentru adulți sănătoși. Nu înlocuiesc sfatul unui medic sau nutriționist.
> Valorile nutriționale sunt estimări pe o porție obișnuită.

Planul complet și referințele de design (Mobbin): [docs/nutritech-v2-plan.md](../docs/nutritech-v2-plan.md).
