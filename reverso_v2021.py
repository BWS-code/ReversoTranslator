import requests
from bs4 import BeautifulSoup
from http.client import responses


class Reverso_translator:
    def __init__(self, meta):
        self.url = 'https://context.reverso.net/translation/'
        self.to_lang = None
        self.word = None
        self.lang_dict = {
            'fr': 'english-french',
            'en': 'french-english'
        }
        self.trs_id = meta['translations_id']
        self.exs_tag = meta['examples_tag']
        self.exs_id = meta['examples_id']
        self.ex_tag = meta['example_tag']
        self.ex_cl = meta['example_class']

    def get_input(self):
        self.to_lang = input('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')
        self.word = input('Type the word you want to translate:')
        print('You chose "{}" as a language to translate "{}".'.format(self.to_lang, self.word))

    def get_link(self):
        self.url = self.url + self.lang_dict[self.to_lang] + f'/{self.word}'
        return self.url

    def get_soup(self):
        r = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        while not r.status_code == requests.codes.ok:
            r = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        else:
            print(r.status_code, responses[r.status_code])
        return BeautifulSoup(r.content, 'html.parser')

    def get_translations(self):
        soup = self.get_soup()
        translations_list = soup.find('div', id=self.trs_id).text.split()
        examples_list = [el.text.strip() for el in soup.find(self.exs_tag, id=self.exs_id).findAll(self.ex_tag, class_=self.ex_cl)]
        return 'Translations', translations_list, examples_list

    def main(self):
        self.get_input()
        self.get_link()
        for item in self.get_translations():
            print(item)

known_ids = {
    'translations_id': 'translations-content',
    'examples_tag': 'section',
    'examples_id': 'examples-content',
    'example_tag': 'span',
    'example_class': 'text'
}

my_translator = Reverso_translator(known_ids)
my_translator.main()
