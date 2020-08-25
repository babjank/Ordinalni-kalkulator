from ordinalni_kalkulator import *
import re
import time

w = Ordinal.omega

class CalculatorError(Exception):
    pass

def calculate(unos, memory):    
    for naredba in unos.split(";"):
        naredba = naredba.strip()

        if "var" in naredba:
            y = naredba[4:].replace(" ","")
            
            if "+=" in naredba:
                variable, value = y.split('+=')
                value = variable + "+" + value

            elif "-=" in naredba:
                variable, value = y.split('-=')
                value = variable + "-" + value

            elif "%=" in naredba:
                variable, value = y.split('%=')
                value = variable + "%" + value 

            elif "//=" in naredba:
                variable, value = y.split('//=')
                value = variable + "//" + value
                
            elif "**=" in naredba:
                variable, value = y.split('**=')
                value = variable + "**" + value
                
            elif "*=" in naredba:
                variable, value = y.split('*=')
                value = variable + "*" + value
                
            else:
                variable, value = y.split('=')

            #print(variable, value)

            if variable != "w" and re.match(r"^[a-zA-Z_$][a-zA-Z_$0-9]*$", variable):
                for i in memory:
                    if i in value:
                        value = value.replace(i,"("+repr(memory[i])+")")
                
                if re.match(r"^[ \*\+\/\-%()w0-9]*$", value):
                    try:
                        v = eval(value)
                        v = Ordinal.coerce(v)
                        
                        if isinstance(v,Ordinal):
                            memory[variable] = v
                        else:
                            print("Izraz sa desne strane ne odgovara Ordinalu.")
                    except:
                        print("Izraz sa desne strane se ne može izračunati.")
                else:
                    print("Izraz sa desne strane nije definiran.")
            else:
                print("Ime varijable može se sadržavati od slova, brojeva i znaka $.\nNe može počinjati sa brojem te biti samo slovo w.")
        else:
            for i in memory:
                if i in naredba:
                    naredba = naredba.replace(i,"("+repr(memory[i])+")")

            if re.match(r"^[ =><\*\+\/\-%()w0-9]*$", naredba):
                try:
                    print(repr(eval(naredba)))
                except:
                    print("Izraz se ne može izračunati.")
            else:
                print("Izraz nije definiran.\nAko ste htjeli dodijeliti vrijednost varijabli stavite 'var' na početak.")
            


def main():
    print("ORDINALNI KALKULATOR by BB")
    print("==========================\n")

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

Ovo je aplikacija napravljena za provođenje aritmetičkih operacija
nad ordinalnim brojevima. Operacije koje je moguće provoditi su:

Uspoređivanje
-------------
ordCalc> w < 1
False
ordCalc> w == 1 + w
True

Zbrajanje
---------
ordCalc> 2 + w
w
ordCalc> (w ** 2 + w * 1 + 4) + (w * 2 + 3)
w**2 + w*3 + 3

Množenje
--------
ordCalc> 2 * w
w
ordCalc> (w ** w * 3 + w) * 2
w**w*6 + w

Potenciranje
------------
ordCalc> 2 ** w
w
ordCalc> (w + 1) ** (w + 1)
w**(w + 1) + w**w

Dodjeljivanje vrijednosti
-------------------------
Prije varijable kojoj želite dodijeliti vrijednost stavite riječ "var".

ordCalc> var x = w + 1
ordCalc> x
w + 1
ordCalc> var x += w * 2 + 4
ordCalc> x
w*3 + 4

Moguće je navesti više naredbi u jednom retku, odvajamo ih separatorom ";".

ordCalc> var y = w ** w + w ** 3 * 2 + w + 4; var y += 5; y
w**w + w**3*2 + w + 9

Oduzimanje
----------
ordCalc> w - 1
w
ordCalc> var a = w**w*3 + w**3*5 + w + 4; var b = w**w*3 + w**3*3 + 2; a - b
w**3*2 + w + 4
ordCalc> var c = a - b; b + c == a
True

Dijeljenje
----------
ordCalc> var a = w**w + w**3*2 + w**2*5 + 4; var b = w**2*4 + w*7 + 5; a / b
(w**w + w*2 + 1, w**2 + 4)
ordCalc> a // b
w**w + w*2 + 1
ordCalc> a % b
w**2 + 4
ordCalc>  var x = w**2 + w; x / w
(w + 1, 0)
ordCalc> var q = x // w; var r = x % w; w*q + r == x
True
                    ''')
                    continue
                
                calculate(unos, memory)
            except CalculatorError as e:
                print(e)
    except KeyboardInterrupt:
        print()
        
    print("\nHvala na korištenju!")
    time.sleep(1)


if __name__ == '__main__':
    main()
