import requests
from bs4 import BeautifulSoup, NavigableString
import urllib.parse
import csv

class Province:

    list = [
        "BUENOS AIRES",
        "CABA",
        "CATAMARCA",
        "CHACO",
        "CHUBUT",
        "CÓRDOBA",
        "CORRIENTES",
        "ENTRE RÍOS",
        "FORMOSA",
        "JUJUY",
        "LA PAMPA",
        "LA RIOJA",
        "MENDOZA",
        "MISIONES",
        "NEUQUÉN",
        "RÍO NEGRO",
        "SALTA",
        "SAN JUAN",
        "SAN LUIS",
        "SANTA CRUZ",
        "SANTA FE",
        "SANTIAGO DEL ESTERO",
        "TIERRA DE FUEGO",
        "TUCUMÁN"
    ]

class ATM:

    def __init__(self, bank, address, province, city, zipcode, lat, long):
        self.bank = bank
        self.address = address
        self.province = province
        self.city = city
        self.zipcode = zipcode
        self.lat = lat
        self.long = long

def main():
    results = list()
    for province in Province.list:
        response = requests.get('http://www.bcra.gov.ar/SistemasFinancierosYdePagos/Entidades_financieras_filiales_y_cajeros_filtros.asp?Provincia={}&bco=AAA00&Tit=1&Tipo=4'.format(urllib.parse.quote(province.encode('iso-8859-1'))))

        if response.status_code == 200:
            html = BeautifulSoup(response.text, 'html.parser')
            listing = html.find_all('table', class_='table-BCRA')
            for tr in listing[0].contents[3].contents:
                if type(tr) != NavigableString:
                    bank = tr.contents[1].text.rstrip().lstrip()
                    address = tr.contents[3].text.rstrip().lstrip()
                    city = tr.contents[5].text.rstrip().lstrip()
                    zipcode = tr.contents[7].text.rstrip().lstrip()
                    lat = float(tr.contents[17].text.rstrip().lstrip().replace(",","."))
                    long = float(tr.contents[19].text.rstrip().lstrip().replace(",","."))

                    atm = ATM(bank, address, province, city, zipcode, lat, long)
                    results.append(atm)
            print('page: ' + str(province) + ' processed')

    with open('banks_bcra.csv', mode='w') as bank_file:
        bank_writer = csv.writer(bank_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        bank_writer.writerow(["Banco", "Dirección", "Provincia", "Localidad", "Codigo Postal", "Latitud", "Longitud"])
        for atm in results:
            bank_writer.writerow([atm.bank, atm.address, atm.province, atm.city, atm.zipcode, atm.lat, atm.long])

if __name__ == "__main__":
    main()