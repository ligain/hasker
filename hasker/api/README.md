# Hasker: API
  API is available by path `http://localhost:8000/api/v1`
  All API call should be performed by authorized user. To authorize you need to obtain JWT token.
 We have test user in initial data with credentials:
 *username=superadmin* and *password=superadminsuperadmin*
 Swagger doc is here: `http://localhost:8000/api-doc/` ![Hasker screenshot](https://github.com/ligain/hasker/tree/master/hasker/static/img/screenshots/Screenshot_swagger.png?raw=true "API schema screenshot")

### Obtain JWT token
Method: **POST**
```
$ curl -X POST -d "username=superadmin&password=superadminsuperadmin" "http://localhost:8000/api-token-auth/"
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE1MzUyMDk0NzUsImVtYWlsIjoic3VwZXJAZXhhbXBsZS5jb20iLCJ1c2VybmFtZSI6InN1cGVyYWRtaW4ifQ.-nG4dAQmcm-mNrlaSPZs4XT1zJpAFRZSibyzi2CBWWk"}
```
### Verify JWT token
Method: **POST**
```
$ curl -X POST -H "Authorization: JWT <jwt_token>" "http://localhost:8000/api-token-verify/"
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE1MzUyMDk0NzUsImVtYWlsIjoic3VwZXJAZXhhbXBsZS5jb20iLCJ1c2VybmFtZSI6InN1cGVyYWRtaW4ifQ.-nG4dAQmcm-mNrlaSPZs4XT1zJpAFRZSibyzi2CBWWk"}
```
### Get a question by slug
Method: **GET**
```
$ curl -H "Authorization: JWT <jwt_token>" http://localhost:8000/api/v1/questions/<question_slug>
{
	"title": "Pass data from class select to get route",
	"text": "how can I pass data from this form to my route?",
	"slug": "pass-data-from-class-select-to-get-route",
	"tags": ["html", "laravel", "href"],
	"author": "Flamms",
	"created_at": "2018-08-17T17:40:32.942332Z",
	"rating": -1,
	"answers": 1
}
```
### Get answers for a question
Method: **GET**
```
$ curl -H "Authorization: JWT <jwt_token>" http://localhost:8000/api/v1/questions/<question_slug>/answers
{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [{
		"text": "You can use request() method to fetch form data without any class dependencies.\r\n\r\nFor example: request()->id;",
		"author": "AqibBangash",
		"created_at": "2018-08-17T17:41:44.223005Z",
		"rating": 1
	}]
}
```
### Trending questions
Method: **GET**
```
$ curl -H "Authorization: JWT <jwt_token>" http://localhost:8000/api/v1/trending/
{
	"count": 7,
	"next": "http://localhost:8000/api/v1/trending/?page=2",
	"previous": null,
	"results": [{
		"title": "How does * operator work in python",
		"rating": 4
	}, {
		"title": "Create JSON file and display",
		"rating": 3
	}]
}
```
### Questions from main page sorted by date
From newest to oldest
Method: **GET**
```
$ curl -H "Authorization: JWT <jwt_token>" http://localhost:8000/api/v1/main-page/
{
	"count": 7,
	"next": "http://localhost:8000/api/v1/main-page/?page=2",
	"previous": null,
	"results": [{
		"title": "Pass data from class select to get route",
		"text": "how can I pass data from this form to my route?",
		"slug": "pass-data-from-class-select-to-get-route",
		"tags": ["html", "laravel", "href"],
		"author": "Flamms",
		"created_at": "2018-08-17T17:40:32.942332Z",
		"rating": -1,
		"answers": 1
	}, {
		"title": "Making a Python Quiz",
		"text": "I'm doing a project that is a quiz filling the gaps and I'm having an error and I can not identify. After I fail to respond to a gap, the quiz does not show the phrase that should appear and an error appears. Can someone help me? I have tried some things and nothing happens, always when an attempt to hit is wrong it shows the error instead of showing the amount of attempts that the player still has or that he has lost. Follow the code: PS: The code is in PT_BR",
		"slug": "making-a-python-quiz",
		"tags": ["python"],
		"author": "AqibBangash",
		"created_at": "2018-08-17T17:35:45.115729Z",
		"rating": 0,
		"answers": 1
	}]
}
```
### Questions from main page sorted by rating
Method: **GET**
```
$ curl -H "Authorization: JWT <jwt_token>" http://localhost:8000/api/v1/main-page/?order_by=hot
{
	"count": 7,
	"next": "http://localhost:8000/api/v1/main-page/?order_by=hot&page=2",
	"previous": null,
	"results": [{
		"title": "How does * operator work in python",
		"text": "I know that it expands function arguments, but if I try something like this in Python 2.\r\nSo it appears that I am missing something about what * exactly does?",
		"slug": "how-does-operator-work-in-python",
		"tags": ["python", "python-2"],
		"author": "superadmin",
		"created_at": "2018-08-17T17:29:10.546532Z",
		"rating": 4,
		"answers": 1
	}, {
		"title": "Create JSON file and display",
		"text": "I want to create a JSON file based in MySQL data but for some reasons my code is not working at all(I dont have any errors)",
		"slug": "create-json-file-and-display",
		"tags": ["php", "mysql", "json", "mysqli"],
		"author": "AqibBangash",
		"created_at": "2018-08-17T17:35:07.554539Z",
		"rating": 3,
		"answers": 1
	}]
}
```
### Search all questions with specific tag
Method: **GET**
```
$ curl -H "Authorization: JWT <jwt_token>" http://localhost:8000/api/v1/search/tag/<question_tag>
{
	"count": 3,
	"next": "http://localhost:8000/api/v1/search/tag/python?page=2",
	"previous": null,
	"results": [{
		"title": "Add time delay in every step of python code",
		"text": "Is there an easy way to execute time delay (like time.sleep(2)) between every line of Python code without having to explicitly write it in every line of code?",
		"slug": "add-time-delay-in-every-step-of-python-code",
		"tags": ["python"],
		"author": "superadmin",
		"created_at": "2018-08-15T20:16:33.493824Z",
		"rating": -2,
		"answers": 1
	}, {
		"title": "How does * operator work in python",
		"text": "I know that it expands function arguments, but if I try something like this in Python 2.\r\nSo it appears that I am missing something about what * exactly does?",
		"slug": "how-does-operator-work-in-python",
		"tags": ["python", "python-2"],
		"author": "superadmin",
		"created_at": "2018-08-17T17:29:10.546532Z",
		"rating": 4,
		"answers": 1
	}]
}
```
### Search all questions by string
It will be looking \<search_string\> in title and question text body.
Method: **GET**
```
$ curl -H "Authorization: JWT <jwt_token>" http://localhost:8000/api/v1/search/tag/<search_string>
{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [{
		"title": "Pass data from class select to get route",
		"text": "how can I pass data from this form to my route?",
		"slug": "pass-data-from-class-select-to-get-route",
		"tags": ["html", "laravel", "href"],
		"author": "Flamms",
		"created_at": "2018-08-17T17:40:32.942332Z",
		"rating": -1,
		"answers": 1
	}]
}
```
## Tests
```
$ ./manage.py tests
```
### Project Goals
The code is written for educational purposes.