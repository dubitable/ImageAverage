import requests, os, io
from PIL import Image
from bs4 import BeautifulSoup

class Finder():
    def __init__(self):
        self.deleteImages()
    
    def deleteImages(self):
        for elem in os.listdir("images"):
            os.remove(os.path.join("images",elem))

    def getSoup(self, url):
        url = "https://en.wikipedia.org/wiki/" + url
        content = requests.get(url).content
        return BeautifulSoup(content, "html.parser")

    def getImages(self, imgs):
        images = []
        for i, img in enumerate(imgs):
            url = "https:" + img["src"]
            response = requests.get(url)
            images.append(Image.open(io.BytesIO(response.content)))
        return images
        
    def getSenators(self):
        soup = self.getSoup("List_of_current_United_States_senators")
        table = soup.find("table", {"id":"senators"})
        return table.find_all("img")
    
    def getPresidents(self):
        soup = self.getSoup("List_of_presidents_of_the_United_States")
        table = soup.find("table", {"class":"wikitable"})
        return table.find_all("img")

if __name__ == "__main__":
    finder = Finder()
    imgs = finder.getSenators()
    images = finder.getImages(imgs)
    images[0].show()
    images[-1].show()