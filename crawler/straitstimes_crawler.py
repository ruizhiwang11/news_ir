from textwrap import indent
import requests
import os
import json
from bs4 import BeautifulSoup as soup
import re
import asyncio
import aiohttp
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from string import punctuation
from autocorrect import Speller as spell
from nltk import word_tokenize, pos_tag
from lxml import etree

class Preprocessor:
    def __int__(self):

        self.snowball_stemmer = SnowballStemmer('english')
        self.wordnet_lemmatizer = WordNetLemmatizer()

    def autospell(self,text):
        """
        correct the spelling of the word.
        """
        spells = [spell(w) for w in (nltk.word_tokenize(text))]
        return " ".join(spells)

    def to_lower(self,text):
        """
        :param text:
        :return:
            Converted text to lower case as in, converting "Hello" to "hello" or "HELLO" to "hello".
        """
        return text.lower()

    def remove_numbers(self,text):
        """
        take string input and return a clean text without numbers.
        Use regex to discard the numbers.
        """
        output = ''.join(c for c in text if not c.isdigit())
        return output

    def remove_punct(self,text):
        """
        take string input and clean string without punctuations.
        use regex to remove the punctuations.
        """
        return ''.join(c for c in text if c not in punctuation)

    def remove_Tags(self,text):
        """
        take string input and clean string without tags.
        use regex to remove the html tags.
        """
        cleaned_text = re.sub("[^a-zA-Z0-9']+", ' ', text)
        return cleaned_text

    def sentence_tokenize(self,text):
        """
        take string input and return list of sentences.
        use nltk.sent_tokenize() to split the sentences.
        """
        sent_list = []
        for w in nltk.sent_tokenize(text):
            sent_list.append(w)
        return sent_list

    def word_tokenize(self,text):
        """
        :param text:
        :return: list of words
        """
        return [w for sent in nltk.sent_tokenize(text) for w in nltk.word_tokenize(sent)]

    def remove_stopwords(self,sentence):
        """
        removes all the stop words like "is,the,a, etc."
        """
        stop_words = stopwords.words('english')
        return ' '.join([w for w in nltk.word_tokenize(sentence) if not w in stop_words])

    def stem(self,text):
        """
        :param word_tokens:
        :return: list of words
        """
        stemmed_word = [self.snowball_stemmer.stem(word) for sent in nltk.sent_tokenize(text)for word in nltk.word_tokenize(sent)]
        return " ".join(stemmed_word)

    def get_wordnet_pos(self,tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    def lemmatize(self,sentence):
        tokens = word_tokenize(sentence)
        tagged_sent = pos_tag(tokens)
        lemmas_sent = []
        for tag in tagged_sent:
            wordnet_pos = self.get_wordnet_pos(tag[1]) or wordnet.NOUN
            lemmas_sent.append(self.wordnet_lemmatizer.lemmatize(tag[0], pos=wordnet_pos))
        return lemmas_sent

    def preprocess(self,text):
        lower_text = self.to_lower(text)
        clean_text = self.remove_Tags(lower_text)
        return clean_text


class InfoGetter:
    def __init__(self,page):
        self.page = page
        self.links = []
        self.data = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    async def get_href_link(self, url):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, timeout=3) as response:
                    print(response.status)
                    if response.status == 200:
                        result = await response.text()
                        return result
            except Exception as e:
                print(e.args)

    async def get_link_by_cat(self):
        singapore_list = ['jobs', 'housing', 'parenting-education', 'politics', 'health', 'transport', 'courts-crime',
                    'consumer', 'environment', 'community']
        asia_country_list = ['se-asia', 'east-asia', 'south-asia', 'australianz']
        world_country_list = ['united-states','europe','middle-east']
        life_cat_list = ['food', 'entertainment', 'style', 'travel', 'arts', 'motoring', 'home-design']
        business_cat_list=['economy', 'invest', 'banking', 'companies-markets','property']
        tech_cat_list = ['tech-news', 'e-sports', 'reviews']
        sport_cat_list = ['football', 'schools', 'formula-one','combat-sports','basketball','tennis','golf']

        web_dic = {}
        web_dic['singapore'] = singapore_list
        web_dic['asia'] = asia_country_list
        web_dic['world'] = world_country_list
        web_dic['life'] = life_cat_list
        web_dic['business'] = business_cat_list
        web_dic['tech'] = tech_cat_list
        web_dic['sport'] = sport_cat_list
        web_dic['opinion']=''
        web_dic['st-podcasts'] = ''
        web_dic['multimedia'] = ''

        for web_link in web_dic.keys():
            for i in range(0,self.page):
                try:
                    web_baisc_link = 'https://www.straitstimes.com/' + web_link
                    html_text = await self.get_href_link(web_baisc_link)
                    html = etree.HTML(html_text)
                    href = html.xpath("//div[@class='view-footer']/a/@href")
                    for item in href:
                        try:
                            if (item.startswith('https')):
                                baselink = item
                                req = requests.get(baselink, headers=self.headers)
                                req.raise_for_status()
                                page_soup = soup(req.text, 'html.parser')
                                reqs = page_soup.findAll("a", {"class": "stretched-link"})
                                #print(reqs)
                                for re in reqs:
                                    self.links.append("https://www.straitstimes.com" + re["href"])
                                    #print(self.links)
                            else:
                                baselink = 'https://www.straitstimes.com' + item + '?page=' + str(i)
                                req = requests.get(baselink, headers=self.headers)
                                req.raise_for_status()
                                page_soup = soup(req.text, 'html.parser')
                                reqs = page_soup.findAll("a", {"class": "stretched-link"})
                                for re in reqs:
                                    self.links.append("https://www.straitstimes.com" + re["href"])
                        except:
                            pass

                    for item in web_dic[web_link]:
                        if item == 'food' or item == 'travel':
                            link = 'https://www.straitstimes.com/' + web_link + '/' + item
                            html_text = await self.get_href_link(link)
                            html = etree.HTML(html_text)
                            href = html.xpath("//div[@class='view-footer']/a/@href")
                            for item in href:
                                try:
                                    baselink = 'https://www.straitstimes.com' + item +'?page=' + str(i)
                                    req = requests.get(baselink,headers=self.headers)
                                    req.raise_for_status()
                                    page_soup = soup(req.text, 'html.parser')
                                    reqs = page_soup.findAll("a", {"class": "stretched-link"})
                                    for re in reqs:
                                        self.links.append("https://www.straitstimes.com" + re["href"])
                                except:
                                    pass
                        else:
                            req = requests.get('https://www.straitstimes.com/' + web_link + '/' +item+'?page='+str(i),headers=self.headers)
                            # print('https://www.straitstimes.com/' + web_link + '/' +item+'?page='+str(i))
                            req.raise_for_status()
                            page_soup = soup(req.text, 'html.parser')
                            # print('success for', 'https://www.straitstimes.com/' + web_link + '/' +item+'?page='+str(i))
                            reqs = page_soup.findAll("a", {"class": "stretched-link"})
                            for re in reqs:
                                self.links.append("https://www.straitstimes.com" + re["href"])
                except requests.HTTPError as err:
                    print('[!!] Something went wrong!' + err)
                    #pass

    async def parse_data(self):
        clean = Preprocessor()
        '''
        with open('mylink_file.txt') as file:
            lines = [line.rstrip() for line in file]
        self.links = lines
        '''
        for id, link in enumerate(self.links):
            html_text = await self.get_href_link(link)
            if html_text:
                page_soup = soup(html_text, 'html.parser')
                try:
                    base_info = str(page_soup.find_all('script')[6].contents[0]).split('\n')
                   # print("base_info  ",page_soup.find_all('script')[6].contents[0])

                    title = base_info[22]
                    title = title[title.find(':') + 2:-1].replace("_", " ")[1:-1].strip('"')

                    author = base_info[9]
                    author = author[author.find(':') + 2:-1][1:-1].strip('"')

                    create_time = base_info[20]
                    create_time = create_time[create_time.find(':') + 2:-1][1:-1].strip('"')

                    image_link = page_soup.find("img", {"class": "image-style-large30x20"})
                    image_link = image_link["src"]

                    content=soup(str(page_soup.findAll('p')), "lxml").text[1:-1]

                    category_A = base_info[4]
                    category_A = category_A[category_A.find(':') + 2:-1].strip('"')
                    category_B = base_info[5]
                    category_B = category_B[category_B.find(':') + 2:-1].strip('"')
                    category = category_A + ' ' + category_B

                    if (str(category_A) == 'Singapore'):
                            location = base_info[4]
                            location = location[location.find(':') + 2:-1]
                    elif(str(category_A) == 'Asia' or str(category_A) == 'World'):
                            location = base_info[5]
                            location = location[location.find(':') + 2:-1]
                    else:
                        location=''

                    dic_data = {
                            "category": clean.preprocess(str(category)),
                            "location": clean.preprocess(str(location)),
                            "title": clean.preprocess(str(title)),
                            "author": clean.preprocess(str(author)),
                            "create_time": str(create_time),
                            "content": clean.preprocess(str(content)),
                            "image": str(image_link)
                    }
                    self.data.append(dic_data)
                except:
                    pass
                    #print("An exception occurred")
                    #print(content)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_link_by_cat())
        loop.run_until_complete(self.parse_data())

    def generate_json(self):
        self.start()
        with open(os.path.join('total_'+str(self.page) + '_page(s).json'), "w") as f:
           f.write(json.dumps(self.data,indent=4) )

if __name__ == '__main__':
        getter = InfoGetter(10)
        getter.generate_json()

