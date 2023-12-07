import random, json, torch, pyttsx3
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f:
    intents = json.load(f)
    
FILE = "data.pth"
data = torch.load(FILE)
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 176)

def say(text):
    engine.say(text)
    engine.runAndWait()

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()
bot_name = "Zylla"

def getRespons(sentence):
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)
    
    ouput = model(X)
    _, predicted = torch.max(ouput, dim=1)
    tag = tags[predicted.item()]
    
    probs = torch.softmax(ouput, dim=1)
    prob = probs[0][predicted.item()]
    
    
    if prob.item() > 0.8:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                ran = random.choice(intent['responses'])
                
                return ran
                
    elif prob.item() >= 0.4 and prob.item() >= 0.6:
        
        return f'Could you be more specific?'
        
    else:
        
        return f"I do not understand could you rephrase"
        
import tkinter
from tkinter import *

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, msg + ":You " +'\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
    
        res = getRespons(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
            
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


base = Tk()
base.title("LSA Chatbot")
base.geometry("400x500")
base.resizable(width=False, height=False)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.insert(END, "Bot: hello nice to meet you"'\n\n')
ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="8", height="2",
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="2", font="Arial")
#EntryBox.bind("<Return>", send)

#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=400, width=370)
EntryBox.place(x=8, y=420, height=70, width=265)
SendButton.place(x=280, y=420, height=70)

base.mainloop()