import requests
from bs4 import BeautifulSoup
import time
import csv

base_url = "https://local.demandforce.com/b/caringcrittersanimalhospital/reviews.page?header=true&page={}"
headers = {"User-Agent": "Mozilla/5.0"}

all_reviews = []
for page in range(150):
    r = requests.get(base_url.format(page), headers=headers)
    if r.status_code != 200: break
    soup = BeautifulSoup(r.text, 'html.parser')
    reviews = soup.find_all('div', class_='business-profile-review')
    if not reviews: break
    for rev in reviews:
        name = rev.find('cite', itemprop='name').text.strip() if rev.find('cite') else 'N/A'
        rating = rev.find('span', itemprop='ratingValue').text.strip() if rev.find('span', itemprop='ratingValue') else '5'
        body_tag = rev.find('blockquote')
        body = '\n\n'.join(p.text.strip() for p in body_tag.find_all('p')) if body_tag else ''
        date = rev.find('a', itemprop='datePublished').get('content', '') if rev.find('a', itemprop='datePublished') else ''
        all_reviews.append([name, rating, date, body])
    time.sleep(1)

with open('reviews.csv', 'w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows([['Name', 'Rating', 'Date', 'Review']] + all_reviews)

print(len(all_reviews), 'reviews saved to reviews.csv')
