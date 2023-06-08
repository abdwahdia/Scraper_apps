import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('BEST DATA SCRAPER')

st.markdown("""
This app performs simple webscraping of vehicles data from expat-dakar!
* **Python libraries:** base64, pandas, streamlit, requests, bs4
* **Data source:** [Vehicles-expat-dakar.com](https://www.expat-dakar.com/voitures/dakar?condition=used-abroad).
""")

st.sidebar.header('User Input Features')
selected_type_vehicle = st.sidebar.selectbox('Type of vehicle',list(['used-abroad', 'used']))
selected_page = st.sidebar.selectbox('Page', list(range(1,307)))
selected_mul_page = st.sidebar.selectbox('Multiple Pages', list([int(p) for p in np.linspace(5, 300, 60)]))


# Web scraping of Vehicles data on expat-dakar
@st.cache_data
def load_data(page, type_of_vehicle):
    Url = "https://www.expat-dakar.com/voitures/dakar?condition="+str(type_of_vehicle)+"&page="+str(page) 
    res = get(Url)
    soup = BeautifulSoup(res.text, 'html.parser')
    conteneurs = soup.find_all('div', class_ ='listings-cards__list-item')
    data = []
    for conteneur in conteneurs : 
      try :
        Gen = conteneur.find('div', class_ ='listing-card__header__tags').find_all('span')
        Ven_Occ = Gen[0].text
        Marque= Gen[1].text 
        Année = Gen[2].text
        Aut_Man = Gen[3].text
        Adresse = conteneur.find('div', class_ = 'listing-card__header__location').text.replace('\n', '')
        Prix = conteneur.find('span', class_ = 'listing-card__price__value 1').text.replace('\n', '').replace('\u202f', '').replace(' F Cfa', '')
    
        obj = {
           'Ven_Occ': Ven_Occ,
           'Marque': Marque, 
           'Année': int(Année), # convertir en Integer
           'Aut_Man': Aut_Man, 
           'Adresse': Adresse,
           'Prix': int(Prix) # convertir en Integer
        }
        data.append(obj)
      except:
        pass
    df = pd.DataFrame(data)
    return df

def load_data1(mul_page, type_of_vehicle):
    df = pd.DataFrame()
    for p in range(1, int(mul_page)):
        Url = f"https://www.expat-dakar.com/voitures/dakar?condition={type_of_vehicle}&page={p}" 
        res = get(Url)
        soup = BeautifulSoup(res.text, 'html.parser')
        conteneurs = soup.find_all('div', class_ ='listings-cards__list-item')
        data = []
        for conteneur in conteneurs : 
            try :
                Gen = conteneur.find('div', class_ ='listing-card__header__tags').find_all('span')
                Ven_Occ = Gen[0].text
                Marque= Gen[1].text 
                Année = Gen[2].text
                Aut_Man = Gen[3].text
                Adresse = conteneur.find('div', class_ = 'listing-card__header__location').text.replace('\n', '')
                Prix = conteneur.find('span', class_ = 'listing-card__price__value 1').text.replace('\n', '').replace('\u202f', '').replace(' F Cfa', '')
    
                obj = {
                    'Ven_Occ': Ven_Occ,
                    'Marque': Marque, 
                    'Année': int(Année), # convertir en Integer
                    'Aut_Man': Aut_Man, 
                    'Adresse': Adresse,
                    'Prix': int(Prix) # convertir en Integer
                }
                data.append(obj)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis = 0)
    df.reset_index(drop = True, inplace = True)
    return df

Vehicles_data = load_data(selected_page,selected_type_vehicle)
Vehicles_data_mul_pag = load_data1(selected_mul_page, selected_type_vehicle)



st.subheader('Display data dimension')
st.write('Data dimension: ' + str(Vehicles_data.shape[0]) + ' rows and ' + str(Vehicles_data.shape[1]) + ' columns.')
st.dataframe(Vehicles_data)

# Download Vehicles data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="Vehicles_data.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(Vehicles_data), unsafe_allow_html=True)

st.header('Collect over multiples pages')

st.subheader('Display data dimension')
st.write('Data dimension: ' + str(Vehicles_data_mul_pag.shape[0]) + ' rows and ' + str(Vehicles_data_mul_pag.shape[1]) + ' columns.')
st.dataframe(Vehicles_data_mul_pag)


st.markdown(filedownload(Vehicles_data_mul_pag), unsafe_allow_html=True)
