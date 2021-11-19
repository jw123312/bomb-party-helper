import cv2
import pytesseract
import pyautogui
import numpy as np
import requests
from bs4 import BeautifulSoup
import re



pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
def getText():
    img = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
     
    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                     cv2.CHAIN_APPROX_NONE)


    im2 = img.copy()

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
         
        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Cropping the text block for giving input to OCR
        cropped = im2[550:600, 780:845] #TODO change this to automatic
        cv2.imshow('image',cropped)
        
        text = pytesseract.image_to_string(cropped)
        text = text.split("\n")[0]
        print(text)
        return text

def findWord(text):
    link = r"https://www.thefreedictionary.com/words-that-end-in-" + text
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    res = soup.find("div", class_ = "TCont")
    res = res.findAll('a', href=True)

    #TODO check used word
    word = ""
    
    while word == "":
        w = res.pop(0).contents
        w = str(w[0]) + str(w[1]).replace("<b>", "").replace("</b>","")
        if text.lower() not in str(w).lower():
            continue

        word = w
    return word

#main

text = getText()

if text.isalnum():
    print("word: ")
    print(findWord(text))
