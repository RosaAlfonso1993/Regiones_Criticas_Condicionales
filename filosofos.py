import threading
import logging
import random
import time
from regionCondicional import *

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

nombres = ["Socrates", "Platón", "Aristóteles", "Locke", "Descartes"]

class RecursoDato(Recurso):
    tenedores = [False,False,False,False,False]
    libre = 5

datos = RecursoDato()


def condicionFilosofo():
    return datos.libre > 1

regionFilosofos = RegionCondicional(datos, condicionFilosofo)

@regionFilosofos.condicion
def cenaDeFilosofos1():
    numTenedorIzq = random.randint(0,4)
    numTenedorDer = random.randint(0,4)
    while numTenedorDer == numTenedorIzq:
        numTenedorDer = random.randint(0,4)
    while datos.tenedores[numTenedorIzq] or datos.tenedores[numTenedorDer]:
        time.sleep(1)
    datos.tenedores[numTenedorIzq] = True
    datos.tenedores[(numTenedorDer+1)%5] = True
    datos.libre -= 2
    logging.info(f'un filosofo esta comiendo')
    datos.tenedores[numTenedorIzq] = False
    datos.tenedores[(numTenedorDer+1)%5] = False
    datos.libre += 2

def cenar(filosofo):
    while True:
        logging.info(f'Filósofo {nombres[filosofo]} comenzó a Pensar')
        cenaDeFilosofos1()
        time.sleep(random.randint(1,3))
        logging.info(f'Filósofo {nombres[filosofo]} ya comio')


def main():
    
    for i in range(5):
        filosofos = threading.Thread(target=cenar,args=(i,), daemon=True)
        filosofos.start()
        filosofos.join()
        time.sleep(random.randint(1,5))


if __name__=='__main__':
    main()