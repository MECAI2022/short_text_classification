import bs4
import requests
import pandas as pd
import re
import warnings

warnings.filterwarnings('ignore')


def get_page(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/106.0.0.0 Safari/537.36"}

    r = requests.get(url, headers)

    try:
        r.raise_for_status()
        page = bs4.BeautifulSoup(r.text, 'lxml')
        return page

    except Exception as e:
        return False


def pontofrio(search, n_page):
    '''df = pd.DataFrame(
        [],
        columns=[
            'nm_item',
            'nm_product',
        ],
    )'''

    df_web = pd.read_csv('web_scrapping_product.csv')

    for page in range(n_page):
        soup = get_page(f'https://search3.pontofrio.com.br/busca?q={search}&page={1 + page}')

        new_search = re.sub('-', ' ', search)
        for item in soup.select('.nm-product-name a'):
            df_web = df_web.append({'nm_item': item.getText().upper(), 'nm_product': new_search}, ignore_index=True)
            # print(item.getText().upper())
        df_web.to_csv('web_scrapping_product.csv', index=False)

    print(f'{search}: Ok')


df = pd.read_csv('product.csv')
nm_product = df['nm_product'].values.tolist()
for product in nm_product:
    new_product = re.sub(' ', '-', product)
    #print(new_product)
    pontofrio(new_product, 5)

# Erro: caderno, lapis, apontador, regua, borracha, estojo, tinta, lapiseira, pasta