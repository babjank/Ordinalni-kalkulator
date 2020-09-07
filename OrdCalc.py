from ordinalni_kalkulator import *
import re
import time

class Error(Exception):
    """Bazna klasa za greške."""
    pass

class CalculatorError(Error):
    """Greška nastala tijekom izvođenja naredbe."""
    def __init__(self, num, message):
        self.num = num
        self.message = message

def calculate(unos, memory):
    n = 0
    for naredba in unos.split(";"):
        naredba = naredba.strip()
        n += 1

        naredba = naredba.replace("ω","w").replace("×","*").replace("·","*").replace("÷","//").replace("^","**")

        if "<<" in naredba or ">>" in naredba:
            naredba = naredba + " + Ordinal(0)"

        try:
            try:
                ans = eval(naredba, globals(), memory)
                memory["_"] = ans

                ans = repr(ans).replace("w","ω").replace("**","^").replace("*","·")
                print(ans)
            except:
                exec(naredba, globals(), memory)
                if 'w' in memory:
                    del memory['w']
                    raise CalculatorError(n,"Ime varijable ne može biti w.")
                #print(memory)
        except CalculatorError as e:
            raise e
        except:
            raise CalculatorError(n,"Naredbu nije moguće izvršiti.")
            


def main():
    print("  ORDINALNI KALKULATOR by BB")
    print("><><><><><><><><><><><><><><><\n")
    print("Za sve informacije o korištenju ove aplikacije koristite naredbu help.")

    memory = dict()
    try:
        while True:
            try:
                unos = input("ordCalc> ")
                unos = unos.strip()

                if unos == "exit": break
                elif unos == "": continue
                elif unos == "help":
                    print('''
Dobrodošli u Ordinalni kalkulator.

Ovo je aplikacija napravljena za provođenje aritmetičkih operacija nad
ordinalnim brojevima. Mogući je standardni python unos gdje je w zamjena
za grčko slovo omega:

ordCalc> (w**w*2 + w**2 + 4) // w**2

Ili unos koristeći unicode znakove:

ordCalc> (ω^ω×2 + ω^2 + 4) ÷ ω^2

Ukoliko ne vidite unicode znakove promijenite font terminala u Lucida console
ili Consolas.

Za dohvat zadnjeg rezultata izračunatog kalkulatorom koristite varijablu `_`.
Operacije koje je moguće provoditi su:

Dodjeljivanje vrijednosti
-------------------------
ordCalc> x = w + 1
ordCalc> x
ω + 1
ordCalc> x += w * 2 + 4
ordCalc> x
ω·3 + 4

Moguće je navesti više naredbi u jednom retku, odvajamo ih separatorom ";".

ordCalc> y = w ** w + w ** 3 * 2 + w + 4; y += 5; y
ω^ω + ω^3·2 + ω + 9

Uspoređivanje
-------------
ordCalc> w < 1
False
ordCalc> w == 1 + w
True

Zbrajanje
---------
ordCalc> 2 + w
ω
ordCalc> (w ** 2 + w * 1 + 4) + (w * 2 + 3)
ω^2 + ω·3 + 3

Množenje
--------
ordCalc> 2 * w
ω
ordCalc> (w ** w * 3 + w) * 2
ω^ω·6 + ω

Potenciranje
------------
ordCalc> 2 ** w
ω
ordCalc> (w + 1) ** (w + 1)
ω^(ω + 1) + ω^ω

Oduzimanje
----------
ordCalc> w - 1
ω
ordCalc> (w**w*3 + w**3*5 + w + 4) - (w**w*3 + w**3*3 + 2)
ω^3·2 + ω + 4

Dijeljenje
----------
ordCalc> a = w**w + w**3*2 + w**2*5 + 4; b = w**2*4 + w*7 + 5; divmod(a,b)
(ω^ω + ω·2 + 1, ω^2 + 4)
ordCalc> a // b
ω^ω + ω·2 + 1
ordCalc> a % b
ω^2 + 4
ordCalc> x = w**2 + w; divmod(x,w)
(ω + 1, 0)
ordCalc> q = x // w; r = x % w; w*q + r == x
True

Maksimum
--------
ordCalc> max(w**4,w**3*2 + w**2 + 4)
ω^4
ordCalc> max((w**1)**w, w**(1**w))
ω^ω

Minimum
-------
ordCalc> min(w**4,w**3*2 + w**2 + 4)
ω^3·2 + ω^2 + 4
ordCalc> min((w**1)**w, w**(1**w))
ω
                    ''')
                    continue
                
                calculate(unos, memory)
            except CalculatorError as e:
                print("Greška u ",e.num,". naredbi: ",e.message)
    except KeyboardInterrupt:
        print()
        
    print("\nHvala na korištenju!")
    time.sleep(1)


if __name__ == '__main__':
    main()
