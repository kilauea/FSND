# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## Tasks

There are `TODO` comments throughout project. Start by reading the READMEs in:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom. 

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)

# Full Stack Trivia API

The Trivia app is developed as a full-stack app to be run from a web server, with a backend developed with Flask, and a front end developed with NodeJs.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

This app is part of the Full-Stack web development Nanodegree.

## Introduction

## Getting Started

* Base URL: The Trivia app runs only locally at the moment, it is not hosted in a server. The backend app is hosted at http://localhost:5000/, which is set as a proxy in the frontend configuration.
* Authentication: There is no authentication  implemented currently for the Trivia app.

### Pre-requsites and Local Development

This app requires Python3 and pip for development. It is highly recommened to use a [Python3 virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

To install the virtual environment run the following shell command from the root repoitory folder:
```bash
python3 -m venv venv
```

This will create the venm folder. To activate the virtual environment run the following shell command:
```bash
// macOS and Linux
source venv/bin/activate
// Windows
.\env\Scripts\activate
```

To check you are using the desired Python run the following shell command:
```bash
// macOS and Linux
which python3
.../env/bin/python3
// Windows
where python3
.../env/bin/python3.exe
```

#### Backend

The backend relies on Postgres database. To install it go to the [Postgres Download](https://www.postgresql.org/download/) page and download Postgres for your machine.

To install the requited python packages for the backend, from the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application, from the backend folder run the following shell commands: 
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application runs on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following shell commands to start the client: 
```bash
npm install // only once to install dependencies
npm start 
```

By default, the frontend runs on localhost:3000.

When installing the nmp modules, a new folder node_modules will be created. This folder should be added to .gitignore to avoid committing this folder by mistake.

### Tests

The Trivia API backend has been developed with unittest to allow testing all the endpoints.
In order to run the test from the backend folder run the following commads:
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
If the trivia_test database doesn't exist yet you can ommit the dropdb command.

All tests can be found in test_flaskr.py and should be maintained when updating the app functionality.

## Error Handling

All errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The Trivia API returns the following error types when requests fail:
* 400: Bad Request
* 404: Resource Not Found
* 422: Unprocessable

## API Reference

### GET '/categories'
- General:
  - Returns a dictionary with all the abailable categories, success value and the number of total categories
- Sample: `curl http://127.0.0.1:5000/categories`
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 6
}
```

### GET '/questions'
- General:
  - Returns a dictionary with all the abailable categories, a list of list of question objects, success value and the number of total questions
  - The list of question objects are paginated in groups of 10. Include the request argument 'page' to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/questions?page=2`
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": 1, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "Don Quijote de la Mancha", 
      "category": 4, 
      "difficulty": 2, 
      "id": 24, 
      "question": "What's the tittle of the most famous book of Miguel de Cervantes?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

### GET `/categories/<int:categoty_id>/questions`
- General:
  - Returns the current category, a list of quetion objects for the category_id passed, success value and the number of total questions
  - The list of question objects are paginated in groups of 10. Include the request argument 'page' to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/categories/6/questions`
```json
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

### POST `/questions`
- General:
  - This endpoint implements two functions:
    - When the argument 'searchTerm' is submitted it will search for questions containing the searchterm. The search is not case-sensitive. It returns the current category, a list of cuestion objects matching the search term paginated in groups of 10, success value and the number of total questions.
    - If the argument 'searchTerm' is not submitted it will create a new question using the submitted question, answer, category and difficulty. Returns success value.
- Search question sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"which"}'`
```json
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "Spain", 
      "category": 6, 
      "difficulty": 2, 
      "id": 25, 
      "question": "Which country won the soccer World Cup in 2011"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```
- Create new question sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Which country won the soccer World Cup in 2011", "answer":"Spain", "category":"6", "difficulty":"2"}'`
```json
{
  "success": true
}
```

### POST `/quizzes`
- General:
  - Selects a ramdom question from the submitted quiz category, and avoiding the previous questions that were previously selected. Returns a question object and success value.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"id":1, "type":"Science"}}'`
```json
{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }, 
  "success": true
}
```

### DELETE `/questions/<int:question_id>`
- General:
  - Deletes the question of the given ID if it exists. Returns a dictionary with all categories, the current category, the ID of the deleted category, a list of questions paginated in groups of 10, success value and the number of total questions.
- Sample: `curl http://127.0.0.1:5000/questions/20 -X DELETE`
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": 1, 
  "deleted": 20, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

## Authors

Arturo Crespo de la Viña

## Ackknowledgements

The Udacity team.
