import os
from tkinter import *

import spacy

frame = Tk()
frame.title("Text Summariser")
frame.iconbitmap("text.ico")
frame.geometry('1100x800')

import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# def printInput():
#     inp = inputtxt.get(1.0, "end-1c")
#     lbl.config(text=inp.capitalize())

def copyToClipboard(text):
	command = 'echo ' + text.strip() + '| clip'
	os.system(command)

def summarizeText():
	text = inputtxt.get(1.0, "end-1c")

	from spacy.lang.en.stop_words import STOP_WORDS
	from string import punctuation

	stopwords = list(STOP_WORDS)

	nlp = spacy.load('en_core_web_sm')

	doc = nlp(text)

	tokens = [token.text for token in doc]

	punctuation = punctuation + '\n'

	word_frequencies = {}
	for word in doc:
		if word.text.lower() not in stopwords:
			if word.text.lower() not in punctuation:
				if word.text not in word_frequencies.keys():
					word_frequencies[word.text] = 1
				else:
					word_frequencies[word.text] += 1

	max_frequency = max(word_frequencies.values())

	for word in word_frequencies.keys():
		word_frequencies[word] = word_frequencies[word] / max_frequency

	sentence_tokens = [sent for sent in doc.sents]

	sentence_scores = {}
	for sent in sentence_tokens:
		for word in sent:
			if word.text.lower() in word_frequencies.keys():
				if sent not in sentence_scores.keys():
					sentence_scores[sent] = word_frequencies[word.text.lower()]
				else:
					sentence_scores[sent] += word_frequencies[word.text.lower()]

	from heapq import nlargest

	select_length = int(len(sentence_tokens) * 0.3)

	summaryList = nlargest(select_length, sentence_scores, key=sentence_scores.get)

	summary = ""

	for i in summaryList:
		summary += str(i) + " "

	summary = summary[:-1]

	# lbl.config(text = summary)
	SummaryOutput.insert(END, summary)

# TextBox Creation
inputtxt = Text(frame,
					font=12,
                   height=11,
                   width=90,
					padx=20,
					pady=40)

inputtxt.pack(pady= 5)

# Button Creation
# printButton = tk.Button(frame,
#                         text="Summarise",
#                         command=printInput)

printButton = Button(frame,
					font=12,
                    text="Summarise",
                    command=summarizeText)

printButton.pack(pady= 5)

label_text = StringVar();

# # Label Creation
# lbl = Label(frame, height=8, width=60, text="")
# lbl.pack()

SummaryOutput = Text(frame,
					 font=12,
					height = 11,
              		width = 90,
              		bg = "light cyan",
					padx=20,
					pady=40)
SummaryOutput.pack(pady= 5)

copyButton = Button(frame,
					font=12,
					text="Copy")

copyButton.pack(pady=5)

frame.mainloop()
