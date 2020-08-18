from functools import total_ordering
from collections import Counter
import copy


@total_ordering
class Ordinal():
    """ Klasa koja reprezentira ordinale u Cantorovoj normalnoj formi. """
    
    def __init__(self, arg):
        """
        Konstruktor ordinala.
        Argumenti:
        arg -- prirodni broj ili dict čiji su ključevi Ordinal, a vrijednosti prirodni brojevi
        """
        if isinstance(arg, int):
            if arg >= 0:
                arg = {Ordinal.zero: arg}
            else:
                raise ValueError("Ordinal ne može biti negativan broj")
        summands = Counter(arg)
        self.summands = Counter()
        
        for exp, coeff in summands.items():
            if not isinstance(coeff, int) or coeff < 0:
                raise ValueError("Koeficijent mora biti prirodni broj")

            if not isinstance(exp, Ordinal):
                raise ValueError("Eksponent mora biti Ordinal")

            if coeff > 0:
                self.summands[exp] += coeff
    
    @classmethod
    def coerce(cls, arg):
        """
        Prima bilo kakav objekt i ako je moguće pretvara ga u Ordinal.
        Argumenti koji su prhvatljivi za pretvorbu:
        arg -- prirodni broj ili Ordinal
        """
        if isinstance(arg, int) and arg >= 0:
            return cls(arg)
        else:
            return arg
            
        
    @classmethod
    def fromnat(cls, n):
        """ Pretvara obični prirodan broj iz tipa int u tip Ordinal. """
        if not isinstance(n, int) or n < 0:
                raise ValueError("Argument funkcije mora biti prirodni broj")
        return cls({Ordinal.zero:n})
    
    #! Sljedeće dvije funkcije su mi totalno čudni interfejs za sumande, mislim da sam o tome već pričao. 
    #! Koliko vidim, jedini kontekst u kojem ih pozivate je prvo s argumentom 0, pa onda svaki sljedeći poziv sa
    #! za jedan većim argumentom. Python to puno čišće opisuje _iteratorima_. 
    #! for coef, exp in self.cnf():, ili it = self.cnf(), pa onda kad Vam zatreba sljedeći par: coef, exp = next(it)
    #! Naravno, možete imati i dva nezavisna iteratora, ali koliko vidim, ionako Vam koeficijent i eksponent uvijek
    #! trebaju u paru.
    
    #! Alternativno, (mislim da sam i o tome već pričao) ako su Vam iteratori prekomplicirani, mislim da bi imalo smisla
    #! reprezentirati Ordinal kao listu parova [(exp, coef), (exp, coef), ...] sortiranih obrnuto po eksponentima.
    #! To efektivno imate s ovim donjim list(dict(sorted(.items()))), samo nema smisla sortirati svaki put iznova, pobogu.
    #! Dobra stvar je da onda uređaj bude doslovno pythonov < na takvim listama (leksikografski).
    
    #! Loša vijest je da Vam ipak tu i tamo treba nekakav dict-access iz ključeva u vrijednosti. Ali ovako na prvi pogled,
    #! jedino vidim da vadite ključeve 0 i 1 (odnosno Ordinal.zero i Ordinal.one:). Ako i ne, daleko je manje posla
    #! _tu_ imati linearni search po listi parova nego sort svaki put kad vadite bilo koji coef ili exp po rednom broju.
    def coefficient(self, k):
        """ Vraća faktor od k-tog sumanda ordinala self. """
        return list(self.summands.values())[k] 
    
    def exponent(self, k):
        """ Vraća eksponent od k-tog sumanda ordinala self. """
        return list(self.summands.keys())[k] 
    
    
    @property
    def is_successor(self):
        """
        Funkcija koja određuje je li ordinal sljedbenik.
        Pomoću toga se može odrediti i je li granični ordinal sa "not alfa.is_successor", gdje je alfa Ordinal.
        """
        return self.summands[Ordinal.zero] != 0

    @staticmethod
    def _make_string(exp,coef):
        """ Pretvara sumand u latex izraz. """
        s = ''
        if exp == 0:
            return s + str(coef)
        if exp < Ordinal.omega:
            exp = exp.coefficient(0)

        if exp == 0:
            s += str(coef)
        elif coef == 0:
            s += '0'
        else:
            s += r'\omega'
            
            if isinstance(exp, int) and exp > 1:
                s += '^{' + str(exp) + '}'
            elif isinstance(exp, Ordinal):
                s += '^{'
                if exp != Ordinal.omega:
                    s += '('
                s += str(exp)
                if exp != Ordinal.omega:
                    s += ')'
                s += '}'
            if coef != 1:
                s += r'\cdot' + str(coef)
        return s
    
    def __str__(self):
        if self == 0:
            return '0'
        summands = [self._make_string(exp,self.summands[exp]) for exp in self.summands]
        return ' + '.join(summands)
    
    @staticmethod
    def _make_direct_str(exp,coef):
        """ Pretvara sumand u python izraz. """
        s = ''
        if exp == 0:
            return s + repr(coef)
        if exp < Ordinal.omega:
            exp = exp.coefficient(0)

        if exp == 0:
            s += repr(coef)
        elif coef == 0:
            s += '0'
        else:
            s += 'w'
            
            if isinstance(exp, int) and exp != 1:
                s += '**' + repr(exp)
            elif isinstance(exp, Ordinal):
                s += '**'
                if exp != Ordinal.omega:
                    s += '('
                s += repr(exp)
                if exp != Ordinal.omega:
                    s += ')'
            if coef != 1:
                s += '*' + repr(coef)
        return s
    
    def __repr__(self):
        summands = [self._make_direct_str(exp,self.summands[exp]) for exp in self.summands]
        return ' + '.join(summands)
    
    def _repr_latex_(self):
        return r"$%s$" % str(self)
    
    def __bool__(self):
        return self != Ordinal.zero
    
    def __eq__(self, other):
        if isinstance(other, int):
            other = Ordinal(other)

        if isinstance(other, Ordinal):
            return self.summands == other.summands
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, int):
            other = Ordinal(other)
            
        if isinstance(other, Ordinal):
            i = 0
            j = 0

            while i < len(self.summands) and j < len(other.summands):
                coef1 = self.coefficient(i)
                coef2 = other.coefficient(j)
                exp1 = self.exponent(i)
                exp2 = other.exponent(j)

                if exp1 > exp2:
                    return False
                elif exp2 > exp1:
                    return True
                else:
                    if coef1 > coef2:
                        return False
                    elif coef2 > coef1:
                        return True

                i += 1
                j += 1

            if i >= len(self.summands):
                if j >= len(other.summands):
                    return False
                return True
            else:
                return False
        else:
            return NotImplemented
    
    def __hash__(self):
        return hash((Ordinal, frozenset(self.summands.items())))
    
    def __add__(self, other):
        """
        Računa sumu ordinala self + other zadržavajući u CNF.
        Argumenti:
        self -- Ordinal
        other -- prirodni broj ili Ordinal
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
                
        if self == 0:
            return other
        if other == 0:
            return self
                
        i = 0
        j = 0
        
        exp1 = self.exponent(i)
        exp2 = other.exponent(j)
        
        
        result = Counter()
        
        while exp1 > exp2:
            coef1 = self.coefficient(i)
            result[exp1] = coef1
            i += 1
            
            if i >= len(self.summands):
                break

            exp1 = self.exponent(i)
            
        
        resultCoef = other.coefficient(j)
        if i < len(self.summands) and exp1 == exp2:
            resultCoef += self.coefficient(i)
        
        result[exp2] = resultCoef

        j += 1
        while j < len(other.summands):
            exp2 = other.exponent(j)
            result[exp2] = other.summands[exp2]
            j += 1
            
        return Ordinal(result)

    def __radd__(self, other):
        """
        Računa sumu ordinala other + self zadržavajući u CNF.
        Argumenti:
        self -- Ordinal
        other -- prirodni broj
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
        
        return other + self
    
    def __sub__(self, other):
        """
        Računa razliku ordinala self - other zadržavajući u CNF.
        Mora vrijediti self >= other.
        Argumenti:
        self -- Ordinal
        other -- prirodni broj ili Ordinal
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
                
        if self < other:
            raise ArithmeticError("Ne može se oduzeti ordinal od strogo manjeg ordinala.")
        if not other:
            return self
        
        # self >= other > 0
                
        i = 0
        
        exp1 = self.exponent(i)
        exp2 = other.exponent(i)
        
        
        result = Counter()
        
        while exp1 == exp2:
            coef1 = self.coefficient(i)
            coef2 = other.coefficient(i)
                
            result[exp1] = coef1 - coef2
            i += 1
            
            if coef1 != coef2:
                break
            
            if i >= len(self.summands) or i >= len(other.summands):
                break

            exp1 = self.exponent(i)
            exp2 = other.exponent(i)
            

        while i < len(self.summands):
            exp1 = self.exponent(i)
            result[exp1] = self.summands[exp1]
            i += 1
            
        return Ordinal(result)
    
    def __rsub__(self, other):
        """
        Računa razliku ordinala other - self zadržavajući u CNF.
        Mora vrijediti other >= self.
        Argumenti:
        self -- Ordinal
        other -- prirodni broj
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
        
        return other - self
            
    def __mul__(self, other):
        """
        Računa produkt ordinala self * other zadržavajući u CNF.
        Argumenti:
        self -- Ordinal
        other -- prirodni broj ili Ordinal
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented

        if self == 0 or other == 0:
            return Ordinal.zero
        
        i = 0
        j = 0
        
        exp1 = self.exponent(i)
        exp2 = other.exponent(j)
        
        result = Counter()
        
        while exp2 > 0:
            resultExp = exp1 + exp2
            result[resultExp] += other.coefficient(j)
            j += 1
            
            if j >= len(other.summands):
                break
                
            exp2 = other.exponent(j)
        
        if j < len(other.summands):
            resultCoef = other.coefficient(j) * self.coefficient(i)
            result[exp1] += resultCoef
            
            i += 1
            while i < len(self.summands):
                exp1 = self.exponent(i)
                result[exp1] += self.summands[exp1]
                i += 1
            
        return Ordinal(result)

    def __rmul__(self, other):
        """
        Računa produkt ordinala other * self zadržavajući u CNF.
        Argumenti:
        self -- Ordinal
        other -- prirodni broj
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
        
        return other * self
    
    def __floordiv__(self, other):
        """
        Računa self // other, odnosno količnik ordinala self / other zadržavajući u CNF.
        Argumenti:
        self -- Ordinal
        other -- prirodni broj ili Ordinal različiti od nula
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented

        if not other:
            raise ZeroDivisionError('Dijeljenje sa ordinalom nula nije moguće.')
        
        if self < other:
            return Ordinal.zero
        elif self == other:
            return Ordinal.one
        
        i = 0
        j = 0
        
        exp1 = self.exponent(i)
        exp2 = other.exponent(j)
        
        result = Counter()
        
        while exp1 > exp2:
            resultExp = exp1 - exp2
            result[resultExp] += self.coefficient(i)
            i += 1
            
            if i >= len(self.summands):
                break
                
            exp1 = self.exponent(i)
            
        
        if exp1 == exp2:
            coef1 = self.coefficient(i)
            coef2 = other.coefficient(j)

            if coef1 > coef2:
                resultCoef = coef1 // coef2
                result[Ordinal.zero] += resultCoef
                
            
        return Ordinal(result)

    def __rfloordiv__(self, other):
        """
        Računa other // self, odnosno količnik ordinala other / self zadržavajući u CNF.
        Argumenti:
        self -- Ordinal
        other -- prirodni broj različiti od nula
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
        
        return other // self
    
    def __mod__(self, other):
        """
        Računa self % other, odnosno ostatak dijeljenja ordinala self / other zadržavajući u CNF.
        Argumenti
        self -- Ordinal
        other -- prirodni broj ili Ordinal različiti od nula
        """
        return self - other * (self // other)
    
    def __rmod__(self, other):
        """
        Računa other % self, odnosno ostatak dijeljenja ordinala other / self zadržavajući u CNF.
        Argumenti
        self -- Ordinal
        other -- prirodni broj različiti od nula
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
        
        return other % self
    
    def __truediv__(self, other):
        """
        Računa količnik i ostatak dijeljenja self / other zadržavajući u CNF.
        Argumenti:
        self -- Ordinal
        other -- prirodni broj ili Ordinal različiti od nula
        """
        q = self // other
        r = self - other*q
        return q,r
    
    def __rtruediv__(self, other):
        """
        Računa količnik i ostatak dijeljenja other / self zadržavajući u CNF.
        Argumenti
        self -- Ordinal
        other -- prirodni broj različiti od nula
        """
        q = other // self
        r = other - self*q
        return q,r
            
    def __pow__(self, other):
        """
        Računa rezultat potenciranja ordinala self ^ other zadržavajući u CNF.
        Argumenti:
        self -- Ordinal
        other -- prirodni broj ili Ordinal
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
        
        natTerm = False #ima li other = w^a1*n1+...+w^ak*nk u cnf zapisu ak=0
        
        if other == 0:
            return Ordinal.one
        
        if self == 0:
            return Ordinal.zero
        
        if other < Ordinal.omega:
            if self < Ordinal.omega:
                # self < omega, other < omega
                result = self.summands[Ordinal.zero] ** other.summands[Ordinal.zero]

            else:
                # self >= omega, other < omega
                coef2 = other.coefficient(0)
                
                if coef2 == 0:
                    return Ordinal.one
                if coef2 == 1:
                    return self
                
                i = 0
                j = 0
                result = Counter()
                
                exp1 = self.exponent(0)
                coef1 = self.coefficient(0)
                
                tmp = exp1*(coef2-1)
                
                while True:
                    if exp1 == 0:
                        break
                        
                    tmpExp = tmp + exp1
                    result[tmpExp] = coef1
                    i += 1
                    
                    if i >= len(self.summands):
                        break
                        
                    exp1 = self.exponent(i)
                    coef1 = self.coefficient(i)
                    
                if exp1 == 0:
                    if coef1 > 0:
                        tmpCoef = self.coefficient(0) * coef1;

                        for j in range(1,coef2):
                            tmpExp =  self.exponent(0) * (coef2-j)
                            result[tmpExp] = tmpCoef
                            
                            i = 1
                            while i < len(self.summands)-1:
                                exp1 = self.exponent(i)
                                coef1 = self.coefficient(i)

                                tmpExp =  self.exponent(0) * (coef2-j-1)

                                if tmpExp == 0:
                                    return Ordinal.zero

                                tmpExp = tmpExp + exp1

                                if tmpExp == 0:
                                    return Ordinal.zero
                                result[tmpExp] = coef1
                                i += 1

                        result[Ordinal.zero] = coef1
                    
        else:
            if self == 0:
                result = 0
            elif self == 1:
                result = 1
            elif self < Ordinal.omega:
                # 1 < self < omega, other >= omega
                result = Counter()
                tmp = Counter()

                for i in range(len(other.summands)):
                        exp2 = other.exponent(i)
                        coef2 = other.coefficient(i)
                        if exp2:
                            if exp2 < Ordinal.omega:
                                    exp2 = Ordinal(exp2.coefficient(0) - 1)
                            tmp[exp2] = coef2;
                        else:
                            natTerm = True

                if natTerm == True:
                    resCoef = self.coefficient(0) ** coef2;
                else:
                    resCoef = 1;

                result[Ordinal(tmp)] = resCoef
            else:
                # self >= omega, other >= omega
                exp1 = self.exponent(0)
                
                result = Counter()
                tmp = Counter()

                for i in range(len(other.summands)):
                        exp2 = other.exponent(i)
                        coef2 = other.coefficient(i)
                        if exp2:
                            tmp[exp2] = coef2
                        else:
                            natTerm = True

                tmpExp = exp1*Ordinal(tmp)
                if tmpExp == 0:
                    return Ordinal.zero
                result[tmpExp] = 1
                
                
                if natTerm == True:
                    tmp2 = self ** coef2
                    return Ordinal(result) * tmp2

        return Ordinal(result)
    
    def __rpow__(self, other):
        """
        Računa rezultat potenciranja ordinala other ^ self zadržavajući u CNF.
        Argumenti:
        self -- Ordinal
        other -- prirodni broj
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
        
        return other ** self
            
    
    def Isummation(alfa_k,beta):
        """
        Funkcija računa sumu izraza alfa_k koji predstavlja ordinal do granice beta = w*i1+i0.
        Ovo je heuristička metoda koja daje točan izraz u većini slučajeva, no ne uvijek.
        Argumenti:
        alfa_k -- lambda izraz koji ovisi o k te uvrštavanjem nekog Ordinala k postaje Ordinal
        beta -- prirodni broj ili Ordinal
        """
        #! Nemam ništa protiv da ovo ostane kao nekakva heuristika, ali treba dokumentirati da nije egzaktno
        #! (za razliku od osnovnih operacija, koje bi morale biti egzaktne).
        
        beta = Ordinal.coerce(beta)
        if not isinstance(beta, Ordinal):
            return NotImplemented
        
        sum = Ordinal.zero
        
        for i in range(beta.summands[Ordinal.one]):
            alfa_fp2 = Ordinal.coerce(alfa_k(Ordinal.omega*i+2))
            
            if alfa_fp2:
                sumExp = alfa_fp2.exponent(0)+1
                sum = sum + Ordinal({sumExp:1})
            
        tmp = Ordinal.omega*beta.summands[Ordinal.one]
        if beta.summands[Ordinal.zero] != 0:
            sum = sum + alfa_k(tmp+0)
            for i in range(1,beta.summands[Ordinal.zero]):
                sum = sum + alfa_k(tmp+i)
        
        return sum
        
    def Iproduct(alfa_k,beta):
        """
        Funkcija računa umnožak izraza alfa_k koji predstavlja ordinal do granice beta = w*i1+i0.
        Ovo je heuristička metoda koja daje točan izraz u većini slučajeva, no ne uvijek.
        Argumenti:
        alfa_k -- lambda izraz koji ovisi o k te uvrštavanjem nekog Ordinala k postaje Ordinal
        beta -- prirodni broj ili Ordinal
        """
        beta = Ordinal.coerce(beta)
        if not isinstance(beta, Ordinal):
            return NotImplemented
        
        prod = Ordinal.one
        
        if not Ordinal.coerce(alfa_k(0)):
            return Ordinal.zero
        
        for i in range(beta.summands[Ordinal.one]):
            alfa_fp2 = Ordinal.coerce(alfa_k(Ordinal.omega*i+2))
            
            if alfa_fp2 == Ordinal.zero:
                prod = 0
            elif alfa_fp2 != Ordinal.one:
                if alfa_fp2 < Ordinal.omega:
                    prodExp = Ordinal.one
                else:
                    prodExp = alfa_fp2.exponent(0) * Ordinal.omega

                prod = prod*Ordinal({prodExp:1})
            
        tmp = Ordinal.omega*beta.summands[Ordinal.one]
        if beta.summands[Ordinal.zero] != 0:
            prod = prod*alfa_k(tmp+0)
            for i in range(1,beta.summands[Ordinal.zero]):
                prod = prod*alfa_k(tmp+i)
        
        return prod


Ordinal.zero = Ordinal({})
Ordinal.one = Ordinal({Ordinal.zero:1})
Ordinal.omega = Ordinal({Ordinal.one:1})
