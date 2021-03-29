# ImageAverage
The "average person" is a mythical being, known only to most as theoretical. With ImageAverage, you have the possibility to have explore this legend, be it with all US senators, presidents, or with your own images.
## Main concepts
#### Retrieving the images
While this program allow importing the user's own images, I originally got the idea for it from a single question: what would happen if I averaged every single US Senator? The first problem I encountered was retrieving the images: I do not possess photos of every single senator, contrary to popular belief. Thankfully, Wikipedia provides lists, complete with images as well as extra information. Unfortunately, the website does not have a standard for each article, which makes the HTML parsing a little more difficult.
```
processor = Processor()

# get the PIL Image objects of all senators
images = processor.urlstoImages(processor.getSenatorUrls())

# get the PIL Image objects of your own images
images = processor.importImages(folder)
```
#### Image Processing
The image processing is pretty straightforward: loop through every single pixel in every single image and take the sum of all the red, green, and blue values. At the end, we can divide each of these values by the amount of images.
```
processor = Processor()

# get the PIL Image objects of all senators
images = processor.urlstoImages(processor.getSenatorUrls())

# show the PIL Image object of averaged image
average = processor.average(images)
average.show()
```
## Functionality
```
Processor()
```

The Processor class allows for the retrieving and processing of images for averaging purposes.

---

```
Processor.average(self, images, size = None)
```

Returns a PIL Image object representing the average pixels of a given list of images.  
 
`images`: a `list` of PIL Image objects.
`size`: the size (`2-tuple`) of the output image (optional argument set by default to the size of the first image in `images`).

```
Processor.importImages(self, folder)
```

Returns a list of PIL Image objects given a folder of images.  

`folder`: the path (`string`) to a directory of images 

```
Processor.urlstoImages(self, urls)
```

Returns a list of PIL Image objects given image sources.  

`urls`: a `list` of image source urls.

```
Processor.getSenatorUrls(self)
```

Returns a list of image sources of the current US Senators.  

```
Processor.getPresidentUrls(self)
```

Returns a list of image sources of all US Presidents.  

```
Processor.getSoup(self, url)
```

 Returns the BeautifulSoup object of a given webpage.
 
 `url`: a url of a webpage.
