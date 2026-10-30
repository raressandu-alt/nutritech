# Punctul de intrare pe Vercel. Runtime-ul Python de pe Vercel caută în acest fișier o clasă numită
# `handler` (un BaseHTTPRequestHandler), așa că refolosim exact serverul aplicației, fără cod nou.
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))   # nutritech.py e un nivel mai sus
from nutritech import Handler  # noqa: E402


class handler(Handler):   # Vercel recunoaște funcția doar după o clasă `handler` definită aici
    pass
