import csv


from sqlalchemy import create_engine

from search_api.api import create_app, db
from search_api.app.models import PaperStore
from search_api.config import Config


#A short script to load the contents of the metadata.csv file into our SQLlite Database

# Create the Sqlite DB

app = create_app(Config)
app_context = app.app_context()
app_context.push()
app = app.test_client()
db.create_all()

# Read in Metadata.csv

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

papers_to_insert = []

with open("search_api/app/metadata.csv", "r") as metadata_file:
    reader = csv.DictReader(metadata_file)

    for row in reader:
        new_paper = PaperStore(title=row['title'], journal=row['journal'], authors=row['authors'],
                               publish_date=row['publish_time'], abstract=row['abstract'], paper_url=row['url'])

        papers_to_insert.append(new_paper)

db.session.bulk_save_objects(papers_to_insert)
db.session.commit()
exit()


