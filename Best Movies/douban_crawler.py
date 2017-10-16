from bs4 import BeautifulSoup
from itertools import product, chain
import pandas as pd
import expanddouban

def get_movie_url(category, location):
    base_url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,'
    return f'{base_url}{category},{location}'

def parse_movie(category, location, item):
    name = item.find('span', class_='title').string
    rate = item.find('span', class_='rate').string

    info_link = item['href']
    cover_link = item.find('img')['src']

    return Movie(name, rate, location, category, info_link, cover_link)

def get_movies(category, location):
    url = get_movie_url(category, location)
    html = expanddouban.getHtml(url)

    soup = BeautifulSoup(html, 'lxml')
    movies_list = soup.find('div', class_='list-wp')
    movies_items = movies_list.find_all('a', class_='item')

    yield from (parse_movie(category, location, item) 
                for item in movies_items)

def get_categories_locations():
    url = get_movie_url('剧情', '美国')
    html = expanddouban.getHtml(url)

    soup = BeautifulSoup(html, 'lxml')
    uls = soup.find_all('ul', class_='category')

    categories_ul = uls[1]
    categories_lis = categories_ul.find_all('li')
    categories = [li.string for li in categories_lis]

    locations_ul = uls[2]
    locations_lis = locations_ul.find_all('li')
    locations = [li.string for li in locations_lis]
    
    # skip '全部类型' and '全部地区'
    return categories[1:], locations[1:]

class Movie:
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link
        
if __name__ == '__main__':
    categories, locations = get_categories_locations()

    movie_lists = (get_movies(category, location)
                  for category, location in product(categories, locations))

    movies = chain.from_iterable(movie_lists)

    movies_df = pd.DataFrame([m.__dict__ for m in movies])
    movies_df = movies_df[['name', 'rate', 'location', 'category', 'info_link', 'cover_link']]

    movies_df.to_csv('movies.csv', header=0, index=0)
    count = movies_df.groupby(['category', 'location'])['name'].count()

    with open('output.txt', 'w') as f:
        
        for category in count.index.levels[0]:        
            f.write(f'{category}: ')

            top3 = count.loc[category].sort_values(ascending=False)[:3]
            subtotal = count.loc[category].sum()
            percentages = top3 / subtotal

            for location, percentage in percentages.iteritems():
                f.write(f'{location}({percentage:.2%}) ')
            
            f.write('\n')

    