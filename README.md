# Ordinalni-kalkulator
Implementacija ordinalnog kalkulatora koji omogućava računanje s ordinalnim brojevima.

## Korištenje

Potrebno je imati instaliran python (>verzija 3.6) na računalu. Moguće ga je preuzeti sa https://www.python.org/downloads/.
Ukoliko ste to zadovoljili, sljedeći korak je preuzimanje ovog repozitorija ili pomoću:
```
git clone https://github.com/babjank/Ordinalni-kalkulator.git
```
ili jednostavno preuzimanjem zip-a direktorija.

----------------------------------------------------------------

Moguće je koristiti modul ordinalni_kalkulator samostalno, kao što je prikazano u notebooku "Ordinalni kalkulator - primjeri", no preporuča se korištenje unutar aplikacije OrdCalc. 

Za detaljan opis kako koristiti OrdCalc upišite naredbu _help_. Ovdje je prikazan kratki pregled:

```
  ORDINALNI KALKULATOR by BB
><><><><><><><><><><><><><><><

Za sve informacije o korištenju ove aplikacije koristite naredbu help.
ordCalc> 1 + w < w + 1
True
ordCalc> (1 + w)^w == w^w
True
ordCalc> (w + 1)^1 + (w + 2)^2 + (w + 3)^3
ω^3 + ω^2·3 + ω·3 + 3
ordCalc> (w*3 + 2)*(w + w^2)*2
ω^3·2
ordCalc> (w + 1)^(w^2 + 2)
ω^(ω^2 + 2) + ω^(ω^2 + 1) + ω^(ω^2)
ordCalc> (w*2 + 4)^(w + 2) + (w^7 + 2)*(w^2*3 + 2 + w)
ω^(ω + 2)·2 + ω^(ω + 1)·8 + ω^ω·4 + ω^9·3 + ω^8
ordCalc> a = w^w^5; a; b = w^5^w; b; c = 5^w^w; c
ω^(ω^5)
ω^ω
ω^(ω^ω)
ordCalc> max(a,b,c)
ω^(ω^ω)
ordCalc> exit

Hvala na korištenju!
```

