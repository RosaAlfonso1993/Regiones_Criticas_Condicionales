import threading
import logging
import random
import time
from regionCondicional import *

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class RecursoDato(Recurso):
    dato1 = 0
    numLectores = 0
    numEscritores =0
    escribiendo = False


datos = RecursoDato()

def condicionLector():
    return (not datos.escribiendo) and (datos.numEscritores == 0)

def condicionEscritor():
    return not datos.escribiendo
    # return (datos.numLectores==0) and (not datos.escribiendo)

def conditionTrue():
    return True


regionLector = RegionCondicional(datos, condicionLector)
regionEscritor = RegionCondicional(datos, condicionEscritor)
regionLE = RegionCondicional(datos, conditionTrue)


@regionLector.condicion
def doLector1():
    datos.numLectores += 1

@regionLE.condicion
def doLector2():
    datos.numLectores -= 1

@regionLE.condicion
def doEscritor1():
    datos.numEscritores += 1

@regionEscritor.condicion
def doEscritor2():
    datos.escribiendo= True
    datos.numEscritores -=1

@regionLE.condicion
def doEscritor3():
    datos.escribiendo=False

def Lector():
    while True:
        doLector1()
        logging.info(f'Lector lee dato1 = {regionLector.recurso.dato1}')
        time.sleep(1)
        doLector2()
      #  time.sleep(random.randint(1,2))

def Escritor():
    while True:
        doEscritor1()
        doEscritor2()
        regionEscritor.recurso.dato1 = random.randint(0,100)
        logging.info(f'Escritor escribe dato1 = {regionEscritor.recurso.dato1}')
        doEscritor3()
        time.sleep(3)
        #time.sleep(random.randint(2,3))


def main():
    nlector = 20
    nescritor = 2

    for k in range(nlector):
        threading.Thread(target=Lector, daemon=True).start()

    for k in range(nescritor):
        threading.Thread(target=Escritor, daemon=True).start()

    time.sleep(300)


if __name__ == "__main__":
    main()