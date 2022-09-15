from bs4 import BeautifulSoup
import re
import os
import random
n=0
for directory in os.listdir("books"):
    with open(os.path.join("books", directory, directory+".htm"), 'r') as f: 
        soup = BeautifulSoup(f)
        pages = []
        h2tags = soup.find_all('h2')

        def next_element(elem):
            while elem is not None:
                # Find next element, skip NavigableString objects
                elem = elem.next_sibling
                if hasattr(elem, 'name'):
                    return elem

        for h2tag in h2tags:
            page = [str(h2tag)]
            elem = next_element(h2tag)
            while elem and elem.name != 'h2':
                page.append(str(elem))
                elem = next_element(elem)
            pages.append('\n'.join(page))
        pages = [page for page in pages if 'id="life_of' in page.lower()]
        if len(pages)>=3:
            min_chapter = min(pages, key=len)
            max_chapter = max(pages, key=len)
            avg_len = sum(len(s) for s in pages)/len(pages)
            avg_chapter = min(pages, key=lambda x:abs(len(x)-avg_len))
            chapters = [min_chapter, max_chapter, avg_chapter]
            for chapter in chapters:
                if 'id="life_of' in chapter.lower():
                    title = re.match(".*?id=\"(life_of_.*?)\"", chapter, re.IGNORECASE).group(1).lower()
                    output = open("chapters_new/"+title+".html", "w", encoding="utf-8")
                    output.write(chapter)
                    n+=1
print(n)
        