# Full Stack Trivia App

This application is created as a final project for Udacity's Full Stack Nano Degree. The project is a web appication to manage the trivia app and play the game.
This project was created to structure plan, implement, and test an API using Flask and SQLAlchemy server.

## Getting Started

### Pre-requisites and local development

Developers need to have Python3, pip and node installed to run this application.

**Backend**

From the backend folder run `pip install requirements.txt` which includes all the required packages.
To run the application,

`FLASK_APP=flaskr FLASK_ENV=development flask run`

This runs the application in develop and debug mode in `__init__.py` file of the flaskr folder. To run on Windows please view [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/installation/).

The application is now run on `http://127.0.0.1:5000/` by default.

**Frontend**

To configure the frontend of the application, from the frontend folder run,

```
npm i //install all node dependencies
npm start
```

The frontend will run by default on `http://localhost:3000/`

### Tests

To run tests,

```
dropdb test_trivia && createdb test_trivia
psql test_trivia < trivia.psql
python test_flaskr.py
```

## API reference

- Base URL : At present the frontend React app is run locally on localhost:3000, not hosted on a base URL. The flask backend is served at 127.0.0.1:5000.
- API Keys /Authentication is not required at the moment

## Error Handling

Errors are returned as JSON Objects in the following format

```
{
        "success": False,
        "error": 400,
        "message": "bad request"
}
```

The API returns the following response codes in case of an error:

- 400, Bad Request
- 404, Method not allowed
- 422, Unprocessable request

The tests are updated as the functionality of the app is updated.

## Endpoint library

### GET /questions

- General
  - Returns a list of quesions, success value, list of categories and the total number of questions
  - Results are paginated by 10 books per page. To access a particular page add a page argument to the url.
- Sample request: `curl http://127.0.0.1:5000/questions`

```
{
   "categories":{
      "1":"Science",
      "2":"Art",
      "3":"Geography",
      "4":"History",
      "5":"Entertainment",
      "6":"Sports"
   },
   "current_category":null,
   "questions":[
      {
         "answer":"Apollo 13",
         "category":5,
         "difficulty":4,
         "id":2,
         "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      },
      {
         "answer":"Tom Cruise",
         "category":5,
         "difficulty":4,
         "id":4,
         "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      },
      {
         "answer":"Maya Angelou",
         "category":4,
         "difficulty":2,
         "id":5,
         "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      },
      {
         "answer":"Edward Scissorhands",
         "category":5,
         "difficulty":3,
         "id":6,
         "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      },
      {
         "answer":"Muhammad Ali",
         "category":4,
         "difficulty":1,
         "id":9,
         "question":"What boxer's original name is Cassius Clay?"
      },
      {
         "answer":"Brazil",
         "category":6,
         "difficulty":3,
         "id":10,
         "question":"Which is the only team to play in every soccer World Cup tournament?"
      },
      {
         "answer":"Uruguay",
         "category":6,
         "difficulty":4,
         "id":11,
         "question":"Which country won the first ever soccer World Cup in 1930?"
      },
      {
         "answer":"George Washington Carver",
         "category":4,
         "difficulty":2,
         "id":12,
         "question":"Who invented Peanut Butter?"
      },
      {
         "answer":"Lake Victoria",
         "category":3,
         "difficulty":2,
         "id":13,
         "question":"What is the largest lake in Africa?"
      },
      {
         "answer":"The Palace of Versailles",
         "category":3,
         "difficulty":3,
         "id":14,
         "question":"In which royal palace would you find the Hall of Mirrors?"
      }
   ],
   "success":true,
   "total_questions":19
}
```

### GET /categories

- General
  - Returns a list of categories, success value, and the total number of categories
  - Results are paginated by 10 books per page. To access a particular page add a page argument to the url.
- Sample request: `curl http://127.0.0.1:5000/categories`

```
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

### DELETE /questions/{question_id}

- General
  - Returns a list of quesions, success value, list of categories and the total number of questions
  - Results are paginated by 10 books per page. To access a particular page add a page argument to the url.
- Sample request: `curl http://127.0.0.1:5000/questions/6`

```
{
    "success": True,
    "deleted": 6
}
```

### POST /questions

- General
  - Creates a new question from the given question, answer, difficulty and category. Returns a success value.
    - Sample request: `curl -X POST "http://127.0.0.1:5000/questions" -H "Content-type: application/json" -d '{"question":"Who is the author of The Hunger Games","answer":"Suzanne Collins","difficulty":4,"category":5}'`
    ```
    {
    "success": true
    }
    ```
  - Can also be used to search a particular search term.
    - Sample request: `curl -X POST "http://127.0.0.1:5000/questions" -H "Content-type: application/json" -d '{"searchTerm":"Hunger"}'`
    ```
    {
        "current_category": null,
        "questions": [
            {
            "answer": "Suzanne Collins",
            "category": 5,
            "difficulty": 4,
            "id": 28,
            "question": "Who is the author of The Hunger Games"
            },
            {
            "answer": "Suzanne Collins",
            "category": 5,
            "difficulty": 4,
            "id": 29,
            "question": "Who is the author of The Hunger Games"
            }
        ],
        "success": true,
        "total_questions": 2
        }
    ```

### GET /categories/{category_id}/questions

- General
  - Retrive lists of questions per category.
  - Returns a list of quesions, success value, current category and the total number of questions.
- Sample request: `curl http://127.0.0.1:5000/categories/5/questions`

```
{
  "current_category": 5,
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
      "answer": "Suzanne Collins",
      "category": 5,
      "difficulty": 4,
      "id": 28,
      "question": "Who is the author of The Hunger Games"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

### POST /quizzes
