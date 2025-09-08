import sys
import os

# Clear terminal screen
if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")


if len(sys.argv) < 2:
    print("Usage: python cat.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

try:
    with open(filename, encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, start=1):
            print(f"{i:03}. {line.rstrip()}")
except FileNotFoundError:
    print(f"File not found: {filename}")

input("\nPress Enter to close...")