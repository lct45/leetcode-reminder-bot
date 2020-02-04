from bs4 import BeautifulSoup
import requests

def checkQuestions(username):
    url = 'https://leetcode.com/' + username + '/'
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    questions = content.find_all('span', attrs={"class": "badge progress-bar-success"})
    totalq = questions[1].text
    totalq = totalq.strip()
    print(totalq)
    totals = totalq.split('/')
    return totals[0]