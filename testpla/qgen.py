import PyPDF2
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sys import argv
import re

from topia.termextract import extract
from topia.termextract import tag

from random import randint

# Setup Term Extractor
extractor = extract.TermExtractor()


# # YOU HAVE TO DELETE THE RAISE ERROR LINES IN ZOPE PACKAGE FOR THIS TO WORK ITS IN zope/interface/advice.py and
# zope/interface/declerations.py


def extractPdfText(filePath=""):
    # Open the pdf file in read binary mode.
    fileObject = open(filePath, "rb")

    # Create a pdf reader .
    pdfFileReader = PyPDF2.PdfFileReader(fileObject)

    # Get total pdf page number.
    totalPageNumber = pdfFileReader.numPages

    # Print pdf total page number.
    # print('This pdf file contains totally ' + str(totalPageNumber) + ' pages.')

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


def get_vocab(text):
    common = open("common.txt", "r").read().splitlines()
    words = [x[0].upper() for x in extractor(text)]
    return words


def fill_in_the_blank(text, vocab):
    sentences = text.upper().split(".")
    fib = []
    splits = set()
    for w in vocab:
        for v in w.split(" "):
            splits.add(v)

    for i in text.split(" "):
        if randint(0, 15) == 2:
            splits.add(i)
    pattern = "|".join([f" {w} " for w in splits]).upper()
    pattern = re.sub(r"[^\w]*", "", pattern)

    for sentence in sentences:
        fib.append(re.sub(pattern, "_________________", sentence.upper()))
    return [x for x in fib if "_________________" in x]


def create_test(text):
    with open("TEST.txt", "w") as test:
        test.write("Name: _________________\t\t\tDate:____________\n")
        test.write("\n\n\nSection 1. Define the folloiwing vocab terms:\t(1pt each)\n")
        vocab = get_vocab(text)

        for word in vocab:
            if randint(0, len(vocab)) > len(vocab) // 3:
                test.write(f"{word}:\n\n\n")

        test.write("\n\n\nSection 2. Fill in the blanks:\t(2pts each blank)\n\n")
        fib = fill_in_the_blank(text, vocab)
        for sentence in fib:
            if len(sentence) > 30 and randint(0, len(fib)) > len(fib) // 3:
                test.write(f"{sentence}\n\n")


if __name__ == "__main__":
    file = "sample.pdf" if len(argv) < 2 else argv[1]
    pdf_text = extractPdfText(file)
    create_test(pdf_text)
