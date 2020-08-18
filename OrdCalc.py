from ordinalni_kalkulator import *
import re
import time

w = Ordinal.omega

class CalculatorError(Exception):
    pass

def calculate(unos, memory):    
    for naredba in unos.split(";"):
        naredba = naredba.strip()
        #print(naredba)
        if "var" in naredba:
            y = naredba[4:].replace(" ","")
            
            if "+=" in naredba:
                variable, value = y.split('+=')
                value = variable + "+" + value
                
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
                
                if re.match(r"^[ \*\+()w0-9]*$", value):
                    try:
                        v = eval(value)
                        memory[variable] = v
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

            if re.match(r"^[ =><\*\+()w0-9]*$", naredba):
                try:
                    print(eval(naredba))
                except:
                    print("Izraz se ne može izračunati.")
            else:
                print("Izraz nije definiran.\nAko ste htjeli pridjeliti vrijednost varijabli stavite 'var' na početak.")
            


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


                    ''')
                    continue
                
                calculate(unos, memory)
            except CalculatorError as e:
                print(e)
    except KeyboardInterrupt:
        print()
        
    print("\nHvala na korištenju!")
    time.sleep(2)


if __name__ == '__main__':
    main()
