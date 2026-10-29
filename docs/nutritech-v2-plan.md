# Nutri-Tech v2.0: plan

Python app, hosted on Google Colab and runnable online. It shows traditional European menus
(Romanian dishes first) and gives general advice for balanced eating.

## Requirements

| Requirement | How we meet it |
|---|---|
| Functional Python code | One module, `colab/nutritech.py`. It runs in Colab and on a laptop. |
| Commented | Every block has a comment that explains *why*, not only *what*. Romanian comments, because the app and its users are Romanian. |
| Hosted on Colab, runnable online | `colab/NutriTech.ipynb` opens straight from GitHub with an "Open in Colab" badge. The app is a small web server from the standard library; Colab shows it under the cell and in a new tab. No install. |
| Traditional European menus, Romanian first | About 32 dishes. 20 are Romanian (sarmale, ciorbă de perișoare, mămăligă, zacuscă, papanași...). 12 come from the rest of Europe (gulaș, pierogi, paella, musaka...). |
| General advice for balanced eating | Calorie and macro targets (Mifflin-St Jeor plus EFSA ranges), a balance score, and rule-based tips. Shown with a clear "not medical advice" note. |
| As little code as possible, without losing performance | Plain Python, no pandas, no web server. Data is a list of tuples. The menu generator is greedy, O(dishes x meals), so it runs in microseconds. |

## Foundation from this repo (Kip)

- **Kip the seal** becomes the nutrition guide. Its mascot images load from
  `app/public/mascot/*.webp` through raw GitHub URLs (the repo is public), so nothing is copied.
- **Design tokens** come from `app/src/styles/tokens.css`: navy text `#0F2540`, light blue page `#EAF4FF`,
  structure blue `#1F5FD6`, progress green `#0B7A57`, gold `#FFB020`, flame orange for the streak.
- **The mascot mood logic** comes from `app/src/components/mascot/lines.ts`: one line, one mood, never guilt.
  Kip is happy when the menu is balanced and thinks when it needs a fix.
- **The streak idea** returns as "zile echilibrate" in the weekly menu.

## UI, from Mobbin references

| Screen in Nutri-Tech | Mobbin reference | What we take |
|---|---|---|
| Profil (form plus result) | MacroFactor onboarding, Bevel "Your Nutrition Goal" | Few questions, then the TDEE explained in plain words ("cum am calculat") |
| Azi (menu of the day) | Yazio Today, Lifesum Diary | Calorie ring, three macro bars, meal cards with kcal |
| Săptămâna (weekly menu) | Crouton Meal Plan | Days stacked, meals grouped under small labels |
| Explorează (all dishes) | Woolworths / Grab cuisines | Country chips with flags, filters for meal and diet |
| Fișa felului | MyFitnessPal recipe, Lifesum nutrition table | Tag chips, macro split in %, nutrition table |
| Sfaturi | Yazio "Meal tips just for you", BitePal tips | Mascot on top, three to five short tips |

## Architecture: one file, four layers

```
colab/nutritech.py
  1. DATE     DISHES: (name, country, meal, kcal, protein, carbs, fat, fiber, tags, description)
  2. CALCUL   targets(profile) -> kcal, macros, water, fiber
              day_menu(targets, filters, seed) -> 4 dishes
              score(menu, targets) -> 0..100, plus tips
  3. HTML     card(), ring(), bar(): small functions that return HTML strings with inline CSS
  4. ECRANE   one function per screen (Profil, Azi, Săptămâna, Explorează, Sfaturi)
  5. APP      http.server: render(url) -> full page, state in the URL, phone layout with a bottom
              tab bar like Kip. Colab: shown with google.colab.output; laptop: http://localhost:8000
colab/NutriTech.ipynb   built from nutritech.py by colab/build_notebook.py (one source, no copy)
colab/test_nutritech.py plain asserts for the calculation layer, run without Colab
```

Cells in `nutritech.py` use `# %%` markers. `build_notebook.py` turns each marked block into a notebook
cell, so the code a teacher reads in Colab is the same code we test locally.

## Formulas (general, for healthy adults)

- BMR, Mifflin-St Jeor: `10*kg + 6.25*cm - 5*age + 5` (male) or `- 161` (female).
- TDEE = BMR x activity (1.2 / 1.375 / 1.55 / 1.725).
- Goal: lose -15%, keep 0%, gain +10%.
- Macros: carbs 50%, fat 30%, protein 20% of kcal (EFSA ranges: 45-60 / 20-35 / 10-20+).
- Water: 33 ml/kg. Fiber: at least 25 g (EFSA).
- Meals: breakfast 25%, lunch 35%, dinner 30%, snack 10%.

## Menu generator

For each meal, keep dishes that match the filters (vegetarian, de post, country). Sort them by
distance to the meal's kcal target and pick at random from the 3 closest (seeded by the day, so the
week is stable and every day is different). Romanian dishes get a small bonus, so they come first
when two dishes are equally close.

## Tips (rule-based, never a diagnosis)

Rules look at the menu against the targets: fat above 35%, fiber below 25 g, protein below target,
too many calories, a fried or cured-meat dish (mici, tochitură), no vegetables. Each rule gives one
short tip in Romanian, with a Romanian swap (for example: "mămăligă cu iaurt în loc de smântână").

## Out of scope

Accounts, saving data between sessions, food logging, photo recognition, exact recipes. Nutrition
values are estimates per portion and are labelled as such.

## Steps

1. Write `colab/nutritech.py` (data, calculation, HTML, UI).
2. Write `colab/test_nutritech.py` and run it locally.
3. Write `colab/build_notebook.py`, build `NutriTech.ipynb`, check that the notebook JSON is valid.
4. Add `colab/README.md` with the Colab badge, and a link from the root README.
5. Do not push until the user asks.
