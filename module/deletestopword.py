def getStopWord():
    with open('./module/stopword.txt', encoding='utf-8', mode='r+') as file:
        stopWord = file.readlines()
    return stopWord


def removeStopWord(text):
    stopWord = getStopWord()
    text = ' '.join([word for word in text.split() if word + '\n' not in stopWord])
    return text
