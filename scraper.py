import string, os, requests
from bs4 import BeautifulSoup

class NatureArticles:


    def __init__(self, pages, article_type):
        self.url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
        self.file_list = []

        self.pages = pages
        self.article_type = article_type


    def make_folders(self):
        for i in range(self.pages):
            os.mkdir(f'Page_{i + 1}')


    def article_search(self):
        for x in range(1, self.pages + 1):
            self.link_list = []
            page = requests.get(f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={x}')
            soup = BeautifulSoup(page.content, 'lxml')
            articles = soup.find_all('article')
            #   find all articles of input type and pull href value (local address link) from them
            #   then concatenate href value with root website address appended to self.link_list
            for i in articles:
                article_type = i.find('span', {'data-test': 'article.type'})
                if article_type.text.strip("\n") == f"{self.article_type}":
                    href = i.find('a', {'data-track-action': 'view article'}).get('href')
                    self.link_list.append(self.url[0:22] + href)
            self.make_files(x)


    def make_files(self, n):
        os.chdir(f'Page_{n}')
        for i in self.link_list:
            l1 = requests.get(i)
            soup = BeautifulSoup(l1.content, 'lxml')
            file_name = soup.find('title').text.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')
            file = open(f"{file_name}.txt", 'wb')
            body = soup.find('div', {'class': 'c-article-body main-content'}).text.strip()
            file.write(body.encode())
            self.file_list.append(file)
            file.close()
        os.chdir(f'..')



    def display_result(self):
        print(f"Saved articles: {[x.name for x in self.file_list]}")
        print('Saved all articles')


if __name__ == '__main__':
    w1 = NatureArticles(int(input()), input())
    w1.make_folders()
    w1.article_search()
    w1.display_result()
