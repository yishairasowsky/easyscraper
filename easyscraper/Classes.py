import re
import os
import spacy
import requests  
import numpy
import matplotlib.pyplot as plt

from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image, ImageFont, ImageDraw 
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

  def get_nouns(self):
    self.noun_lists = []
    chunks = []
    remainder = self.story
    chunk_chars = 60
    while len(remainder) > chunk_chars:
        chunk = remainder[0:chunk_chars]
        last_space = chunk.rfind(' ')
        chunk = chunk[:last_space]
        chunks.append(chunk)
        chunk_size = len(chunk)
        remainder = remainder[chunk_size +1:]
    chunks.append(remainder)

    sentences = chunks
    for sentence in sentences:
      blob = TextBlob(sentence)
      wanted_POS = {'NN',
      # 'CD',
      # 'NNP',
      # 'VBG',
      'NNS',
      # 'VBN'
      }
      noun_list = [token[0] for token in blob.tags if token[1] in wanted_POS]
      self.noun_lists.append((sentence,noun_list))

class PictureManager:
  def __init__(self,num_imgs,word_lists):
    self.num_imgs = num_imgs
    self.word_lists = word_lists

  def save_img(self,search_word,img_idx,img_url,sentence, sentence_idx):
    text = sentence
    response = None
    try:
      response = requests.get(img_url)
      img = Image.open(BytesIO(response.content))
      width, height = img.size
      draw = ImageDraw.Draw(img)
      font = ImageFont.truetype("arial.ttf", 12)

      text_width, text_height = font.getsize(text)
      image_width, image_height = (width, height)
      left_edge = image_width - 1.0*text_width - 5
      right_edge = image_width - 0.0*text_width + 5, # right side, more positive farther right
      draw.rectangle((
          left_edge,
          image_height, 
          right_edge,
          image_height - text_height
          ), fill='white')
      draw.text((left_edge, image_height - text_height), text, fill=(0, 0, 0), font=font)

      img.save(f'imgs/phrase_{sentence_idx}_word_{search_word}_{img_idx}.png')

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

      search_url = f'https://images.search.yahoo.com/search/images;_ylt=AwrExdrB_MlfwyYAsv6LuLkF;_ylc=X1MDOTYwNTc0ODMEX3IDMgRmcgMEZ3ByaWQDc0cuQS5iMU9ScGl0aVlTNFlUUnBrQQRuX3N1Z2cDMTAEb3JpZ2luA2ltYWdlcy5zZWFyY2gueWFob28uY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDBHFzdHJsAzYEcXVlcnkDcmFtYmFuBHRfc3RtcAMxNjA3MDcyOTY2?fr2=sb-top-images.search&p={search_word}&ei=UTF-8&iscqry=&fr=sfp'

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

      word_list = sentence_tuple[1]

      for search_word in word_list:

        self.get_html(search_word)

        self.limit_imgs(self.all_imgs)

        for img_idx,img_url in enumerate(self.img_urls[:self.num_imgs]):
            
            self.save_img(search_word,img_idx,img_url, sentence, sentence_idx)





def main():
  pass

if __name__ == "__main__":
   main()