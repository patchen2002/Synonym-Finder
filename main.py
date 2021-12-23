# This is a web scraper for synonyms. Create an interface that will allow users to input words/and get synonyms
import tkinter
from tkinter import font
import requests
from bs4 import BeautifulSoup

# initializing the window
top = tkinter.Tk()
top.geometry("1000x800")
top.configure(bg="#FFFDD0")

# the different font families
headerFont = font.Font(family="Veradana", size=20, weight="bold")
generalFont = font.Font(family="Veradana", size=12)
buttonFont = font.Font(family="Veradana", size=10)

# frame for the header and the instructions
headerFrame = tkinter.Frame(bg="#FFFDD0")
headerFrame.pack(pady=30)

# making the header
header = tkinter.Label(headerFrame, text="Synonym Generator", width=70, bg="#FFFDD0")
header.pack()
header.configure(font=headerFont)

# making the instructions
instruction = tkinter.Label(headerFrame, text="Enter a word, then click the button. For multiple different words, "
                                              "type each phrase on a new line", width=100, bg="#FFFDD0")
instruction.pack()
instruction.configure(font=generalFont)

# making the frame for the text box
textFrame = tkinter.Frame()
textFrame.pack(padx=10, pady=10)

# making the textbox
text_box = tkinter.Text(textFrame, width=50, height=10, relief="solid", borderwidth=1)
text_box.configure(font=generalFont)

# initializing the output
outputMessage = tkinter.Message(text="", font=generalFont, width=800, bg="#FFFDD0")

# code for web scraping to retrieve the synonyms
def computeSynonym():
    outputString = ""
    listOf = list(text_box.get("1.0", tkinter.END).strip().split("\n"))

    for x in listOf:
        URL = "https://www.thesaurus.com/browse/" + x
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="meanings")
        try:
            synonyms = results.find_all("a")
        except AttributeError:
            outputMessage["text"] = "One of your words don't exist. Try again!"
            break

        synonymString = x.capitalize() + ": "
        counter = 0
        for synonym in synonyms:
            counter += 1
            s = synonym.text
            if counter == 1:
                synonymString += s.strip().capitalize()
            else:
                synonymString += ", " + s.strip().capitalize()

        outputString += synonymString + "\n"*2

    outputMessage["text"] = outputString


# making the frame/border for the button
buttonFrame = tkinter.Frame()
buttonFrame.pack(padx=10, pady=20)

# button to start calculate the synonyms
insertButton = tkinter.Button(buttonFrame, text="Enter", command=computeSynonym, relief="solid", borderwidth=1)
insertButton.configure(font=buttonFont)

text_box.pack()
insertButton.pack()
outputMessage.pack()

top.mainloop()
