import re
import os
import spacy
import requests  
import numpy
import matplotlib.pyplot as plt

from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image, ImageFont, ImageDraw 
from datetime import datetime
from textblob import TextBlob
from spacy.lang.en import English

class WordManager:
  def __init__(self):
    pass

  def get_story_text(self):
    with open('story.txt') as file:
      self.story = file.read()

  def clean_story(self):
    self.story = re.sub(r'\n+', ' ', self.story)#.strip()
    self.story = re.sub(r' +', ' ', self.story)#.strip()

  def get_nouns(self, phrase_length = 35):
    self.noun_lists = []
    sentences = []
    sentence = ''
    for i in range(0,len(self.story)):
      sentence += self.story[i]
      if sentence[-1] == '.' or (len(sentence)>phrase_length and self.story[i+1] == ' ') or (sentence[-1] == ',' and len(sentence)>20):
        if sentence[0] == ' ':
          sentence = sentence[1:]
        sentences.append(sentence)
        sentence = ''
      else:
        continue

    for sentence in sentences:
      blob = TextBlob(sentence)
      wanted_POS = {'NN','CD','NNP','VBG','NNS','VBN'}
      noun_list = [token[0] for token in blob.tags if token[1] in wanted_POS]
      self.noun_lists.append((sentence,noun_list))


class PictureManager:

  def __init__(self,num_imgs,word_lists):
    self.num_imgs = num_imgs
    self.word_lists = word_lists

  def save_img(self,sentence, sentence_idx,word_idx=None,img_idx=None,img_url=None):
    text = sentence    
    response = None
    img = None
    try:
      if img_url:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
      else:
        img = Image.open('black_bkgd.jpg')

      width, height = img.size
      draw = ImageDraw.Draw(img)
      font_size = 10
      font = ImageFont.truetype("arial.ttf", font_size)

      text_width, text_height = font.getsize(text)
      image_width, image_height = (width, height)

      left_edge = image_width - text_width - 5 - 0.5*(image_width - text_width)
      right_edge = left_edge + text_width + 10 # right edge, more positive = farther right

      top_edge = 0.7*image_height # more positive = farther down
      bottom_edge = top_edge + text_height + 2.0

      draw.rectangle((
          left_edge,
          bottom_edge, # bottom edge
          right_edge,
          top_edge # top edge
          ), fill='white')

      draw.text(
        (
          left_edge + 5, # left edge
          top_edge # top edge
          ), 
        text, fill=(0, 0, 0), font=font)

      sentence_str = str(sentence_idx).zfill(3)

      word_str = str(word_idx).zfill(3)

      img.save(f'imgs/sent_{sentence_str}_word_{word_str}.png')

      pass

    except:
      print("Could not get response...")


  def limit_imgs(self,all_imgs):

      num_total_imgs = len(all_imgs)

      self.img_urls=[]

      for img in all_imgs[:min(num_total_imgs-1,2*self.num_imgs)]:

        try:
          self.img_urls += [img['src']]

        except:
          continue


  def get_html(self,search_word):

      search_url = f'https://images.search.yahoo.com/search/images;_ylt=A?p={search_word}+icon&ei=UTF-8&fr=sfp&imgsz=large'

      htmldata = ''

      try:
        htmldata =  requests.get(search_url).text
      
      except: 
        pass

      soup = BeautifulSoup(htmldata, 'html.parser')  

      self.all_imgs = soup.find_all('img')


  def make_img_dir(self):

    folder_name = 'imgs'

    if not os.path.exists(folder_name):

      os.mkdir(folder_name)


  def get_imgs(self):

    self.make_img_dir()

    for sentence_idx, sentence_tuple in enumerate(self.word_lists):

      sentence = sentence_tuple[0]

      self.save_img(sentence=sentence,sentence_idx=sentence_idx)

      word_list = sentence_tuple[1]

      for word_idx, search_word in enumerate(word_list):

        self.get_html(search_word)

        self.limit_imgs(self.all_imgs)

        for img_idx,img_url in enumerate(self.img_urls[:self.num_imgs]):
            
            self.save_img(word_idx=word_idx,img_idx=img_idx,img_url=img_url, sentence=sentence, sentence_idx=sentence_idx)


def main():
  pass

if __name__ == "__main__":
   main()