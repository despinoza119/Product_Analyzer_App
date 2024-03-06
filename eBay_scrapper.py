import re
import sys
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from tools import tiempoAlea
from tools import agenteUsuario

def scrapper(head, produbuscar, nombre_archivo):
    datos_eBay = []
    catchClause = []

    produinuser = produbuscar.replace(" ", "+")
    ingresoProducto = f"https://www.ebay.es/sch/i.html?_nkw={produinuser}"

    eBay_link_pattern = re.search("^https://www.ebay.es/sch/i.html\?.+", ingresoProducto)

    if eBay_link_pattern == None:
        print("El link de eBay no es válido")
        sys.exit()

    print(ingresoProducto)

    with sync_playwright() as play:
        # Launch browser
        navegador = play.chromium.launch(headless=head, slow_mo=3*1000) # Slow_Mo reduces actioning by milliseconds.
        # Create new page in browser
        pagina = navegador.new_page(user_agent=agenteUsuario())
        # Navigate to specified URL
        pagina.goto(ingresoProducto)

        pagina.wait_for_timeout(timeout=tiempoAlea(4)*1000) # Specifying a random time for next execution.
        nombreProducto = "/html/body/div[4]/div[4]/div[2]/div[1]/div[2]/ul/li[2]/div/div[1]/div/a/div/img/@alt"

        totalPaginasUno = "/html/body/div[4]/div[4]/div[2]/div[1]/div[2]/ul/li[62]/div[2]/span/span/nav/ol/li[9]/a"
        totalPaginasDos = "/html/body/div[4]/div[4]/div[2]/div[1]/div[2]/ul/li[62]/div[2]/span/span/nav/ol/li[2]/a"
        siguienteBoton = "/html/body/div[4]/div[4]/div[2]/div[1]/div[2]/ul/li[62]/div[2]/span/span/nav/a"

        contenidorPrincipal = '//*[@id="srp-river-results"]'

        enlace = "/html/body/div[4]/div[4]/div[2]/div[1]/div[2]/ul/li[2]/div/div[2]/a"
        precio = "/html/body/div[4]/div[4]/div[2]/div[1]/div[2]/ul/li[2]/div/div[2]/div[2]/div[1]/span[@class='s-item__price']"
        #precioAnterior = ""
        califica = "/html/body/div[4]/div[4]/div[2]/div[1]/div[2]/ul/li[2]/div/div[2]/div[2]/span[1]/span/span"
        #numCalifica = ""
        imagen = "/html/body/div[4]/div[4]/div[2]/div[1]/div[2]/ul/li[2]/div/div[1]/div/a/div/img"

        print(nombreProducto)

        try:
            pagina.wait_for_selector(contenidorPrincipal, timeout=10 * 1000)
        except PlaywrightTimeoutError:
            print(f"Error al cargar el contenido. Vuelva a intentar en unos minutos")

        try:
            ultimaPagina = pagina.query_selector(
                totalPaginasUno).inner_text().strip()
        except:
            #ultimaPagina = pagina.query_selector(
                #totalPaginasDos)[-2].get_attribute('aria-label').split()[-1]
            ultimaPagina=1

        print(f"El numero de paginas es: {ultimaPagina}")
        print(f"Realizando scraping a: {produbuscar}")

        for click in range(1, 2):
            print(f"pagina de scraping numero: {click}")
            pagina.wait_for_timeout(timeout=tiempoAlea(8) * 1000)
            for content in pagina.query_selector_all(contenidorPrincipal):
                datos = {
                    "Producto": catchClause.text(content.query_selector('.//*[@class="s-item__title"]//text()')),
                    "ASIN": catchClause.attributes(content, 'data-asin'),
                    "Precio": catchClause.text(content.query_selector(precio)),
                    #"Precio Original": catchClause.text(content.query_selector(precioAnterior)),
                    "Calificacion": catchClause.text(content.query_selector(califica)),
                    #"Numero de Calificaciones": re.sub(r"[()]", "",
                                                       #catchClause.text(content.query_selector(numCalifica))),
                    "Enlace Producto": f"""https://www.amazon.com{catchClause.attributes(content.query_selector(enlace), 'href')}""",
                    "Imagen": F"""{catchClause.attributes(content.query_selector(imagen), 'src')}"""
                }
                datos_eBay.append(datos)

                try:
                    pagina.query_selector(siguienteBoton).click()
                except AttributeError:
                    print(f"Hay problemas con las eccion {pagina.url} numero: {click}")
                    break
        navegador.close()
    print(f"Scraping realizado con exito")

    df = pd.DataFrame(datos_eBay)
    df.to_excel(f"output/{nombre_archivo}.xlsx", index=False)
    print(f"{produbuscar}.xlsx creado con exito")





