
# Covid-19 Research Paper Search Tool

A small webapp to surface metadata on research papers relating to Covid-19. 
Built using Flask + React.

Features
* User can search for a search term within research papers across Author/Title/Journal Name/Abstract fields.
* User can view search results and the Authors/Title/Journal/Publish Date/URL per paper.
* User can see the number of search results retrieved.
* User can add the paper title and url to a reading_list for later reference.


 
## Running The Application

The application has been dockerised for ease of use.


Download the docker image

```bash
docker pull joshhatfield1994/covid19_research_paper_viewer
```

Run the docker image

```bash
docker run --rm -p 5000:5000 joshhatfield1994/covid19_research_paper_viewer:latest
```

The webapp can the be viewed at http://0.0.0.0:5000.


## Developing For The Application

### Setup The Project Environment

Install python 3.6 (or greater) + pip and nodejs (version 14.17.4 or greater) + npm

Clone the github repository

```
git clone https://github.com/JoshHatfield/Covid19-Research-Paper-Viewer

```

Install Python Libraries 

```
python -m pip install -r search_api/requirements.txt
```

Install node-packages


```
cd search_app
npm install
```

### Run Tests

How to run API Integration + Schema Tests

```bash

python -m unittest search_api/tests/integration_tests.py

----------------------------------------------------------------------
Ran 9 tests in 0.399s

OK


python -m unittest search_api/tests/schema_tests.py

----------------------------------------------------------------------
Ran 4 tests in 0.002s

OK

```

How to run Frontend Integration Tests

```
cd search_app
npm test -- --watchAll=false

----------------------------------------------------------------------

  Key User Journeys
    ✓ User Can Search For Keyword And View Results (219 ms)
    ✓ User Can View And Add Items To Reading List (348 ms)

Test Suites: 1 passed, 1 total
Tests:       2 passed, 2 total
Snapshots:   0 total
Time:        1.78 s

```

### Starting The Application For Development

Setup The API Sqlite Database

```
export FLASK_APP=search_api/setup_db.py
python -m flask run

----------------------------------------------------------------------

47298 Research Papers Have Been Added To The DB
Database Setup Is Complete

```

Start The API Server
```
export FLASK_APP=search_api/api.py
python -m flask run
```

Start the React Dev Server

```
cd search_app
npm run start
```

The webapp can now be access at http://localhost:3000/