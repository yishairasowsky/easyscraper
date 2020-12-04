import requests  
import matplotlib.pyplot as plt

from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup  


search_words = [
                # '',
                'chazonish',
                # 'yishairasowsky',
                ]    

num_imgs = 5

for search_word in search_words:

    search_url = f'https://images.search.yahoo.com/search/images;_ylt=AwrExdrB_MlfwyYAsv6LuLkF;_ylc=X1MDOTYwNTc0ODMEX3IDMgRmcgMEZ3ByaWQDc0cuQS5iMU9ScGl0aVlTNFlUUnBrQQRuX3N1Z2cDMTAEb3JpZ2luA2ltYWdlcy5zZWFyY2gueWFob28uY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDBHFzdHJsAzYEcXVlcnkDcmFtYmFuBHRfc3RtcAMxNjA3MDcyOTY2?fr2=sb-top-images.search&p={search_word}&ei=UTF-8&iscqry=&fr=sfp'

    htmldata =  requests.get(search_url).text

    soup = BeautifulSoup(htmldata, 'html.parser')  
    all_imgs = soup.find_all('img')
    num_total_imgs = len(all_imgs)

    img_urls=[]

    for img in all_imgs[:min(num_total_imgs-1,2*num_imgs)]:
      try:
        img_urls += [img['src']]
      except:
        continue

    for img_idx,img_url in enumerate(img_urls[:num_imgs]):
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        
        plt.imshow(img)
        plt.savefig(f'imgs/{search_word}_{img_idx}.png')