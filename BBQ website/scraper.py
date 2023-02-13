import requests
from bs4 import BeautifulSoup
import pandas as pd

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}
keywd = 'lamb'
url = f'https://www.allrecipes.com/search?q={keywd}'

def getdata(url):
    r = requests.get(url, headers=header).text
    soup = BeautifulSoup(r, 'html.parser')
    return soup

def get_next_page(soup):
        page = soup.find('li', {'class': "pagination__next"})
        if page.find('a', {"class": 'type--squirrel-link'}):
            url = page.find('a', {"class": 'type--squirrel-link'})["href"]
            return url
        else:
            return

def get_all_product_links(soup, tag, attributes, string_to_clean):
    all_product_rough = soup.find(tag, attributes).contents
    all_product=[]
    for product in all_product_rough:
        if product not in string_to_clean:
            all_product.append(product)

    all_product_links = []
    asd = all_product[0].find('span', class_='recipe-card-meta__rating-count-text')
    for product in all_product:
        try:
            all_product_links.append(product['href'])
        except:
            pass
    return all_product_links

review = None
prep_time = None
cook_time = None
total_time = None
servings = None
yield_ = None
ingredients = None
directions = None




num=1
data = []

while True:
    #Making soup
    soup = getdata(url=url)
    soup.find_all('a', class_='comp')

    # Get all url from current page
    string_to_clean = ['\n', ' end: comp mntl-sc-list-item list-sc-item mntl-block ',
                       ' end: comp mntl-card-list-items mntl-document-card mntl-card card card--no-image ',
                       ' end: comp article-feedback mntl-article-feedback ']
    all_urls = get_all_product_links(soup=soup, tag='div', attributes={"id": 'card-list_1-0'},string_to_clean=string_to_clean)

    # Scrape data from all urls
    for product_url in all_urls:
        new_soup = getdata(url=product_url)
    # new_soup = getdata(url=all_urls[0])


        recipie_name = new_soup.find('h1').text
        try:
            ingredients = new_soup.find('ul', class_='mntl-structured-ingredients__list').text
            all_details = new_soup.find_all('div', 'mntl-recipe-details__value')
            all_details_label = new_soup.find_all('div', 'mntl-recipe-details__label')
            for i in range(len(all_details)):
                if 'Prep Time:' in all_details_label[i].text:
                    try:
                        prep_time = all_details[i].text
                    except IndexError:
                        prep_time = None
                if 'Cook Time:' in all_details_label[i].text:
                    try:
                        cook_time = all_details[i].text
                    except IndexError:
                        cook_time = None
                if 'Total Time:' in all_details_label[i].text:
                    try:
                        total_time = all_details[i].text
                    except IndexError:
                        total_time = None
                if 'Servings:' in all_details_label[i].text:
                    try:
                        servings = all_details[i].text
                    except IndexError:
                        servings = None
                if 'Yield:' in all_details_label[i].text:
                    try:
                        yield_ = all_details[i].text.replace('servings', '')
                    except IndexError:
                        yield_ = None

                if 'Additional Time:' in all_details_label[i].text:
                    try:
                        additional_time = all_details[i].text
                    except IndexError:
                        additional_time = None
                try:
                    print(additional_time)
                except NameError:
                    additional_time=None

            try:
                review = new_soup.find('div', {'id': 'mntl-recipe-review-bar__comment-count_1-0'}).text.replace(
                    'Reviews', '').strip()
            except AttributeError:
                review = None
            try:
                directions = new_soup.find('ol', {'id': 'mntl-sc-block_2-0'}).text
            except AttributeError:
                directions = None
            dict_data = {
                'Recipe Name': recipie_name,
                'Reviews': review,
                'Prep Time': prep_time,
                'Cook Time': cook_time,
                'TotalTime': total_time,
                'Additional Time': additional_time,
                'Servings': servings,
                'Yield': yield_,
                'Ingredients': ingredients,
                'Directions': directions
            }
            data.append(dict_data)
            print("Passed")

        except AttributeError:
            print('[+]Cant find the desired elements. Getting all product links and scrape[+]')
            # Get all url from child page
            all_product_rough = new_soup.select('.list-sc-item')

            new_urls = []
            for product in all_product_rough:
                new_urls.append(product.find('a')['href'])
            for urli in new_urls:
                print(urli)
                soup_baby = getdata(url=urli)
            #     Scrape and append
                recipie_name = soup_baby.find('h1').text
                try:
                    ingredients = soup_baby.find('ul', class_='mntl-structured-ingredients__list').text

                except AttributeError:
                    review = None
                all_details = soup_baby.find_all('div', 'mntl-recipe-details__value')
                all_details_label = soup_baby.find_all('div', 'mntl-recipe-details__label')
                for i in range(len(all_details)):
                    if 'Prep Time:' in all_details_label[i].text:
                        try:
                            prep_time = all_details[i].text
                        except IndexError:
                            prep_time = None
                    if 'Cook Time:' in all_details_label[i].text:
                        try:
                            cook_time = all_details[i].text
                        except IndexError:
                            cook_time = None
                    if 'Total Time:' in all_details_label[i].text:
                        try:
                            total_time = all_details[i].text
                        except IndexError:
                            total_time = None
                    if 'Servings:' in all_details_label[i].text:
                        try:
                            servings = all_details[i].text
                        except IndexError:
                            servings = None
                    if 'Yield:' in all_details_label[i].text:
                        try:
                            yield_ = all_details[i].text.replace('servings', '')
                        except IndexError:
                            yield_ = None
                    if 'Yield:' in all_details_label[i].text:
                        try:
                            yield_ = all_details[i].text.replace('servings', '')
                        except IndexError:
                            yield_ = None
                    if 'Additional Time:' in all_details_label[i].text:
                        try:
                            additional_time = all_details[i].text
                        except IndexError:
                            additional_time = None
                try:
                    print(additional_time)
                except NameError:
                    additional_time = None



                try:
                    review = soup_baby.find('div', {'id': 'mntl-recipe-review-bar__comment-count_1-0'}).text.replace(
                        'Reviews', '').strip()
                except AttributeError:
                    review = None
                try:
                    directions = soup_baby.find('ol', {'id': 'mntl-sc-block_2-0'}).text
                except AttributeError:
                    pass
                    directions = None
                dict_data = {
                    'Recipe Name': recipie_name,
                    'Reviews': review,
                    'Prep Time': prep_time,
                    'Cook Time': cook_time,
                    'TotalTime': total_time,
                    'Additional Time': additional_time,
                    'Servings': servings,
                    'Yield': yield_,
                    'Ingredients': ingredients,
                    'Directions': directions
                }
                data.append(dict_data)



    # Get Next Page

    try:
        url = get_next_page(soup)
    except AttributeError:
        break
    print(f"Page {num}")
    num+=1

new_df = pd.DataFrame(data)
print(new_df)
new_df.to_csv('firstdishes.csv', index=False)
new_df.to_excel('firstdishes.xlsx')
new_df.to_json('firstdishes.json')

