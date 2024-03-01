from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome()
BASE_URL = "https://www.seminovosmovida.com.br/busca"

CATEGORIAS_PATHS = {
    "Hatch": "categorias-hatch",
    "SUV": "categorias-suv",
    "Sedan": "categorias-seda",
    "Picape": "categorias-picape",
    "Utilitário": "categorias-utilitario"
}

def buscar_e_extrair_veiculos(driver, categoria, caminho):
    driver.get(f"{BASE_URL}/{caminho}")
    driver.implicitly_wait(10) 
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card__inner')))
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # adicionar 2 veiculos aleatorios poor categoria
    veiculos = []
    elementos_veiculos = soup.select('.card__inner')[:2] 
    
    for elemento in elementos_veiculos:
        nome = elemento.select_one('.info__title').get_text(strip=True)
        detalhes = elemento.select_one('.add__info').get_text(strip=True)
        preco = elemento.select_one('.price').get_text(strip=True).replace('R$', '').strip()

        detalhes_split = detalhes.split('•')
        modelo_ano = detalhes_split[0].strip() if len(detalhes_split) > 0 else 'N/A'
        quilometragem = detalhes_split[1].strip() if len(detalhes_split) > 1 else 'N/A'

        veiculo = {
            'categoria': categoria,
            'nome': nome,
            'modelo_ano': modelo_ano,
            'valor': preco,
            'quilometragem': quilometragem
        }
        veiculos.append(veiculo)

    return veiculos


todos_veiculos = []
for categoria, caminho in CATEGORIAS_PATHS.items():
    veiculos = buscar_e_extrair_veiculos(driver, categoria, caminho)
    todos_veiculos.extend(veiculos)


driver.quit()

# transformar em dataframe 
df_veiculos = pd.DataFrame(todos_veiculos)

caminho_arquivo_excel = 'Relatorio_Veiculos.xlsx'


df_veiculos.to_excel(caminho_arquivo_excel, index=False, sheet_name='Veiculos')

print('finalizado com sucesso!!!')