
# coding: utf-8

# In[18]:


import requests
from lxml import html
from lxml.etree import tostring
import time
import requests
from pprint import pprint
from bs4 import BeautifulSoup

#nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
#nltk.download('popular', halt_on_error=False)

import nltk
#textblob

from textblob import TextBlob, Word
import numpy as np #for numeric operations
import pandas as pd #for dealing with dataframes
import matplotlib.pyplot as plt #for visualization
import re
import time
from lxml.cssselect import CSSSelector
from lxml import html
import json
from selenium import webdriver
import time
import pandas as pd
from itertools import chain
from glob import glob
from collections import Iterable


# Create a utils.py file which will have the following classes/functions defined:
# #. 1.5 points Scrape_All class, which will scrape from a given page all:
# a. hyperlinks  and provide the absolute link if relative one is given in the page,
# b. headings and paragraphs and merge them inside one string with a new line between different headings/paragraphs, without distorting order).
# c. custom tags provided by the user i.e. if the user provides li.author or similar input then all the list items that have class author must be scraped.

# In[123]:


class Scrape_All:
    """This class helps get data using different methods B4 xpath and selenium"""
    def __init__(self,url):
        self.url=url
        self.response=requests.get(self.url)
        self.page=self.response.content
    def beaut(self):
        pageB=BeautifulSoup(self.page, "html.parser")
        self.pageB=pageB #beautiful page
        return pageB
    def s_lxml(self):
        tree = html.document_fromstring(self.page)
        self.tree=tree #xpath treee
        return tree
    def selen(self):
        browser = webdriver.Chrome()
        browser.get(self.url)
        time.sleep(3)
        elems = browser.find_elements_by_xpath("//a[@href]")
        ablinks=[i.get_attribute("href") for i in elems]
        self.selen_links=ablinks #hyperlinks this one by default get the whole links
        return browser #browser 
    def hyperlinks(self,base=""):#I did not specify the base because in some cases it cannot be equal to url
        try:
            links=[i.get("href") for i in self.pageB.find_all("a")]
            ablinks=[str(base)+ str(i) for i in links]
            return ablinks
        except:
            links=self.tree.xpath("//a/@href")
            ablinks=[str(base)+ str(i) for i in links]
            return ablinks
    @property
    def get_text_content(self):
        text=""
        for header in self.pageB.find_all(re.compile("h[1-6]{1}")):
            text+=header.get_text() + u'\n'
            for elem in header.next_siblings:
                if elem.name and elem.name.startswith('h'):
                    # stop at next header
                    break
                if elem.name == 'p':
                    text+=elem.get_text() + u'\n'
        return text
    def get_tag(self):
        tag=input("input a tag ")
        attribute_type =input("enter selector type: class, id, etc ")
        attribute_name=input("enter selector name ") 
        try:
            return self.pageB.find_all(tag, attrs={attribute_type:attribute_name})
        except:
            return self.tree.xpath("//%s[@%s='%s']"%(tag,attribute_type,attribute_name))
    
       
    


# Super_list class, which will take a list as input and provide the following functionalities:
# a. untilst function, that will return the unlisted version of a nested list or the same one if list was not nested,
# b. merge function, that will merge all the elements of any list into strings,
# c. find function that will take a type argument as an input. If type =:
# i. number, then it will return all the list elements that include a number,
# ii. letter, then it will return all the list elements that include a letter.

# In[13]:


class Super_list:
   
    def __init__(self,ls):
        self.ls=ls
    #def unlist(self):
    #    if any(isinstance(i, list) for i in self.ls)==True:
    #       return list(chain.from_iterable(self.ls))
    #   else:
    #        return self.ls
    def unlist(self):
        """the method defined above will not unlist mixed lists like [123,["123",[23]],"vazgen"] which contain integers 
        and mixed lists so this one can handle problems like that"""
        new_list=[]
        for i in range(len(self.ls)):
            inp = self.ls[i]
            if inp.__class__ == list:
                contains_list = any(map(lambda x: x.__class__ == list, inp))
                if contains_list:
                    unlist(inp, new_list)
                else:
                    new_list.extend(inp)
            else:
                new_list.append(inp)
        return new_list
    def to_string(self):
        new=[str(i) for i in self.unlist()] #made it str because we might have integers inside list
        return " ".join(new)
    def typelem(self,tip=str):
        new=[i for i in self.ls if isinstance(i, tip)]
        return new
    def select(self):
        choice=input("what do you want to get? ").lower()
        if choice=="numbers":
            return [float(i) for i in self.unlist() if str(i).isdigit()==True]
        elif choice=="letters":
            return [str(i) for i in self.unlist() if str(i).isalpha()==True]
        else:
            print("please insert numbers or letters")
            return self.select()


# Cleaner class, which will take a string as an input and provide the following methods:
# a. tokenize into words/sentences,
# b. lemmatize, clean stopwords,
# c. make plural/singular,
# d. uppercase/lowercase,
# e. draw frequency distributions of words

# In[76]:


class Cleaner:
    def __init__(self,string):
        self.string=TextBlob(string)
        self.words=self.string.words
        self.sentences=self.string.sentences
    
    """ This method works but i prefered do it as an attribute
    def tokenize(self,get_words=True,get_sent=False):
        if get_words==True and get_sent==False:
            words=self.string.words
            return words
        elif get_sent==True and get_words==False:
            sent=self.string.sentences
            return sent
        else:
            words=self.string.words
            sent=self.string.sentences
            return words,sent"""
    def lem_stopwords(self,lang="english"):
        sw = stopwords.words(lang)
        sw1=["n't","'re","'ll","'ve"]
        new = [i for i in self.words if i not in sw and len(i)>2 and i not in sw1]
        cleaned=TextBlob(" ".join(new))
        a=[]
        ## here we will loop twice to lemmatize both verbs and nouns
        for i in cleaned.words:
            a.append(i.lemmatize("v"))
        c=TextBlob(" ".join(a)).words
        d=[]
        for i in c:
            d.append(i.lemmatize("n"))
        las=TextBlob(" ".join(d)).words
        return TextBlob(" ".join(las))
    def plur_sing(self,plur=True):
        if plur==True:
            return self.lem_stopwords().words.pluralize()
        else:
            return self.lem_stopwords().words.singularize()
    def upper_lower(self,upper=True):
        if upper==True:
            return self.words.upper()
        else:
            return self.words.lower()
    def freq(self,n=20):
        freq = nltk.FreqDist(Cleaner(" ".join(self.upper_lower(False))).lem_stopwords().split(" "))
        return freq.plot(20,cumulative=False,title="Frequency plot for most met words for this Artist")
    def freq1(self,n=20):
        freq = nltk.FreqDist(Cleaner(" ".join(self.upper_lower(False))).lem_stopwords().split(" "))
        return freq.plot(20,cumulative=False,title="Frequency plot for most met words for this Genre")

