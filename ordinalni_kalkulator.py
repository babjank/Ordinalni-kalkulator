from functools import total_ordering

""" Ovaj modul predstavlja računalnu reprezentaciju ordinala manjih od epsilon_0
te pripadne ordinalne aritmetike nad njom. Moguće ga je koristiti individualno
ili u sklopu aplikacije OrdCalc.
"""


@total_ordering
class Ordinal():
    """ Klasa koja reprezentira ordinale u Cantorovoj normalnoj formi. """
    
    def __init__(self, arg):
        """ Kreira novi objekt klase Ordinal.
        
        Parametri
        ---------
        arg : prirodni broj ili lista parova (exp : Ordinal, coef : prirodni broj)

        Greške
        ------
        ValueError
            Ako je `arg` negativan cijeli broj ili za `arg`= [(e1,c1),...,(ek,ck)]
            ako postoji ej koji nije tipa Ordinal ili cj koji nije prirodni broj.
            Također ako ne vrijedi e1 > ... > ek.

        Napomene
        --------
        Ne preporučuje se korištenje u korisničkom kodu; preporučeni način
        konstrukcije ordinala je pomoću w, prirodnih brojeva i aritmetičkih
        operacija.

        Primjeri
        --------
        >>> Ordinal(2)
        2
        >>> Ordinal([(Ordinal.one,1),(Ordinal.zero,2)])
        w + 2
        """
        if isinstance(arg, int):
            if arg >= 0:
                arg = [(Ordinal.zero, arg)]
            else:
                raise ValueError("Ordinal ne može biti negativan broj")
        summands = arg
        self.summands = []

        tmpExp = -1
        
        for exp, coef in summands:
            if not isinstance(coef, int) or coef < 0:
                raise ValueError("Koeficijent mora biti prirodni broj")

            if not isinstance(exp, Ordinal):
                raise ValueError("Eksponent mora biti Ordinal")

            if coef > 0:
                self.summands.append((exp,coef))

            if tmpExp != -1 and tmpExp <= exp:
                raise ValueError("Eksponenti moraju biti u strogo silaznom redu.")

            tmpExp = exp
    
    @classmethod
    def coerce(cls, arg):
        """ Prima bilo kakav objekt `arg` i ako je moguće pretvara ga u Ordinal. """
        if isinstance(arg, int) and arg >= 0:
            return cls(arg)
        else:
            return arg
            
        
    @classmethod
    def fromnat(cls, n):
        """ Pretvara obični prirodan broj iz tipa int u tip Ordinal. """
        if not isinstance(n, int) or n < 0:
                raise ValueError("Argument funkcije mora biti prirodni broj")
        return cls([(Ordinal.zero, n)])
    
    def __getitem__(self, key):
        for exp, coef in self.summands:
            if exp == key:
                return coef
        return 0
        
    def __setitem__(self, key, value):
        if value == 0:
            return
        
        for i, (exp, coef) in enumerate(self.summands):
            if exp == key:
                self.summands[i] = (key, value)
                return
        
        self.summands.append((key, value))
        self.summands.sort(reverse=True)
    
    
    @property
    def is_successor(self):
        """ Je li ordinal `self` sljedbenik?

        Pomoću toga se može odrediti i je li taj ordinal granični ordinal s
        "self and not self.is_successor".
        """
        return self[Ordinal.zero] != 0

    @staticmethod
    def _make_string(exp,coef):
        """ Pretvara pribrojnik CNF-a (`exp`,`coef`) u latex izraz. """
        s = ''
        if exp == 0:
            return s + str(coef)
        if exp < Ordinal.omega:
            exp = exp.summands[0][1]

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
                s += r' \cdot ' + str(coef)
        return s
    
    def __str__(self):
        if self == 0:
            return '0'
        summands = [self._make_string(exp,coef) for exp,coef in self.summands]
        return ' + '.join(summands)
    
    @staticmethod
    def _make_direct_str(exp,coef):
        """ Pretvara pribrojnik CNF-a (`exp`,`coef`) u python izraz. """
        s = ''
        if exp == 0:
            return s + repr(coef)
        if exp < Ordinal.omega:
            exp = exp.summands[0][1]

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
        if self == 0:
            return '0'
        summands = [self._make_direct_str(exp,coef) for exp,coef in self.summands]
        return ' + '.join(summands)
    
    def _repr_latex_(self):
        return r"$%s$" % str(self)
    
    def __bool__(self):
        """ Je li ordinal `self` različit od 0? """
        return self != Ordinal.zero
    
    def __eq__(self, other):
        """ Jesu li ordinali `self` i `other` jednaki? """
        other = Ordinal.coerce(other)

        if isinstance(other, Ordinal):
            return self.summands == other.summands
        else:
            return False

    def __lt__(self, other):
        """ Je li ordinal `self` manji od `other`? """
        other = Ordinal.coerce(other)
            
        if isinstance(other, Ordinal):
            i = 0
            j = 0

            while i < len(self.summands) and j < len(other.summands):
                coef1 = self.summands[i][1]
                coef2 = other.summands[j][1]
                exp1 = self.summands[i][0]
                exp2 = other.summands[j][0]

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
        return hash((Ordinal, frozenset(self.summands)))
    
    def __add__(self, other):
        """ Zbroj ordinala `self` i `other`, tim redom.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj ili Ordinal

        Primjeri
        --------
        >>> a = Ordinal.fromnat(2)
        >>> b = w + 2
        >>> a + b
        w + 2
        >>> b + 2
        w + 4
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
        
        exp1 = self.summands[i][0]
        exp2 = other.summands[j][0]
        
        
        result = Ordinal([])
        
        while exp1 > exp2:
            coef1 = self.summands[i][1]
            result[exp1] = coef1
            i += 1
            
            if i >= len(self.summands):
                break

            exp1 = self.summands[i][0]
            
        
        resultCoef = other.summands[j][1]
        if i < len(self.summands) and exp1 == exp2:
            resultCoef += self.summands[i][1]
        
        result[exp2] = resultCoef

        j += 1
        while j < len(other.summands):
            exp2 = other.summands[j][0]
            result[exp2] = other[exp2]
            j += 1
            
        return result

    def __radd__(self, other):
        """ Zbroj ordinala `other` i `self`, tim redom.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj

        Primjeri
        --------
        >>> a = Ordinal.fromnat(2)
        >>> b = w + 2
        >>> 2 + a
        4
        >>> 2 + b
        w + 2
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
        
        return other + self

    __iadd__ = __add__
    
    def __sub__(self, other):
        """ Razlika ordinala `self` i `other`, tim redom.
        Mora vrijediti `self` >= `other`.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj ili Ordinal

        Greške
        ------
        ArithmeticError
            Ako je `self` manji od `other`.

        Primjeri
        --------
        >>> b = w + 2
        >>> b - 2
        w + 2
        >>> b - w
        2
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
        
        exp1 = self.summands[i][0]
        exp2 = other.summands[i][0]
        
        
        result = Ordinal([])
        
        while exp1 == exp2:
            coef1 = self.summands[i][1]
            coef2 = other.summands[i][1]
                
            result[exp1] = coef1 - coef2
            i += 1
            
            if coef1 != coef2:
                break
            
            if i >= len(self.summands) or i >= len(other.summands):
                break

            exp1 = self.summands[i][0]
            exp2 = other.summands[i][0]
            

        while i < len(self.summands):
            exp1 = self.summands[i][0]
            result[exp1] = self[exp1]
            i += 1
            
        return result
    
    def __rsub__(self, other):
        """ Razlika ordinala `other` i `self`, tim redom.
        Mora vrijediti `other` >= `self`.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj

        Greške
        ------
        ArithmeticError
            Ako je `other` manji od `self`.

        Primjeri
        --------
        >>> a = Ordinal.fromnat(2)
        >>> 2 - a
        0
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
        
        return other - self

    __isub__ = __sub__
            
    def __mul__(self, other):
        """ Produkt ordinala `self` i `other`, tim redom.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj ili Ordinal

        Primjeri
        --------
        >>> b = w + 2
        >>> b * 2
        w*2 + 2
        >>> w * b
        w**2 + w*2
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented

        if self == 0 or other == 0:
            return Ordinal.zero
        
        i = 0
        j = 0
        
        exp1 = self.summands[i][0]
        exp2 = other.summands[j][0]
        
        result = Ordinal([])
        
        while exp2 > 0:
            resultExp = exp1 + exp2
            result[resultExp] += other.summands[j][1]
            j += 1
            
            if j >= len(other.summands):
                break
                
            exp2 = other.summands[j][0]
        
        if j < len(other.summands):
            resultCoef = other.summands[j][1] * self.summands[i][1]
            result[exp1] += resultCoef
            
            i += 1
            while i < len(self.summands):
                exp1 = self.summands[i][0]
                result[exp1] += self[exp1]
                i += 1
            
        return result

    def __rmul__(self, other):
        """ Produkt ordinala `other` i `self`, tim redom.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj

        Primjeri
        --------
        >>> b = w + 2
        >>> 2 * b
        w + 4
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
        
        return other * self

    __imul__ = __mul__
    
    def __floordiv__(self, other):
        """ Količnik dijeljenja ordinala `self` i `other`, tim redom.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj ili Ordinal

        Greške
        ------
        ZeroDivisionError
            Ako je `other` jednak nula.

        Primjeri
        --------
        >>> b = w + 2
        >>> b // 2
        w + 1
        >>> b // w
        1
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
        
        exp1 = self.summands[i][0]
        exp2 = other.summands[j][0]
        
        result = Ordinal([])
        
        while exp1 > exp2:
            resultExp = exp1 - exp2
            result[resultExp] += self.summands[i][1]
            i += 1
            
            if i >= len(self.summands):
                break
                
            exp1 = self.summands[i][0]
            
        
        if exp1 == exp2:
            coef1 = self.summands[i][1]
            coef2 = other.summands[j][1]

            if coef1 % coef2 == 0:
                resultCoef = coef1 // coef2
                
                i += 1
                j += 1
                while i < len(self.summands) and j < len(other.summands):
                    coef1 = self.summands[i][1]
                    coef2 = other.summands[j][1]
                    exp1 = self.summands[i][0]
                    exp2 = other.summands[j][0]

                    if exp1 > exp2:
                        result[Ordinal.zero] += resultCoef
                        break
                    elif exp2 > exp1:
                        break
                    else:
                        if coef1 > coef2:
                            result[Ordinal.zero] += resultCoef
                            break
                        elif coef2 > coef1:
                            break

                    i += 1
                    j += 1

                    if i == len(self.summands) and j == len(other.summands):
                        result[Ordinal.zero] += resultCoef

            elif coef1 > coef2:
                resultCoef = coef1 // coef2
                result[Ordinal.zero] += resultCoef
                
        return result

    def __rfloordiv__(self, other):
        """ Količnik dijeljenja ordinala `other` i `self`, tim redom.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj

        Greške
        ------
        ZeroDivisionError
            Ako je `self` jednak nula.

        Primjeri
        --------
        >>> a = Ordinal.fromnat(2)
        >>> 2 // a
        1
        >>> 2 // w
        0
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
        
        return other // self

    __ifloordiv__ = __floordiv__
    
    def __mod__(self, other):
        """ Ostatak dijeljenja ordinala `self` i `other`, tim redom.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj ili Ordinal

        Greške
        ------
        ZeroDivisionError
            Ako je `other` jednak nula.

        Primjeri
        --------
        >>> b = w + 2
        >>> b % 2
        0
        >>> b % w
        2
        """
        return self - other * (self // other)
    
    def __rmod__(self, other):
        """ Ostatak dijeljenja ordinala `other` i `self`, tim redom.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj

        Greške
        ------
        ZeroDivisionError
            Ako je `self` jednak nula.

        Primjeri
        --------
        >>> a = Ordinal.fromnat(2)
        >>> 2 % a
        0
        >>> 2 % w
        2
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
        
        return other % self

    __imod__ = __mod__
    
    def __divmod__(self, other):
        """ Količnik i ostatak dijeljenja ordinala `self` i `other`, tim redom.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj ili Ordinal

        Greške
        ------
        ZeroDivisionError
            Ako je `other` jednak nula.

        Primjeri
        --------
        >>> b = w + 2
        >>> divmod(b,2)
        (w + 1, 0)
        >>> divmod(b,w)
        (1, 2)
        """
        q = self // other
        r = self - other*q
        return q,r
    
    def __rdivmod__(self, other):
        """ Količnik i ostatak dijeljenja ordinala `other` i `self`, tim redom.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj

        Greške
        ------
        ZeroDivisionError
            Ako je `self` jednak nula.

        Primjeri
        --------
        >>> a = Ordinal.fromnat(2)
        >>> divmod(2,a)
        (1, 0)
        >>> divmod(2,w)
        (0, 2)
        """
        q = other // self
        r = other - self*q
        return q,r
            
    def __pow__(self, other, mod = None):
        """ Potencija ordinala `self` na `other`.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj ili Ordinal

        Primjeri
        --------
        >>> b = w + 2
        >>> b ** 2
        w**2 + w*2 + 2
        >>> w ** b
        w**w
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented

        if mod is not None:
            mod = Ordinal.coerce(mod)
        
            if not isinstance(mod, Ordinal):
                return NotImplemented
        
            base = self
            exp = other
            result = Ordinal.one
            while exp > 0:
                if exp % 2 == 0:
                    print(base,mod)
                    base = (base * base) % mod
                    exp = exp // 2
                else:
                    result = (base * result) % mod
                    exp = exp - 1
            return result
        
        natTerm = False #ima li other = w^a1*n1+...+w^ak*nk u cnf zapisu ak=0
        
        if other == 0:
            return Ordinal.one
        
        if self == 0:
            return Ordinal.zero
        
        if other < Ordinal.omega:
            if self < Ordinal.omega:
                # self < omega, other < omega
                result = self[Ordinal.zero] ** other[Ordinal.zero]

            else:
                # self >= omega, other < omega
                coef2 = other.summands[0][1]
                
                if coef2 == 0:
                    return Ordinal.one
                if coef2 == 1:
                    return self
                
                i = 0
                j = 0
                result = Ordinal([])
                
                exp1 = self.summands[0][0]
                coef1 = self.summands[0][1]
                
                tmp = exp1*(coef2-1)
                
                while True:
                    if exp1 == 0:
                        break
                        
                    tmpExp = tmp + exp1
                    result[tmpExp] = coef1
                    i += 1
                    
                    if i >= len(self.summands):
                        break
                        
                    exp1 = self.summands[i][0]
                    coef1 = self.summands[i][1]
                    
                if exp1 == 0:
                    if coef1 > 0:
                        tmpCoef = self.summands[0][1] * coef1

                        for j in range(1,coef2):
                            tmpExp =  self.summands[0][0] * (coef2-j)
                            result[tmpExp] = tmpCoef
                            
                            i = 1
                            while i < len(self.summands)-1:
                                exp1 = self.summands[i][0]
                                coef1 = self.summands[i][1]

                                tmpExp =  self.summands[0][0] * (coef2-j-1)
                                tmpExp = tmpExp + exp1

                                result[tmpExp] = coef1
                                i += 1

                        coef1 = self.summands[i][1]
                        result[Ordinal.zero] = coef1
                    
        else:
            if self == 0:
                result = 0
            elif self == 1:
                result = 1
            elif self < Ordinal.omega:
                # 1 < self < omega, other >= omega
                result = Ordinal([])
                tmp = Ordinal([])

                for i in range(len(other.summands)):
                        exp2 = other.summands[i][0]
                        coef2 = other.summands[i][1]
                        if exp2:
                            if exp2 < Ordinal.omega:
                                    exp2 = Ordinal(exp2.summands[0][1] - 1)
                            tmp[exp2] = coef2
                        else:
                            natTerm = True

                if natTerm == True:
                    resCoef = self.summands[0][1] ** coef2
                else:
                    resCoef = 1

                result[tmp] = resCoef
            else:
                # self >= omega, other >= omega
                exp1 = self.summands[0][0]
                
                result = Ordinal([])
                tmp = Ordinal([])

                for i in range(len(other.summands)):
                        exp2 = other.summands[i][0]
                        coef2 = other.summands[i][1]
                        if exp2:
                            tmp[exp2] = coef2
                        else:
                            natTerm = True

                tmpExp = exp1*tmp
                result[tmpExp] = 1
                
                
                if natTerm == True:
                    tmp2 = self ** coef2
                    return result * tmp2

        return result
    
    def __rpow__(self, other):
        """ Potencija ordinala `other` na `self`.
        
        Parametri
        ---------
        self : Ordinal
        other : prirodni broj

        Primjeri
        --------
        >>> a = Ordinal.fromnat(2)
        >>> 2 ** a
        4
        >>> 2 ** w
        w
        """
        other = Ordinal.coerce(other)
        
        if not isinstance(other, Ordinal):
            return NotImplemented
        
        return other ** self

    __ipow__ = __pow__
            
    
    def Isummation(alfa_k,beta):
        """ Suma indeksirane familije ordinalnih brojeva { `alfa_k` : k < `beta` }.
        
        Parametri
        ---------
        alfa_k : lambda izraz koji ovisi o k
            Uvrštavanjem nekog Ordinala k lambda izraz postaje Ordinal.
        beta : prirodni broj ili Ordinal
            Mora biti oblika w * i1 + i0.

        Napomene
        --------
        Ovo je heuristička metoda koja daje točan izraz u većini slučajeva,
        no ne uvijek.

        Primjeri
        --------
        >>> Ordinal.Isummation(lambda k: w + k, w)
        w**2
        >>> Ordinal.Isummation(lambda k: (w + k)**k, 4)
        w**3 + w**2*3 + w*3 + 3
        """
        beta = Ordinal.coerce(beta)
        if not isinstance(beta, Ordinal):
            return NotImplemented
        
        sum = Ordinal.zero
        
        for i in range(beta[Ordinal.one]):
            alfa_fp2 = Ordinal.coerce(alfa_k(Ordinal.omega*i+2))
            
            if alfa_fp2:
                sumExp = alfa_fp2.summands[0][0]+1
                sum = sum + Ordinal([(sumExp,1)])
            
        tmp = Ordinal.omega*beta[Ordinal.one]
        if beta[Ordinal.zero] != 0:
            sum = sum + alfa_k(tmp+0)
            for i in range(1,beta[Ordinal.zero]):
                sum = sum + alfa_k(tmp+i)
        
        return sum
        
    def Iproduct(alfa_k,beta):
        """ Produkt indeksirane familije ordinalnih brojeva { `alfa_k` : k < `beta` }.
        
        Parametri
        ---------
        alfa_k : lambda izraz koji ovisi o k
            Uvrštavanjem nekog Ordinala k lambda izraz postaje Ordinal.
        beta : prirodni broj ili Ordinal
            Mora biti oblika w * i1 + i0.

        Napomene
        --------
        Ovo je heuristička metoda koja daje točan izraz u većini slučajeva,
        no ne uvijek.
        
        Primjeri
        --------
        >>> Ordinal.Iproduct(lambda k: w, w)
        w**w
        >>> Ordinal.Iproduct(lambda k: w * k, w)
        0
        """
        beta = Ordinal.coerce(beta)
        if not isinstance(beta, Ordinal):
            return NotImplemented
        
        prod = Ordinal.one
        
        if not Ordinal.coerce(alfa_k(0)):
            return Ordinal.zero
        
        for i in range(beta[Ordinal.one]):
            alfa_fp2 = Ordinal.coerce(alfa_k(Ordinal.omega*i+2))
            
            if alfa_fp2 == Ordinal.zero:
                prod = 0
            elif alfa_fp2 != Ordinal.one:
                if alfa_fp2 < Ordinal.omega:
                    prodExp = Ordinal.one
                else:
                    prodExp = alfa_fp2.summands[0][0] * Ordinal.omega

                prod = prod*Ordinal([(prodExp,1)])
            
        tmp = Ordinal.omega*beta[Ordinal.one]
        if beta[Ordinal.zero] != 0:
            prod = prod*alfa_k(tmp+0)
            for i in range(1,beta[Ordinal.zero]):
                prod = prod*alfa_k(tmp+i)
        
        return prod


Ordinal.zero = Ordinal([])
Ordinal.one = Ordinal([(Ordinal.zero,1)])
Ordinal.omega = Ordinal([(Ordinal.one,1)])

# konstanta za korištenje pri konstrukciji
w = Ordinal.omega
