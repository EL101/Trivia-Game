#Note: you might have to pip install requests
import requests
import random
from pprint import pprint

#Author: Ethan Liu
#Contract: None -> dictionary
#Description: This function takes in the user input of the difficulty of the questions and the amount of questions they want. It them puts them into a dictionary for later use.
#Test: getInput()
def getInput():
  diff=input("What difficulty do you want the questions to be?(easy/medium/hard) ")
  while (diff not in ["easy", "medium", "hard"]):
    diff=input("Please give a valid input (easy, medium, or hard) ")
  amount=input("How many questions do you want?(up to 50 questions) ")
  while ((not amount.isdigit()) or int(amount) > 50 or int(amount) <= 0):
    amount=input("Please give a valid input (integer between 1 and 50 inclusive) ")
  params = {
    "amount": int(amount),
    "difficulty": diff
  }
  return params

#Author: Ethan Liu
#Contract: string -> string
#Description: This function takes in a string and replaces the symbols that did not print correctly into their correct symbols.
#Test: removeSymbols(&quot;Pokemon&#039;s&quot;) -> "Pokemon's"
def removeSymbols(s):
  s=s.replace("&quot;", "\"")
  s=s.replace("&#039;", "\'")
  return s

#Author: Ethan Liu
#Contract: dictionary -> None
#Description: This function gets the trivia questions from this website: https://opentdb.com. It gets the user specified difficulty and amount of questions from the getInput() function. It then converts that data into a csv file so that it is easier to read.
#Test: makeCSVfromData({"amount": 10, "difficulty": "medium"})
def makeCSVfromData(params):
  r=requests.get("https://opentdb.com/api.php", params=params)
  data=r.json()
  with open("data.csv", "w") as txt:
    for i in data["results"]:
      q=removeSymbols(i['question'])
      c=removeSymbols(i['correct_answer'])
      L=[]
      for x in i['incorrect_answers']:
        L.append(removeSymbols(x))
      str='/// '.join(L)
      txt.write(f'{q},, {c},, {str}\n')

#Author: Ethan Liu
#Contract: None -> List
#Description: This function converts the csv file into a list in order to make it easier to handle the data. The question and the correct answer are strings while the incorrect answers are thrown into a list.
#Test: getData()
def getData():
  ret = []
  with open("data.csv", "r") as txt:
    ret=[x.split(",, ") for x in txt.read().split("\n")]
  for i in ret:
    i[-1]=i[-1].split("/// ")
  # print(ret)
  return ret[:-1]

#Author: Ethan Liu
#Contract: List -> List of dictionaries
#Description: This function converts the list outputed by the getData() function and converts it into a list of dictionaries. Each dictionary contains the question, the correct answer, and a list of all the incorrect answers. This makes the code more readable and easier to understand.
#Test: ListtoDict()
def ListtoDict(data):
  ret=[]
  for i in data:
    d={}
    d['question']=i[0]
    d['correct_answer']=i[1]
    d['incorrect_answers']=i[2]
    ret.append(d)
  # print(ret)
  return ret

#Author: Ethan Liu
#Contract: dictionary -> list
#Decription: This function takes in a dictionary of a question and shuffles the incorrect answer with the correct answer. It uses random.shuffle() to do this.
#Test: shufflChoices({"question": "What color is the sky", "correct_answer": "blue", "incorrect_answers": ["purple", "silver", "green"]})
def shuffleChoices(question):
  L=question["incorrect_answers"]
  L.append(question["correct_answer"])
  random.shuffle(L)
  return L

#Author: Ethan Liu
#Contract: List -> dictionary
#Description: This function takes in the shuffled answer choices and displays them with their corresponding letter values. 
#Test: makeMultipleChoice([100, 20, 19, 11])
def makeMultipleChoice(L):
  count=0
  str="ABCD"
  dict={}
  for j in L:
    print(str[count]+") ",j)
    dict[str[count]]=j
    count+=1
  return dict

#Author: Ethan Liu
#Contract: None -> None
#Description: This function first gets the user inputs and then calls the functions that get the questions and turns it into a csv file. It then calls the functions to convert that csv file into a list of dictionaries. Then, for every question, it shuffles the chioces and takes in the user's answer. Finally, it tells the user if they are correct or not.
#Test: main()
def main():
  params = getInput()
  makeCSVfromData(params)
  ListData=getData()
  data=ListtoDict(ListData)
  for i in data:
    print(i['question'], "\n")
    L=shuffleChoices(i)
    dict=makeMultipleChoice(L)
    user_ans=input("What is your answer? ")
    while (user_ans not in "ABCD"):
      print("INVALID INPUT")
      user_ans=input("Try again. ")
    if (dict[user_ans]==i["correct_answer"]):
      print("CORRECT!\n")
    else:
      print("WRONG!\nCORRECT ANSWER WAS: ", i["correct_answer"], "\n")

main()   
