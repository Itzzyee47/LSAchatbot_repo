import random, json, torch, pyttsx3, regex
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
engine.setProperty('rate', 166)

def say(text):
    engine.say(text)

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
    qes = sentence
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)
    
    ouput = model(X)
    _, predicted = torch.max(ouput, dim=1)
    tag = tags[predicted.item()]
    
    probs = torch.softmax(ouput, dim=1)
    prob = probs[0][predicted.item()]
    
    
    if prob.item() > 0.71:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                ran = random.choice(intent['responses'])
                print(str(prob.item()))
                return ran
                
    elif prob.item() >= 0.56 or prob.item() <= 0.7:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                # if tag === "digit":
                #     pass
                #responds to potentially unaccurate responds.....
                ran = f"<br>{random.choice(intent['responses'])}"
                print(str(prob.item()))
                return ran
        
    else:
        with open("newQ.csv","a") as f:
            newQ = f
            newQ.writelines(","+qes)
            newQ.close()
            print(str(prob.item()))
        return f"I do not understand could you rephrase"
        