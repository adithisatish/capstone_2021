import requests
import csv
from bs4 import BeautifulSoup
  
URL = "https://www.ereadingworksheets.com/figurative-language/poetic-devices/alliteration-examples/"
r = requests.get(URL)
  
soup = BeautifulSoup(r.content, 'html5lib')
data = []
with open("dataset.csv","w",newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['Text','Letter'])
    for row in soup.findAll('dd'):
        processed_text = str(row)[4:-5].strip().split(". ")[1]
        s_index = processed_text.find(">")
        # c_index = processed_text.find("<",s_index)
        letter = processed_text[s_index+1].lower()
        processed_text = processed_text.replace("<b>","")
        processed_text = processed_text.replace("</b>","")
        writer.writerow([processed_text, letter])
