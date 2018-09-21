# 1. nacitat mapu
# 2. spustit skript se vstupem a precist vystup
# 3. zvalidovat vystup
# 4. provest vystup, vyhodnotit a upravit mapu
# 5. ulozit mezivysledek nekam, at' vime co se deje


def read_map(file_name):
    with open(file_name, "r") as f:
        return map(str.strip, f.read().split("\n"))

