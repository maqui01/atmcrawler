import requests
from bs4 import BeautifulSoup
import csv

class ATM:

    def __init__(self, name, address, bank, network):
        self.name = name
        self.address = address
        self.bank = bank
        self.network = network

def main():
    page_count = 1
    response = requests.get('https://www.icajero.com.ar/?pg={}'.format(page_count))
    results = list()
    while response.status_code == 200:
        html = BeautifulSoup(response.text, 'html.parser')
        listing = html.find(id='listing')
        if len(listing.contents) == 1 and listing.contents[0].has_attr('class') and listing.contents[0]['class'][0] == 'empty':
            break
        for div in listing.contents:
            if div.has_attr('class') and div['class'][0] == 'item':
                name = div.h2.a.text.rstrip().lstrip()
                address = div.ul.contents[0].text.rstrip().lstrip()
                bank = div.ul.contents[1].text.rstrip().lstrip()
                network = div.ul.contents[2].text.rstrip().lstrip()
                atm = ATM(name, address, bank, network)
                results.append(atm)
        page_count += 1
        response = requests.get('https://www.icajero.com.ar/?pg={}'.format(page_count))
        print('page: ' + str(page_count) + ' processed')

    with open('banks.csv', mode='w') as bank_file:
        bank_writer = csv.writer(bank_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        bank_writer.writerow(["Nombre", "Dirección", "Banco", "Red"])
        for atm in results:
            bank_writer.writerow([atm.name, atm.address, atm.bank, atm.network])

if __name__ == "__main__":
    main()