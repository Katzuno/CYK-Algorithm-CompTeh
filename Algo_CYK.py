import json

'''
@Productie - defineste o Productie a gramaticii in F.N Chomsky (ex. A->b
'''


class Productie:
    nume = ""
    drept = []

    def __init__(self, nume, drept):
        self.nume = nume
        self.drept = drept

    def getName(self):
        return self.nume

    def getRight(self):
        return self.drept

    '''
    Cauta dupa o anumita Productie si litera
    '''

    def preiaProductieCuLitera(self, caracter):
        for val in self.drept:
            if caracter == val[0]:
                return True
        return False

    '''
    Verifica daca nodul este terminal sau nu
    @return True / False
    '''

    def verificaNeterminal(self, nod):
        for val in self.drept:
            if val == nod:
                return True
        return False


class AlgoCYK:
    productii = []
    cuvant = ""
    tabel = {}

    def __init__(self, citit):
        self.cuvant = citit["cuvant"]
        for productie in citit["productii"]:
            self.productii.append(Productie(productie["nume"], productie["drept"]))

    def preiaCuvant(self):
        return self.cuvant

    '''
    Vom căuta în gramatică pentru fiecare literă mică de ce
    neterminale poate fi generată.
    '''

    def Pasul1(self):
        self.tabel[1] = {}
        for i in range(1, len(self.cuvant) + 1):
            self.tabel[1][i] = []
            for Productie in self.productii:
                if Productie.preiaProductieCuLitera(self.cuvant[i - 1]):
                    self.tabel[1][i].append(Productie.getName())

    '''
    Reuniunea a doua multimi, exemplu {A} U {B,C}

    @m1 - multimea 1
    @m2 - multimea 2
    @return reuniune
    '''

    def reuniune(self, m1, m2):
        for val in m2:
            if val not in m1:
                m1.append(val)
        return m1

    '''
    Produsul a doua multimi, exempli {A} X {B,C}

    @m1 - multimea 1
    @m2 - multimea 2
    @return produs
    '''

    def produs(self, m1, m2):
        rezultat = []
        for m1_elem in m1:
            for m2_elem in m2:
                elem_nou = m1_elem + m2_elem
                if elem_nou not in rezultat:
                    rezultat.append(elem_nou)
        return rezultat

    def preiaproductiiCuLitere(self, drept):
        productii = []
        for Productie in self.productii:
            if Productie.verificaNeterminal(drept):
                productii.append(Productie.getName())
        return productii

    '''
    Valoare pe care o calculăm este Vi j pentru cuvântul care începe la poziţia i şi are
    lungimea j.
    Prima parte conţine primele k litere din cuvânt. Deci va
    începe la poziţia i (la fel ca întreg cuvântul) şi va avea lungime k, deci Vi k.
    A doua parte conţine restul de litere, adică j–k, şi începe cu
    k poziţii mai în dreapta faţă de cuvântul total, adică la i+k, deci avem Vi+k, j-k.

    @i -Incepe la pozitia i
    @j - Restul de litere, j-k
    @return - Vij
    '''

    def calcVij(self, i, j):
        rezultat = {}
        rezultat['final'] = []
        for k in range(1, j):
            tmp = self.produs(self.tabel[k][i], self.tabel[j - k][i + k])
            rezultat[k] = []
            for val in tmp:
                elem_nou = self.preiaproductiiCuLitere(val)
                rezultat[k] = self.reuniune(rezultat[k], elem_nou)
                print(val, rezultat)
                print()
            rezultat['final'] = self.reuniune(rezultat['final'], rezultat[k])

        return rezultat['final']

    '''
    Răspunsul final pe care îl căutăm este V1, |w| adică mulţimea de neterminale din care
    putem genera cuvântul dat începând de pe prima poziţie şi având lungimea egală cu
    întreg cuvântul. Dacă în această mulţime se va găsi şi simbolul de start S, înseamnă că
    cuvântul este generat de gramatică. Dacă nu, atunci nu este generat.
    '''

    def executa(self):
        self.Pasul1()
        for j in range(2, len(self.cuvant) + 1):
            self.tabel[j] = {}
            for i in range(1, len(self.cuvant) + 1):
                if not i + j <= len(self.cuvant) + 1:
                    break
                self.tabel[j][i] = self.calcVij(i, j)
        if self.productii[0].getName() in self.tabel[len(self.cuvant)][1]:
            return True
        return False

    '''
    Afiseaza tabelul Vij
    '''

    def afiseaza(self):
        print('V(i,j)')
        for i in range(1, len(self.cuvant) + 1):
            print('i = ' + str(i), end='\t |')
        print()
        for j in range(1, len(self.cuvant) + 1):
            print('j = ' + str(j), end='\t |')
            for i in range(1, len(self.cuvant) + 1):
                if not i + j <= len(self.cuvant) + 1:
                    break
                print('{', end='')
                for val in self.tabel[j][i]:
                    print(val, end=', ')
                print('}', end=' | ')
            print()
        print('END')


if __name__ == "__main__":
    with open('gramatica.json') as f:
        data = json.load(f)
    cyk = AlgoCYK(data)
    print('Cuvantul:' + str(cyk.preiaCuvant()) + ' ' + ('' if cyk.executa() else ' NU ') + 'este acceptat')
    cyk.afiseaza()
