### General
Basic usage of Django Rest API - created for storing movies details in local database. After geting movie title send request to  omdb API to check movie details and saves them in local database. Handles adding own comments and based on amount of comment in specified date range ranks movies.    

### Preview
- to add movie or show list of all movies use: https://protected-basin-94413.herokuapp.com/movies/
- to add comment or show list of all comments use: https://protected-basin-94413.herokuapp.com/comments/
- to show comments for one movie use: https://protected-basin-94413.herokuapp.com/comments/?movie_id=1
- to see most commented movies use: https://protected-basin-94413.herokuapp.com/top/?date_from=2019-01-01&date_to=2019-04-01

### Technologies
Python 3.6, Django 2.1, Django Rest API, PostgreSQL

### Instalation
To use repository locally you need to have Python 3.5+, PostgreSQL server installed on your computer. 
1. Clone repository and save it locally
2. Change branc to dev by typing in console ```git checkout dev```
3. Install depencies using ```pip install -r requirements.txt``` command
4. Log into PosgreSQL using ```psql -U username -h localhost -p``` command, type your password and create database
5. In root directory create ```.env``` file and add this lines: 
```
SQL_NAME=< your database name >
SQL_USER=< your database username >
SQL_PSWD=< your database password >
OMDB_API_KEY=< your API key from http://www.omdbapi.com >
DEBUG=True
```
6. Run ```python manage.py makemigrations``` and ```python manage.py migrate``` commands
7. Run ```python manage.py runserver``` and enjoy your local api

### Usage
There are 3 endpoints in repository:
1. http://127.0.0.1:5000/movies/ 
   - By using GET method you will get access to all movies stored in database
   - By using POST method you can add movie to database
     ```{
	       "title": "shrek"
        }```

2. http://127.0.0.1:5000/comments/
   - By using GET method you will get access to all comments stored in database, you can also pass additional parameter to        list comments only for specified movie like in example:```http://127.0.0.1:5000/comments?movie_id=1``` 
   - By using POST method you can add comment to existing in local database movie
    ```{
	      "body": "comment text",
	      "movie": 1
       }```
3. http://127.0.0.1:5000/top/
    - By using GET method you will get access to movies ranking based on amount of comments added in specified date range. To use it correctly you need to pass additional parameters to url like in this example: ```http://127.0.0.1:5000/top/?date_from=2019-01-01&date_to=2020-01-01```
   







