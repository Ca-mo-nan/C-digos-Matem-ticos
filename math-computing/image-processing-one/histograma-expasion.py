import cv2
import matplotlib.pyplot as plt
import numpy as np


def cantidad_pixeles_color(lista):
    elementos = {}
    for i in lista:
        if i not in elementos:
            elementos[i] = 0

        if i in elementos.keys():
            elementos[i] += 1
    
    return elementos
             
def dibujar_histograma(pixeles):
    niveles = list(pixeles.keys())
    cantidades = list(pixeles.values())

    plt.bar(niveles, cantidades, width=1)

    plt.title("Histograma de escala de grises")
    plt.xlabel("Nivel de gris")
    plt.ylabel("Cantidad de píxeles")
    plt.show()


def reordenamiento(inicial, final):
    punto1 = (inicial[0], final[0]) #interpretalo como (x, y)
    punto2 = (inicial[1], final[1])
    pendiente = (punto2[1] - punto1[1]) / (punto2[0] - punto1[0])
    constante = final[0] - (pendiente * inicial[0])
    return (pendiente, constante)

#------------------- transformación-------------------------#
def funcion_transformacion(valores, gris):
    #De la forma T(r) = m * r + b
    new_valor = int((valores[0] * gris) + valores[1])
    return new_valor


def obtener_nuevos_valores(valores, pixeles):
    new_elementos = {}
    for i in pixeles:
        trans = funcion_transformacion(valores, i)
        new_elementos[trans] = pixeles[i]
    return new_elementos

#----------------- Reconstrucción de la imagén ------------#

def reconstruir_imagen(gris, valores):
    pendiente, constante = valores
    nueva_imagen = pendiente * gris + constante

    nueva_imagen = np.clip(nueva_imagen, 0, 255)
    return nueva_imagen.astype(np.uint8)


def Main():
    #Paso 1: cantidad de pixeles de la imagen
    imagen = cv2.imread("zorro.png")
    alto, ancho, canales = imagen.shape
    print("ancho: ", ancho, "Alto:", alto)
    #paso 2: Obtenemos la escala de grises en una lista    
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    niveles_gris = gris.flatten()
    print(niveles_gris)
    print(max(niveles_gris), min(niveles_gris))

    #Paso 3 diccionario con la cantidad
    pixeles = cantidad_pixeles_color(niveles_gris)
    print(pixeles) #observar la escala de gris con la cantidad de píxeles
    dibujar_histograma(pixeles)
    
    print("\nValores transformados\n---------------------\n")

    #Paso 4 Reordenamiento del histograma
    escala_original = (min(niveles_gris), max(niveles_gris))
    escala_nueva = (0, 255)

    valores = reordenamiento(escala_original, escala_nueva)
    print(valores) #Cálculo de la pendiente y constante de la función de transformación
    new_valores = obtener_nuevos_valores(valores, pixeles)
    dibujar_histograma(new_valores)
    print(new_valores) #observar la escala de gris transformada con la cantidad de píxeles

    #Paso 5 Imagen obtenida
    imagen_expandida = reconstruir_imagen(gris, valores)
    cv2.imshow("Imagen original", gris)
    cv2.imshow("Imagen expandida", imagen_expandida)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #guardar la imagen
    #cv2.imwrite("pina_expandida.jpg", imagen_expandida)

#principal
Main()
