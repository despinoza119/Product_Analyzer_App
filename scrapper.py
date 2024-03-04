import time
from tools import scraping

tiempoInicio = time.time()

make_headless = True

scraping(make_headless)

tiempoTotal = round(time.time() - tiempoInicio, 2)
tiempoSegundos =round(tiempoTotal)
tiempoMinutos = round(tiempoTotal / 60)

print(f"Tiempo requerido: {tiempoTotal} segundos ({tiempoSegundos} segundos) ({tiempoMinutos} minutos)")

