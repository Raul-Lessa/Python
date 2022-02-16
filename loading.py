from itertools import count


import os
os.system('cls' if os.name == 'nt' else 'clear')

i = 0
while i <= 100:
    bar = "[" + "="*i + "]".rjust(101 - i)
    percentage = str(i) + "%"
    print(bar[:50 - len(percentage)] + percentage + bar[50:])
    i = i + 1
