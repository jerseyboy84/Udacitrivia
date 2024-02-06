# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

#  ----------------------------------------------------------------
#  Student documentation starts here!
#  ----------------------------------------------------------------

#  ----------------------------------------------------------------
#  Udacitrivia Game
#  ----------------------------------------------------------------

This version of the Udacitrivia Game is based on the reference code provided by Udacity.
The frontend code is the unmodified reference code
The backend code includes new API endpoints which control the view (frontend) and models (trivia database), as well as a set of test cases

#  ----------------------------------------------------------------
#  Getting Started
#  ----------------------------------------------------------------

First create the trivia database ("createdb trivia") and pre-populate ("psql trivia < /backend/trivia.psql")
In my local environment, the postgres server required a password so I changed the table ownership from "student" to "rock", a user that was previously configured with a password

Next, activate the backend with these commands run from the /backend directory:
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

Confirm the backend is running by opening another terminal and executing "curl http://127.0.0.1:5000/categories"

Next, activate the frontend with this commands run from the /frontend directory: "npm start"

The react frontend server can be viewed as http://localhost:3000, and all aspects of the game can now be exercised using the frontend

The API can be automatically tested by creating a test db (trivia_test) using the same procedure as when creating the "trivia" db, then running python3 test_flaskr.py from the /backend directory

The test_flask.py executes both positive and negative test cases.  When creating new database entries, it also deletes them so database size remains constant over successive test runs.

#  ----------------------------------------------------------------
#  API reference
#  ----------------------------------------------------------------


#  Getting Started
#  ----------------------------------------------------------------

The base URL:   The backend URL is http://127.0.0.1:5000
Authentication: This version of the application does not require authentication or API keys


#  Error handling
#  ----------------------------------------------------------------

Errors are returned as JSON objects in the following format, with error 404 as an example:
{
    "success": False,
    "error": 404,
    "message": "Resource not found"
}

The API will generate the following errors:
400: Bad Request
404: Resource not found
405: Method not allowed
422: Content unprocessable

#  Endpoints
#  ----------------------------------------------------------------

#  ----------------------------------------------------------------
GET /categories
Returns a JSON object with all defined categories including id (integer) and type (string)

Sample request:
curl http://127.0.0.1:5000/categories

Sample response:
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}

#  ----------------------------------------------------------------
GET /questions
Returns a JSON object with all 6 defined categories, current category type, number of total questions, and list of questions including question (string), answer (string), category id (string), and difficulty (integer).  The questions are paginated in groups of 10.  The request optionally includes an argument to choose the page #, starting from 1.  If no page attribute is provided, the response will be for page 1. 

Sample request:
curl http://127.0.0.1:5000/questions?page=4

Sample response:
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "Science",
  "questions": [
    {
      "answer": "Taxi Driver",
      "category": 5,
      "difficulty": 3,
      "id": 48,
      "question": "Which movie starred Robert DeNiro asking \"are you talkin' to me?\""
    },
    {
      "answer": "Andy Warhol",
      "category": 2,
      "difficulty": 4,
      "id": 49,
      "question": "Which American artist is best known for blended art and pop culture?"
    },
    {
      "answer": "Guggenheim",
      "category": 2,
      "difficulty": 2,
      "id": 50,
      "question": "What museum in NYC is famous for modern art?"
    },
    {
      "answer": "cousins",
      "category": 4,
      "difficulty": 4,
      "id": 51,
      "question": "What is the relationship between Theodore and Franklin Roosevelt?"
    },
    {
      "answer": "Colonel Nathan R Jessup",
      "category": 5,
      "difficulty": 5,
      "id": 52,
      "question": "What character famously yelled \"you can't handle the truth\"?"
    },
    {
      "answer": "4 years",
      "category": 6,
      "difficulty": 1,
      "id": 53,
      "question": "What is the time between each successive summer Olympics?"
    }
  ],
  "success": true,
  "totalQuestions": 36
}

#  ----------------------------------------------------------------
GET /categories/<cat-id>/questions
Returns a JSON object with current category type, number of questions in that category, and list of questions including question (string), answer (string), category id (string), and difficulty (integer).

Sample request:
curl http://127.0.0.1:5000/categories/4/questions

Sample response:
{
  "currentCategory": "History",
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
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "Archduke Ferdinand",
      "category": 4,
      "difficulty": 4,
      "id": 29,
      "question": "Whose assasination triggered WWI?"
    },
    {
      "answer": "cousins",
      "category": 4,
      "difficulty": 4,
      "id": 51,
      "question": "What is the relationship between Theodore and Franklin Roosevelt?"
    }
  ],
  "success": true,
  "totalQuestions": 6
}

#  ----------------------------------------------------------------
POST /questions
Request includes a JSON object containing the question (string), answer (string), difficulty (integer), and category id (string).  When successful, the new question is added to the database and API returns a JSON object with the newly created question id (integer) and the new total number of questions (integer).


Sample request:
curl -X POST -H "Content-Type: application/json" -d '{"question":"What is the most popular new sport in the United States?","answer":"Pickleball","difficulty":"3","category":"5"}' http://127.0.0.1:5000/questions

Sample response:
{
  "created": 55, 
  "success": true, 
  "totalQuestions": 38
}

#  ----------------------------------------------------------------
POST /search
Request includes a JSON object containing the search term (string) associated with one of more questions.  The search is case insensitive, and if questions containing the serch term are found they will be returned along with the total number of matches as a JSON object.

Sample request:
curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"american"}' http://127.0.0.1:5000/search

Sample response:
{
  "questions": [
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "Andy Warhol", 
      "category": 2, 
      "difficulty": 4, 
      "id": 49, 
      "question": "Which American artist is best known for blended art and pop culture?"
    }
  ], 
  "success": true, 
  "totalQuestions": 2
}

#  ----------------------------------------------------------------
DELETE /questions/<question_id>
When question_id (integer) corresponds to an existing question id, that question is deleted from the database and the API returns a JSON object with the new total number of questions (integer).

Sample request:
curl -X DELETE http://127.0.0.1:5000/questions/57

Sample response:
{
  "success": true, 
  "totalQuestions": 36
}

#  ----------------------------------------------------------------
POST /quizzes
Request includes a JSON object containing the quiz category ("click" if no specific category) and the previous questions returned in the current quiz.   By including the previous questions in the request, these can be excluded from the set of possible next questions.


Sample request:
curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}}' http://127.0.0.1:5000/quizzes

Sample response:
{
  "question": {
    "answer": "force",
    "category": 1,
    "difficulty": 4,
    "id": 44,
    "question": "What is the product of mass and acceleration?"
  },
  "success": true
}


#  ----------------------------------------------------------------
#  Authors
#  ----------------------------------------------------------------

This version of the game was written by Brian Rockermann

#  ----------------------------------------------------------------
#  Acknowledgements
#  ----------------------------------------------------------------

Author wishes to acknowledge the contributions of Coach Caryn, and of Udacity.
