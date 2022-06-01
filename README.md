
# Covid-19 Research Paper Search Tool

A small webapp to surface metadata on research papers relating to covid-19. 
Built using Flask + React.



 
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

Install python 3.6 (or greater) and nodejs (version 14.17.4 or greater)

Clone the github repository

```
git clone https://github.com/JoshHatfield/Covid19-Research-Paper-Viewer

```

Install Python Libraries 

```
cd search_api
python -m pip install requirements.txt
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

  Key User Journeys
    ✓ User Can Search For Keyword And View Results (219 ms)
    ✓ User Can View And Add Items To Reading List (348 ms)

Test Suites: 1 passed, 1 total
Tests:       2 passed, 2 total
Snapshots:   0 total
Time:        1.78 s

```

### Start The Development Server


Start the Flask API

```
export FLASK_APP=Covid19-Research-Paper-Viewer
python ./search_app/api.py
```

Start the React Dev Server

```
cd search_app
npm run start
```