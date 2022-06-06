
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


### Additional Features I Would Add If I Had More Time


* Pagination
  * Currently, the application becomes much less responsive when broad searches are made and thousands of results are surfaced.
  * The slowdown is largely driven clientside by the time taken to render results.
  * Pagination would allow us to only serve dozens of results in a single page. Maintaining responsiveness.

* User specific reading list. This could be added by
  * Implementing user authentication (via a third party identity provider like Google to reduce user friction + dev work)+ surface reading list per user.
  * Or storing a reading list object per user in their browsers local storage. 
  * It would be useful to better understand how the application is used. Shared reading lists (for example from within a single research team) might actually be a useful feature!


* Prevent the same paper being added to the same reading list twice.
  * This could be done by adding a short validation function on the frontend checking the id of the paper to be added against the papers currently added.

* Elasticsearch integration
    * I went with a basic SQL query approach due to time constraints.
    * The more relevant the search results are the more usable the application becomes
    * In a production app I would be leaning towards using a third party search tool.
      * Search + NLP is a very deep domain. Makes sense to leverage expertise of others and use existing tools vs building a new one from scratch.
  
    * Elasticsearch seems like one such option. It offers:
      * Support for the construction more advanced search filters + generation of more sophisticated results.
      * Improved search times + capacity for scaling vs current approach (Although this not a bottleneck currently)
      
* Caching of search results via flask-cache.
    * Caching would help improve response times on the search endpoint
    * Flask-caching offers an easy-to-use implementation
    * Only GET request are made to this endpoint and the underlying data queried is likely to change infrequently (daily rather than every few seconds!)
    * Cache can just be invalidated each time we manually update the dataset
    * Caching would therefore represent a relatively quick and easy way of improving API responsiveness + overall UX

    