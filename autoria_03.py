import csv
import requests
from bs4 import BeautifulSoup, SoupStrainer

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

u = "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&year[0].gte=2018&categories.main.id=1&brand.id[0]=24&model.id[0]=2047&price.currency=1&abroad.not=0&custom.not=1&size=10&page="

CSV_HEADER = ["title", "year", "price", "mileage", "location", "fuel", "gearbox", "state_num", "vin", "descriptions",
              "add_date", "update_date"]


class Car:

    def __init__(self, title, year, price=None, mileage=None, location=None, fuel=None, gearbox=None, state_num=None,
                 vin=None, descriptions=None, add_date=None, update_date=None):
        self.title = title
        self.year = year
        self.price = price
        self.mileage = mileage
        self.location = location
        self.fuel = fuel
        self.gearbox = gearbox
        self.state_num = state_num
        self.vin = vin
        self.descriptions = descriptions
        self.add_date = add_date
        self.update_date = update_date

    def __str__(self):
        return self.title + ' ' + str(self.year)

car1 = Car('aaaaa', '2018')


class Cars:

    def __init__(self, *args):
        if args:
            self.items = list(args)
        else:
            self.items = list()

    def getCar(self, item_number):
        return self.items[item_number]

    def addCar(self, car):
        self.items.append(car)

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return f'Collect {str(len(self))} item{"" if len(self)==1 else "s"}'


m = Cars(car1)
print(m.getCar(0))

for item in m.items:
    print(item)


def get_content_block(url, start_page=0, stop_page=100000):
    # page_data = []
    page_data = Cars()

    page = start_page
    while page <= stop_page:
        print('Scrap page number', page)
        page_url = u + str(page)
        req = requests.get(page_url, headers=HEADERS)
        soup = BeautifulSoup(req.content, 'lxml', parse_only=SoupStrainer('div', attrs={'class': 'content-bar'}))
        # with open(f'f{page}.html', 'w', encoding='utf-8') as file:
        #     file.write(soup.prettify())
        all_content_block = soup.find_all('div', class_="content")
        if len(all_content_block) == 0:
            scrap_pages = page - start_page
            print(f'Scrap {scrap_pages} page{"s" if scrap_pages != 1 else ""}')
            return page_data

        for content_block in all_content_block:
            title = content_block.find('span', {'class': "blue bold"}).getText().strip()
            year = content_block.find('span', {'class': "blue bold"}).next.next.strip()
            price = content_block.find('div', {'class': "price-ticket"}).get('data-main-price')
            all_characteristic = content_block.find_all('li')
            mileage = all_characteristic[0].getText().strip()
            location = all_characteristic[1].getText().strip()
            fuel = all_characteristic[2].getText().strip()
            gearbox = all_characteristic[3].getText().strip()
            state_num = content_block.find('span', {'class': 'state-num'}).next.strip() if content_block.find('span', {
                'class': 'state-num'}) != None else ''
            vin = content_block.find('span', {'class': 'label-vin'}).findChild(
                'span').getText().strip() if content_block.find(
                'span', {'class': 'label-vin'}) != None else ''

            descriptions = ' '.join(
                content_block.find('p', {'class': 'descriptions-ticket'}).span.text.replace('\n', ' ').split())

            add_date = content_block.find('div', {'class': 'footer_ticket'}).span.get('data-add-date')
            update_date = content_block.find('div', {'class': 'footer_ticket'}).span.get('data-update-date')
            # print(title, price, mileage, location, fuel, gearbox, state_num, vin, descriptions, )
            car = Car(title, year, price, mileage, location, fuel, gearbox, state_num, vin, descriptions, add_date,
                      update_date)

            page_data.addCar(car)

            # page_data.append(
            #     (title, year, price, mileage, location, fuel, gearbox, state_num, vin, descriptions, add_date,
            #      update_date))
        page += 1
        scrap_pages = page - start_page + 1
    print(f'Scrap {scrap_pages} page{"s" if scrap_pages != 1 else ""}')
    return page_data


def write_csv(data, header=None, file_name='data.csv'):
    with open(file_name, mode='w', newline='', encoding='UTF-8') as csv_file:
        data_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if header != None:
            data_writer.writerow(header)
        # for item in data:
        #     data_writer.writerow(item)
        data_writer.writerows(data)


# data = get_content_block(u, start_page=26, stop_page=55)
# data = get_content_block(u, start_page=0)
data = get_content_block(u)
print(data, sep='\n')

print(data.getCar(1))
# write_csv(data, CSV_HEADER)
