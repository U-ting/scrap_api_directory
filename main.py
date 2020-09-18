import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.programmableweb.com/category/all/apis'
data_api = {}
api_no = 0
while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')
    # DAPATKAN SEMUA TAG TR
    rows = soup.find_all('tr')
    for row in rows:
        links = row.find('td', {'class': 'views-field views-field-pw-version-title'})
        if links is None:
            continue
        title = links.text
        alamat = 'https://www.programmableweb.com' + links.find('a').get('href')
        # mengambil data dari api
        api_detail = requests.get(alamat)
        detail_soup = BeautifulSoup(api_detail.text, features='html.parser')
        description_tag = detail_soup.find('div', {'class': 'api_description tabs-header_description'})
        description = description_tag.text if description_tag else "N/A"
        category = row.find('td', {'views-field views-field-field-article-primary-category'}).text
        follower = row.find('td', {'views-field views-field-flag-follow-api-count'}).text
        api_no += 1
        print(api_no)
        data_api[api_no] = [title,alamat,description,category,follower]

        # membuat next page
    nextPage = soup.find('a',{'title':'Go to next page'})
    if nextPage != None:
        url = 'https://www.programmableweb.com'+nextPage.get('href')
        print(url)
    else:
        break
export = pd.DataFrame.from_dict(data_api, orient='index',columns=['Api Nama','Link','Deskripsi','Kategori','Follower'])
export.to_csv('data_api.csv')
print(f'total api : {api_no}')