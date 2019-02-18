import sys, time, os
import urllib.request
from selenium import webdriver

def main(argc):
	input1 = argc[1]
	input1 = input1.split()
	#item = input1[0]
	#for i in range(len(input1)-1):
	#	item = item + "+" + input1[i+1]
	item = "+".join(input1) #format the first argument so that it's compatible with searchGoogle link below
	searchGoogle = "https://www.google.co.in/search?q=" + item + "&source=lnms&tbm=isch" #google image link for searching the item 
	#folderName = argc[2]	
	folderName = argc[1]
	if not os.path.exists(folderName):
		os.makedirs(folderName)
	
	print("Scraping \"" + argc[1] + "\" images -> ", end='')
	option = webdriver.ChromeOptions()
	option.add_argument('headless') #invisible browser (run in background)
	browser = webdriver.Chrome(options=option) #open Chrome
	browser.get(searchGoogle) #open the search link
	scrollHeight = browser.execute_script("return document.body.scrollHeight") #get scroll height
	
	while True:
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scroll down to bottom using javascript
		time.sleep(1.5) #load page
		newScrollHeight = browser.execute_script("return document.body.scrollHeight") #find new scroll height and compare from last scroll height
		if newScrollHeight == scrollHeight:
			break
		scrollHeight = newScrollHeight

	print("done")
	print("Saving...")
	images = browser.find_elements_by_tag_name("img") #find html tag "img"	
	numbImage = 1
	for image in images:
		className = image.get_attribute('class') #read class attributes of "img" tag
		if "rg_ic rg_i" in className: #class "rg_ic rg_i" is for actual image of the item 
			link = image.get_attribute('src') #read link of the image 
			try:
				urllib.request.urlretrieve(link, folderName + "/" + str(numbImage))
				numbImage += 1
			except TypeError:
				continue
	numbImage -= 1 #total number of images
	print("Total " + str(numbImage) + " images are saved in \"" + folderName + "\" folder")
	browser.close()	

if __name__ == '__main__':
	main(sys.argv)
