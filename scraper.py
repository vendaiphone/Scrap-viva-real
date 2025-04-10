# scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time

def buscar_imoveis(cidade, estado, bairro, metragem, tipo):
    margem = 10
    min_m = metragem - margem
    max_m = metragem + margem
    max_resultados = 20
    max_paginas = 10

    tipo_url = {
        "casa": "casa",
        "apartamento": "apartamento",
        "terreno": "terreno-lote-condominio"
    }

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    valores = []
    metragems = []
    dados_csv = []

    for pagina in range(1, max_paginas + 1):
        url = (
            f"https://www.vivareal.com.br/venda/{tipo_url[tipo]}/"
            f"{estado.lower()}/{cidade.lower().replace(' ', '-')}/"
            f"{bairro.lower().replace(' ', '-')}/?pagina={pagina}"
        )
        driver.get(url)
        time.sleep(3)

        cards = driver.find_elements(By.CSS_SELECTOR, "article.property-card__container")

        for card in cards:
            try:
                valor_txt = card.find_element(By.CLASS_NAME, "property-card__price").text
                valor = int(valor_txt.replace("R$", "").replace(".", "").replace(",", "").strip())

                m2_txt = card.find_element(By.CLASS_NAME, "property-card__area").text
                m2 = int(''.join(filter(str.isdigit, m2_txt)))

                if min_m <= m2 <= max_m:
                    valores.append(valor)
                    metragems.append(m2)
                    dados_csv.append({"valor": valor, "metragem": m2, "pagina": pagina})

                    if len(valores) >= max_resultados:
                        break
            except Exception:
                continue

        if len(valores) >= max_resultados:
            break

    driver.quit()

    if not valores:
        raise Exception("Nenhum imóvel encontrado com os critérios.")

    with open("imoveis_filtrados.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["valor", "metragem", "pagina"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dados_csv)

    media_valor_total = sum(valores) / len(valores)
    media_valor_m2 = sum([v / m for v, m in zip(valores, metragems)]) / len(valores)

    return {
        "media_valor_total": round(media_valor_total),
        "media_valor_m2": round(media_valor_m2, 2),
        "quantidade_encontrada": len(valores)
    }
