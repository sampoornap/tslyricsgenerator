from nltk.tokenize import word_tokenize
import random

text=''
with open("taylorlyrics.txt", 'r') as lyricstext:
    text=lyricstext.readlines()
    
  
def gen_text(text):
    generated_text = []
    for line in text:
        
        tokens = word_tokenize(line)
        words = [word for word in tokens if word.isalpha()]
        generated_text += words
    return generated_text

lyrtext = gen_text(text)

def markov_model_gen(lyr, n_gram=2):
    markov_model = {}
    for i in range(len(lyr)-n_gram-1):
        pstate=""
        nstate=""
        for j in range(n_gram):
            pstate += lyr[i+j] + " "
            nstate += lyr[i+j+n_gram] + " "
        pstate = pstate[:-1]
        nstate = nstate[:-1]
        
        if pstate not in markov_model:
            markov_model[pstate] = {}
            markov_model[pstate][nstate] = 1
        else:
            if nstate in markov_model[pstate]:
                markov_model[pstate][nstate] +=1
            else:
                markov_model[pstate][nstate] = 1
                
    #transition probabilities
    for pstate, transition in markov_model.items():
        total = sum(transition.values())
        for state, count in transition.items():
            markov_model[pstate][state] = count/total
    
    return markov_model


markov_model = markov_model_gen(lyrtext)
#print(len(markov_model.keys()))
print(markov_model['and i'])


def generate_lyrics(model, limit=100, start='and i'):
    n = 0
    pstate = start
    nstate = None
    lyric = ""
    lyric += pstate + " "
    while n < limit:
        nstate = random.choices(list(model[pstate].keys()),
                                list(model[pstate].values()))
        pstate = nstate[0]
        lyric += pstate + " "
        n += 1
    return lyric

for i in range(10):
    print(generate_lyrics(markov_model, limit=100))


