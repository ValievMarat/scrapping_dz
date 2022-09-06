import requests
import bs4

def scrapping_habr(url, page, keywords_list):
   HEADERS = {
      'user-agent': "Mozilla / 5.0 NT 10.0; Win64; x64) AppleWebKit / "
                    "537.36 (KHTML, like Gecko) Chrome / 104.0.0.0 Safari / 537.36"
   }
   result_list = []
   response = requests.get(url+page, headers=HEADERS)
   text = response.text
   soap = bs4.BeautifulSoup(text, features='html.parser')

   articles = soap.find_all('article')
   for article in articles:
      caption = article.find('h2').find('span').text
      href = article.find(class_='tm-article-snippet__title-link').attrs['href']
      date_publication = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['datetime']

      hubs_obj = article.find_all(class_='tm-article-snippet__hubs-item')
      hubs = [hub.text.strip() for hub in hubs_obj]

      text_obj = article.find(class_='article-formatted-body article-formatted-body '
                                     'article-formatted-body_version-1')
      if text_obj is None:
         text_obj = article.find(class_='article-formatted-body article-formatted-body '
                                        'article-formatted-body_version-2')

      text_preview = text_obj.text
      # поиск будет осуществляться и по заголовку, и по хабам, и по тексту,
      # закидываем их в один список
      hubs.append(caption)
      hubs.append(text_preview)

      # дополнительно: поиск в самой статье
      response = requests.get(url + href, headers=HEADERS)
      text = response.text
      soap = bs4.BeautifulSoup(text, features='html.parser')
      text_obj = soap.find(class_='article-formatted-body article-formatted-body '
                                     'article-formatted-body_version-1')
      if text_obj is None:
         text_obj = soap.find(class_='article-formatted-body article-formatted-body '
                                        'article-formatted-body_version-2')

      text_public = text_obj.text
      # также закидываем его в список поиска
      hubs.append(text_public)


      check_public = False
      for keyword in keywords_list:
         for text in hubs:
            if keyword.lower() in text.lower():
               check_public = True
               break

      if check_public:
         result_list.append({'date': date_publication,
                             'caption': caption,
                             'link': url + href})

   return result_list

if __name__ == '__main__':
   keywords_list = ['C#', 'проект']
   url = 'https://habr.com'
   page = '/ru/all'
   result_list = scrapping_habr(url, page, keywords_list)
   for article_dict in result_list:
      print(f"{article_dict['date']} - {article_dict['caption']} - {article_dict['link']}")



