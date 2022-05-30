from search_api.api import db, ma


class PaperSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'publish_date', 'journal', 'authors', 'paper_url', 'abstract')

    id = ma.String()
    title = ma.String()
    publish_date = ma.String()
    journal = ma.String()
    authors = ma.String()
    paper_url = ma.String()
    abstract = ma.String()


class ReadingListSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'paper_url')

    id = ma.String()
    title = ma.String()
    paper_url = ma.String()


class ReadingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    paper_url = db.Column(db.Text)


class PaperStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    # dtype depends on db used

    # ignore timezones for now - Most papers published more than one day ago
    # should be in yyyy-mm-dd format e.g 1980-03-31
    publish_date = db.Column(db.Text)
    journal = db.Column(db.Text)
    authors = db.Column(db.Text)
    paper_url = db.Column(db.Text)
    abstract = db.Column(db.Text)
