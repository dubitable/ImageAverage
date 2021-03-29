import requests, os, io
from PIL import Image
from bs4 import BeautifulSoup

class Processor():
    def getSoup(self, url):
        url = "https://en.wikipedia.org/wiki/" + url
        content = requests.get(url).content
        return BeautifulSoup(content, "html.parser")

    def urlstoImages(self, urls):
        images = []
        for i, url in enumerate(urls):
            response = requests.get(url)
            images.append(Image.open(io.BytesIO(response.content)))
        return images

    def getSenatorUrls(self):
        soup = self.getSoup("List_of_current_United_States_senators")
        table = soup.find("table", {"id":"senators"})
        urls = ["https:"+ elem["src"] for elem in table.find_all("img")]
        return urls
    
    def getPresidentUrls(self):
        soup = self.getSoup("List_of_presidents_of_the_United_States")
        table = soup.find("table", {"class":"wikitable"})
        urls = ["https:"+ elem["src"] for elem in table.find_all("img")]
        return urls
    
    def importImages(self, folder):
        images = []
        for file in os.listdir(folder):
            images.append(Image.open(os.path.join(folder,file)))
        return images

    def average(self, images, size=None):
        if size is None: size = images[0].size
        outputlist  = []
        for image in images:
            image = image.convert("RGB").resize(size)
            imagelist = list(image.getdata())
            for i, pixel in enumerate(imagelist):
                red, green, blue = pixel
                if i >= len(outputlist): outputlist.append([0,0,0])
                RED, GREEN, BLUE = outputlist[i]
                outputlist[i] = [red + RED, green + GREEN, blue + BLUE]
        x = len(images)
        outputlist = [(r//x,g//x,b//x) for r, g, b in outputlist]
        output = Image.new("RGB", size)
        output.putdata(outputlist)
        return output          

if __name__ == "__main__":
    processor = Processor()
    images = processor.urlstoImages(processor.getSenatorUrls())
    average = processor.average(images)
    average.show()