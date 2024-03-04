import re
import sys
import random
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def tiempoAlea(val):
    ranges = [i for i in range(3,val+1)]
    return random.choice(ranges)

def agenteUsuario():
    with open('user-agents.txt') as f:
        agente = f.read().split("\n")
        return random.choice(agente)

class TryExcept:
    def text(self,element):
        try:
            return element.inner_text().strip()
        except:
            return "Sin Información"
    
    def attributes(self,element,attr):
        try:
            return element.get_attribute(attr)
        except AttributeError:
            return "Valor No Disponible"

def scraping(head):
    datosAmazon = []
    catchClause = TryExcept()

    produbuscar = str(input("Ingrese el producto a buscar: "))
    produinuser = produbuscar.replace(" ","+")
    ingresoProducto = f"https://www.amazon.com/s?k={produinuser}"

    amazon_link_pattern = re.search("^https://www.amazon.com/s\?.+", ingresoProducto)

    if amazon_link_pattern == None:
        print("El link de Amazon no es válido")
        sys.exit()

    with sync_playwright() as play:
        navegador = play.chromium.launch(headless=head, slow_mo=3*1000)
        pagina = navegador.new_page(user_agent=agenteUsuario())
        pagina.goto(ingresoProducto)

        pagina.wait_for_timeout(timeout=tiempoAlea(4)*1000)
        nombreProducto = "/html/body/div[1]/div[1]/div[1]/div[2]/div/div[3]/span/div/div/div/div[3]/ul/span/span[1]/li/span/a/span"
        
        totalPaginasUno = "//span[@class='s-pagination-item s-pagination-disabled']"
        totalPaginasDos = "//span[@class='s-pagination-strip']/a"
        siguienteBoton = "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']"

        contenidorPrincipal = "//div[@data-component-type='s-search-result']"

        enlace = "//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']"
        precio = "//span[@data-a-color='secondary']/span[@class='a-offscreen']"
        precioAnterior = "//span[@data-a-color='secondary']/span[@class='a-offscreen']"
        califica = "//span[@class='a-declarative']/a/i/span[@class='a-icon-alt']"
        numCalifica = "//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style']/span[@class='a-size-base s-underline-text']"
        imagen = "//img[@class='s-image']"

        print(nombreProducto)

        try:
            pagina.wait_for_selector(contenidorPrincipal,timeout=10*1000)
        except PlaywrightTimeoutError:
            print(f"Error al cargar el contenido. Vuelva a intentar en unos minutos")

        try:
            ultimaPagina = pagina.query_selector(
                totalPaginasUno).inner_text().strip()
        except:
            ultimaPagina = pagina.query_selector(
                totalPaginasDos)[-2].get_attribute('aria-label').split()[-1] 

        print(f"El numero de paginas es: {ultimaPagina}")
        print(f"Realizando scraping a: {produbuscar}")  

        for click in range(1,int(ultimaPagina)):
            print(f"pagina de scraping numero: {click}")
            pagina.wait_for_timeout(timeout=tiempoAlea(8)*1000)
            for content in pagina.query_selector_all(contenidorPrincipal):
                datos={
                    "Producto": catchClause.text(content.query_selector(enlace)),
                    "ASIN": catchClause.attributes(content,'data-asin'),
                    "Precio": catchClause.text(content.query_selector(precio)),
                    "Precio Original": catchClause.text(content.query_selector(precioAnterior)),
                    "Calificacion": catchClause.text(content.query_selector(califica)),
                    "Numero de Calificaciones": re.sub(r"[()]","",catchClause.text(content.query_selector(numCalifica))),
                    "Enlace Producto": f"""https://www.amazon.com{catchClause.attributes(content.query_selector(enlace),'href')}""",
                    "Imagen": F"""{catchClause.attributes(content.query_selector(imagen),'src')}"""
                }
                datosAmazon.append(datos)
                
                try:
                    pagina.query_selector(siguienteBoton).click()
                except AttributeError:
                    print(f"Hay problemas con las eccion {pagina.url} numero: {click}")
                    break
        navegador.close()
    print(f"Scraping realizado con exito")

    df = pd.DataFrame(datosAmazon)
    df.to_excel(f"{produbuscar}.xlsx",index=False)
    print(f"{produbuscar}.xlsx creado con exito")



