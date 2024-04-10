import random
import requests
from bs4 import BeautifulSoup
import ast

def is_question_valid(question_text):
    return "toutes utilisées." not in question_text and "Explique" not in question_text

def requestCisco():
    url = 'https://ccnareponses.com/ccna-1-examen-final-itnv7-questions-et-reponses-francais/'
    r = requests.get(url)
    
    if r.status_code != 200:
        raise Exception(f"Failed to retrieve data. Status code: {r.status_code}")

    html_content = r.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract all questions and answers
    questions = []
    current_question = None  # Initialize current_question to None
    for tag in soup.find_all(['strong', 'figure', 'li', 'span']):
        if tag.name == 'strong':
            question_text = tag.text.strip()
            if is_question_valid(question_text) and tag.find_parent('li') is None:
                current_question = {'question': question_text, 'answers': []}
                questions.append(current_question)
        elif tag.name == 'figure' and current_question is not None and is_question_valid(question_text):
            image_url = tag.find('img')['data-src'] if tag.find('img') else None
            if image_url is not None:
                current_question['image_url'] = image_url
        elif tag.name == 'span' and current_question is not None and is_question_valid(current_question['question']):
            pass
        elif tag.name == 'li' and current_question is not None and is_question_valid(question_text):
            answer_text = tag.text.strip()
            is_correct = 'correct_answer' in tag.get('class', [])
            current_question['answers'].append({'answer': answer_text, 'correct': is_correct})
    

    
    res = []
    for question in questions:
        print(question['question'])
        if "28. Quelles sont" in question['question']:
            ans = []
            ans.append(f"Question: {question['question']}")
            for j in range (5):
                lettre = ['A', 'B', 'C', 'D', 'E']
                ans = []
                ans.append(f"Question: Version {lettre[j]} {question['question']}")
                for i in range(5):
                    ans.append(f" - {question['answers'][i*j]['answer']} {'(Correct)' if question['answers'][i*j]['correct'] else ''}")
                res.append(ans)
        elif "116. Associez les protocoles d’application aux" in question['question']:
            pass
        elif "116. Quel est l’ID de sous-réseau associé à l’adresse IPv6 2001:DA48:FC5:A4:3D1B::1/64\xa0?" in question['question']:
            pass
        elif "Quel est l’ID de sous-réseau associé à l’adresse IPv6 2001:DA48:FC5:A 4:3 D1B::1/64?" in question['question']:
            ans = []
            ans.append(f"Question: 116. {question['question']}")
            for answer in question['answers']:
                ans.append(f" - {answer['answer']} {'(Correct)' if answer['correct'] else ''}")
            if 'image_url' in question:
                ans.append({"URL" : question['image_url']})
            res.append(ans)
        else:
            ans = []
            ans.append(f"Question: {question['question']}")
            for answer in question['answers']:
                ans.append(f" - {answer['answer']} {'(Correct)' if answer['correct'] else ''}")
            if 'image_url' in question:
                ans.append({"URL" : question['image_url']})
            res.append(ans)
           
    with open("BotCisco/questionCisco.txt", "wb") as f:
        f.write(str(res).encode())
    return res

def questionCisco():
    try:
        with open("BotCisco/questionCisco.txt", "rb") as f:
            data = f.read()
            res = ast.literal_eval(data.decode())
    except (FileNotFoundError, SyntaxError, Exception) as e:
        print(f"Error reading file or evaluating data: {e}")
        res = requestCisco()
    return res