import requests, uuid, pprint, os, sys
from bs4 import BeautifulSoup

URL = "https://oneidalanguage.ca/learn-our-language/oneidalanguage-words-phrases/page/"

if not os.path.exists("./audio"):
    os.makedirs("./audio")
    
file = open("Oneida-Dictionary.csv", "a")

for page in range(1, 93):
    req = requests.get(URL + str(page) + '/')
    soup = BeautifulSoup(req.text, 'html.parser')
    
    oneida_word = soup.find_all('p', class_= 'oneida')
    english_word = soup.find_all('p', class_= 'english')
    audio_links = []
    for tag in soup.find_all('a', class_= 'action primary'):
      audio_links.append(tag.get('href'))
      
    # Make CSV and append for page
    for one,eng,url in zip(oneida_word,english_word,audio_links):
      file.write(str(one.get_text()) + "," + str(eng.get_text()) + "\n")
      r = requests.get(url)
      filename = one.get_text() + ".mp3"
      with open(filename, 'wb') as f:
        f.write(r.content)
      os.rename("./" + str(one.get_text()) + ".mp3", "./audio/" + str(one.get_text()) + ".mp3")
      
file.close()
