# Construiește NutriTech.ipynb din nutritech.py: o singură sursă de cod, deci notebook-ul nu rămâne în urmă.
# Fiecare bloc care începe cu "# %%" devine o celulă; "# %% [markdown]" devine celulă de text.
# Rulare: python colab/build_notebook.py
import json
import pathlib
import re

here = pathlib.Path(__file__).parent
src = (here / "nutritech.py").read_text(encoding="utf-8")
cells = []
for block in re.split(r"^# %%", src, flags=re.M)[1:]:
    header, _, body = block.partition("\n")
    if "[markdown]" in header:   # textul de markdown e scris ca linii de comentariu: scoatem "# "
        cells.append({"cell_type": "markdown", "metadata": {},
                      "source": [re.sub(r"^# ?", "", line) for line in body.strip().splitlines(True)]})
    else:
        cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                      "source": body.strip().splitlines(True)})

notebook = {"cells": cells, "nbformat": 4, "nbformat_minor": 5,
            "metadata": {"colab": {"name": "NutriTech.ipynb"}, "language_info": {"name": "python"},
                         "kernelspec": {"name": "python3", "display_name": "Python 3"}}}
(here / "NutriTech.ipynb").write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"NutriTech.ipynb: {len(cells)} celule")
