import requests, os, io
from PIL import Image
from bs4 import BeautifulSoup

class Finder():
    def __init__(self):
        self.deleteimages()
    
    def deleteimages(self):
        for elem in os.listdir("images"):
            os.remove(os.path.join("images",elem))

    def getSoup(self, url):
        url = "https://en.wikipedia.org/wiki/" + url
        content = requests.get(url).content
        return BeautifulSoup(content, "html.parser")

    def save_images(self, imgs):
        for i, img in enumerate(imgs):
            url = "https:" + img["src"]
            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content))
            image.save(os.path.join("images",str(i))+os.path.splitext(url)[-1])

    def getSenators(self):
        soup = self.getSoup("List_of_current_United_States_senators")
        table = soup.find("table", {"id":"senators"})
        return table.find_all("img")

finder = Finder()
finder.deleteimages()