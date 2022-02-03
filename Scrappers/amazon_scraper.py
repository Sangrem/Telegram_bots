"""Статья по которой был собран данный скрепер.
https://habr.com/ru/company/vdsina/blog/537174/
"""

import requests
import json
from bs4 import BeautifulSoup as Soup
import time

headers = {
    'authority': 'www.amazon.com',
    'dnt': '1',
    'rtt': '250',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'accept': 'text/html,*/*',
    'x-requested-with': 'XMLHttpRequest',
    'downlink': '6.45',
    'ect': '4g',
    'origin': 'https://www.amazon.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/product-reviews/0132350882/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1',
}

post_data = {
  'sortBy': 'recent',
  'reviewerType': 'all_reviews',
  'formatType': '',
  'mediaType': '',
  'filterByStar': '',
  'pageNumber': '1',
  'filterByLanguage': '',
  'filterByKeyword': '',
  'shouldAppend': 'undefined',
  'deviceType': 'desktop',
  'canShowIntHeader': 'undefined',
  'reftag': 'cm_cr_getr_d_paging_btm_next_2',
  'pageSize': '10',
  'asin': '0132350882',
  'scope': 'reviewsAjax1'
}

response = requests.post('https://www.amazon.com/hz/reviews-render/ajax/reviews/get/ref=cm_cr_arp_d_paging_btm_next_2',
    headers=headers, data=post_data)

page = 1
reviews = []
while True:
  post_data['pageNumber'] = page
  response = requests.post('https://www.amazon.com/hz/reviews-render/ajax/reviews/get/ref=cm_cr_arp_d_paging_btm_next_2',
    headers=headers, data=post_data)
  data = response.content.decode('utf-8')
  for line in data.splitlines():
    try:
      payload = json.loads(line)
      html = Soup(payload[2], features="lxml")
      # Stop scraping once we reach the last page
      if html.select_one('.a-disabled.a-last'):
        break
      review = html.select_one('.a-section.review')
      if not review:
        # Skip unrelated sections
        continue
      reviews.append({
        'stars': float(review.select_one('.review-rating').text.split(' out of ')[0]),
        'text': review.select_one('.review-text.review-text-content').text.replace("\n\n", "").strip(),
        'date': review.select_one('.review-date').text.split(' on ')[1],
        'profile_name': review.select_one('.a-profile-name').text
      })
    except Exception as e:
      pass
  print(str(len(reviews)) + ' reviews have been fetched so far on page ' + str(page))
  page += 1
  time.sleep(2)

