from easyscraper import *

wm = WordManager()

wm.get_story_text()
wm.clean_story()
wm.get_nouns()

num_imgs=1

pm = PictureManager(
    num_imgs=num_imgs,
    word_lists=wm.noun_lists
    )

pm.get_imgs()

print()