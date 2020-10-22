# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.conf import settings
from os.path import join

import PyPDF2
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sys import argv
from random import shuffle, randint
from re import sub
from string import punctuation


# This function will extract and return the pdf file text content.
def extractPdfText(filePath=""):
    # Open the pdf file in read binary mode.
    fileObject = open(filePath, "rb")

    # Create a pdf reader .
    pdfFileReader = PyPDF2.PdfFileReader(fileObject)

    # Get total pdf page number.
    totalPageNumber = pdfFileReader.numPages

    # Print pdf total page number.
    print("This pdf file contains totally " + str(totalPageNumber) + " pages.")

    currentPageNumber = 0
    text = ""

    # Loop in all the pdf pages.
    while currentPageNumber < totalPageNumber:
        # Get the specified pdf page object.
        pdfPage = pdfFileReader.getPage(currentPageNumber)

        # Get pdf page text.
        text = text + pdfPage.extractText()

        # Process next page.
        currentPageNumber += 1

    if text == "":
        # If can not extract text then use ocr lib to extract the scanned pdf file.
        text = textract.process(filePath, method="tesseract", encoding="utf-8")

    return text


# This function will remove all stop words and punctuations in the text and return a list of keywords.
def extractKeywords(text):
    # Split the text words into tokens
    wordTokens = word_tokenize(text)

    # Remove blow punctuation in the list.
    punctuations = ["(", ")", ";", ":", "[", "]", ","]

    # Get all stop words in english.
    stopWords = stopwords.words("english")

    # Below list comprehension will return only keywords tha are not in stop words and  punctuations
    keywords = [
        word
        for word in wordTokens
        if not word in stopWords and not word in punctuations
    ]

    return keywords


def get_fill_in_the_blank(text, vocab):
    sentences = text.split(".")

    fib = []
    d = "__________"

    for sentence in sentences:
        sentence += "."
        if len(sentence) < 50:
            continue

        v = [x.upper() for x in extractKeywords(sentence)]
        shuffle(v)
        s = sentence.upper().replace(v[0].upper(), d, 1)
        if d in s:
            f = s.split(d)
            if len(f) == 2:
                fib.append(f)

    return fib


# Create your views here.
def home(request):
    return render(request, "common/index.html")


def choose_textbook(request):
    return render(request, "common/textbook.html")


def get_test(request, filename):
    file_path = join(join(settings.BASE_DIR, "resources"), filename) + ".pdf"
    content = extractPdfText(file_path)

    vocab = [sub(r"[^\w\d]]", "", x).upper() for x in extractKeywords(content) if len(x) > 4 and '.' not in x]

    fill_in = get_fill_in_the_blank(content, vocab)

    shuffle(vocab)

    v = []
    for i in vocab:
        if randint(0, 10) < 2:
            v.append(i)

    shuffle(v)
    vocab = v[0:7]
    v = ["ATOMS", "NEUTRON", "ISOTOPE"]
    v.extend(vocab)

    context = {
        "TITLE": filename.upper(),
        "VOCAB": v,
        "FILL_IN": fill_in
    }

    return render(request, "common/test.html", context=context)
