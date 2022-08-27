# Udaciti-Trivia
Udaciti Trivia is a simple web application that allows users to play a series of trivia quizzes from different domains which includes science, geography, history e.t.c.

Udaciti-trivia is build using **flask** in the backend and **react** in the frontend.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started
### Prerequisite and Local Development
#### Backend
from the backend folder run ```pip install -r requirements.txt``` this will install all the dependencies needed to run the application. the run to start the backend
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

by default the backend will be served on ```http://localhost:5000/``` which has been already proxied from the frontend.

#### frontend 
from the frontend folder run ```npm install``` this will install the dependencies needed for the frontend, then run ```npm start``` to start the frontend.

by default the frontend will be served on ```http://localhost:3000/```

### Tests 
in order to run the tests navigate to the backend folder the run 
```
./init_test_db.sh
python test_flaskr.py
```

## API Reference

### Getting started
- Base url: At present the api is served on the default url which is ```http://localhost:5000``` 
- Authentication: At present the API does not require any authentication or api keys

### Error Handling
The application uses standard ```HTTP status codes``` for successful or failed operation. Errors are returned as a ```JSON``` object which the following format:
```json
{
    "success": false,
    "message": "bad request"
}
```
The application will return these errors when a request failed:
- 400 - Bad Request
- 404 - Resource Not Found
- 422 - Not Processable
- 500 - Internal Server Error

## Endpoints
### GET /questions
- General:
    - return a list of questions, success, total number of questions
    - results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample:
    - curl http://127.0.0.1:5000/questions
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
    "questions": [
        {
            "answer": "Maya Angelou", 
            "category": 4, 
            "difficulty": 2, 
            "id": 5, 
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }, 
        {
            "answer": "Muhammad Ali", 
            "category": 4, 
            "difficulty": 1, 
            "id": 9, 
            "question": "What boxer's original name is Cassius Clay?"
        }, 
        {
            "answer": "Apollo 13", 
            "category": 5, 
            "difficulty": 4, 
            "id": 2, 
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ],
    "success": true,
    "total_questions": 3
    }
    ```

### POST /questions
- General 
    - add a new questions to the database, accepts question, category and answer from a json object
    - return success, question in a json response
- Sample
    ```shell
    $ curl -X POST -d '{"question": "What is the capital of India", "answer": "New Delhi", "category": 1}' http://127.0.0.1:5000/
    ```
    ```json
    {
        "succes": true,
        "created": 10
    }

    ```

### DELETE /questions/`<question_id>`
- General
    - Delete a specific question from the database with the given `question_id`
    - return success, deleted in a json response
- Sample
    ```json
    $ curl http://127.0.0.1:5000/questions/1
    {
        "success": true,
        "deleted": 1
    }
    ```

### GET /categories
- General
    - return all categories from the database
- Sample
    ```json
    $ curl /categories

    {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    }
}
    ```

### GET /categories/`<category_id>`/questions
- General 
    - return all questions from the category with given `category_id`
    - response are returned as json with success questions, total_questions, current_category as keys
- Sample
    ```json
    $ curl https://categories/1/questions
    {
        "current_category": "Sports", 
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
        "total_questions": 2
    }
    ````
### POST /quizzes
- General
    - accepts a json with `current_category`, `previous_questions`
    - return a random question from the given category if specified that is not already added to the `previous_questions` array.
- Sample
    ```shell
    $ curl -X POST -H "Content-Type: application/json;" -d '{"quiz_category": {"id": 6, "type": "Sports"}, "previous_questions": []}' http://127.0.0.1:5000/quizzes
    
    ```
    ```json
    {
    "previous_questions": [], 
    "question": {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    "success": true
    }
    ```

## Deployment N/A

## Authors
Your truly, Muhammad Lawal (Abba Raees)

## Acknowledgements
My sincere gratitude goes to all the members of the alx community and Udacity for all the support they gave during the course of the program.
