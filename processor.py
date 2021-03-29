import requests, os, io
from PIL import Image
from bs4 import BeautifulSoup

class Processor():
    def getSoup(self, url):
        """
        Returns the BeautifulSoup object of a given webpage.
        """
        url = "https://en.wikipedia.org/wiki/" + url
        content = requests.get(url).content
        return BeautifulSoup(content, "html.parser")

    def getSenatorUrls(self):
        """
        Returns a list of image sources of the current US Senators.
        """
        #get the soup of the list of senators wikipedia article
        soup = self.getSoup("List_of_current_United_States_senators")

        #find the table of senators and get the image sources
        table = soup.find("table", {"id":"senators"})
        urls = ["https:"+ elem["src"] for elem in table.find_all("img")]
        return urls
    
    def getPresidentUrls(self):
        """
        Returns a list of image sources of all US presidents.
        """
        #get the soup of the list of presidents wikipedia article
        soup = self.getSoup("List_of_presidents_of_the_United_States")

        #find the table of presidents and get the image sources
        table = soup.find("table", {"class":"wikitable"})
        urls = ["https:"+ elem["src"] for elem in table.find_all("img")]
        return urls
    
    def urlstoImages(self, urls):
        """
        Returns a list of PIL Image objects given image sources.
        """
        images = []
        for i, url in enumerate(urls):
            response = requests.get(url)
            images.append(Image.open(io.BytesIO(response.content)))
        return images

    def importImages(self, folder):
        """
        Returns a list of PIL Image objects given a folder of images.
        """
        images = []
        for file in os.listdir(folder):
            images.append(Image.open(os.path.join(folder,file)))
        return images

    def average(self, images, size=None):
        """
        Returns a PIL Image object representing the average pixels of a list of images.
        """
        #set the default image size as the size of the first image
        if size is None: size = images[0].size

        #sum all of the r, g, b values in every pixel of every image
        outputlist  = []
        for image in images:
            #convert the images to standardize them
            image = image.convert("RGB").resize(size)
            imagelist = list(image.getdata())

            #loop through each image to sum each r, g, b
            for i, pixel in enumerate(imagelist):
                red, green, blue = pixel
                if i >= len(outputlist): outputlist.append([0,0,0])
                RED, GREEN, BLUE = outputlist[i]
                outputlist[i] = [red + RED, green + GREEN, blue + BLUE]

        #divide each r,g,b by the number of images to average
        x = len(images)
        outputlist = [(r//x,g//x,b//x) for r, g, b in outputlist]

        #make a new image out of the averaged values
        output = Image.new("RGB", size)
        output.putdata(outputlist)
        return output          

if __name__ == "__main__":
    processor = Processor()
    images = processor.urlstoImages(processor.getSenatorUrls())
    average = processor.average(images)
    average.show()