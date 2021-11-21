import cv2
import pytesseract
import pyautogui
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import pyautogui
import time

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
        #cv2.imshow('image',cropped)
        
        text = pytesseract.image_to_string(cropped)
        text = text.split("\n")[0]
        print(text)
        return text

used = []
cache = dict()

def getWord(res, text):
    global used

    word = ""
    while word == "" or word in used:
        w = res.pop(0).find('a', href=True).contents[0]

        if text.lower() not in str(w).lower() or w == '':
            continue

        word = str(w)
    return word


def findWord(text):
    global used
    
    link = r"https://wordfind.com/contains/" + text
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    
    res = soup.findAll("li", class_ = "dl")

    word = getWord(res, text)
    
    used.append(word)
    
    return res, word



def typer(text):
    window = "BombParty"
    if window in pyautogui.getActiveWindow().title:
        pyautogui.typewrite(text)
        pyautogui.press("enter")

def addCache(res, text):
    global cache
    
    if text not in cache.keys():
        cache[text] = set()
    while res != []:
        cache[text].add(getWord(res,text))

#main

while True:
    inp = input("scan?")
    if inp.strip() == '': 
        text = getText()
    else:
        text = inp.strip().lower()
        
    text = text.lower()
    
    if text.isalnum():
        print("word: ")

        if text not in cache.keys():
            res, word = findWord(text)
        else:
            word = cache[text].pop()
        
        print("\t", word)
        pyautogui.hotkey("alt","tab")
        time.sleep(0.4)
        print(used)
        typer(word)

        if res is not None:
            addCache(res, text)

        res = None
        
    print()
