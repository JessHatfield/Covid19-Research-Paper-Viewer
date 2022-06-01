import os
import unittest

from search_api.api import create_app, db
from search_api.app.models import PaperStore, PaperSchema, ReadingList, ReadingListSchema


class TestConfig():
    print(os.getcwd())
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), 'api.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_DOMAIN = "http://127.0.0.1:5000"


class AddItemToReadingList(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app = self.app.test_client()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_api_request_missing_required_keys(self) -> None:
        result = self.app.post(f'{TestConfig.API_DOMAIN}/api/v1/reading_list')
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.json['message'], 'Request Body Is Missing One Or More Required Keys')

    def test_add_single_item_to_reading_list(self) -> None:
        result = self.app.post(f'{TestConfig.API_DOMAIN}/api/v1/reading_list',
                               json={"title": "Coronaviruses in Balkan nephritis",
                                     "paper_url": "https://doi.org/10.1016/0002-8703(80)90355-5"},
                               follow_redirects=True)
        self.assertEqual(result.status_code, 200)

        # check that reading list item now exists in database

        reading_list_in_db = ReadingList.query.filter(ReadingList.title == "Coronaviruses in Balkan nephritis").all()
        self.assertEqual(len(reading_list_in_db), 1)
        self.assertEqual(reading_list_in_db[0].id, 1)
        self.assertEqual(reading_list_in_db[0].title, "Coronaviruses in Balkan nephritis")
        self.assertEqual(reading_list_in_db[0].paper_url, "https://doi.org/10.1016/0002-8703(80)90355-5")


class GetReadingListAPITests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app = self.app.test_client()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_no_reading_list_items_found(self):
        search_result = self.app.get(f'{TestConfig.API_DOMAIN}/api/v1/reading_list')
        self.assertEqual(search_result.status_code, 200)
        self.assertEqual(search_result.json, [])

    def test_single_reading_list_item_found(self):
        reading_list_item = ReadingList(title="Coronaviruses in Balkan nephritis",
                                        paper_url="https://doi.org/10.1016/0002-8703(80)90355-5")
        db.session.add(reading_list_item)
        db.session.commit()

        search_result = self.app.get(f'{TestConfig.API_DOMAIN}/api/v1/reading_list')
        self.assertEqual(search_result.json, [ReadingListSchema().dump(reading_list_item)])

    def test_multiple_reading_list_item_found(self):
        reading_list_items = [ReadingList(title="Coronaviruses in Balkan nephritis",
                                          paper_url="https://doi.org/10.1016/0002-8703(80)90355-5"), ReadingList(
            title="Predict7, a program for protein structure prediction",
            paper_url="https://doi.org/10.1016/0006-291x(89)90049-1")]

        db.session.add_all(reading_list_items)
        db.session.commit()

        search_result = self.app.get(f'{TestConfig.API_DOMAIN}/api/v1/reading_list')
        self.assertEqual(search_result.json, ReadingListSchema(many=True).dump(reading_list_items))


class PaperSearchAPITests(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app = self.app.test_client()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_no_results_found(self):
        search_result = self.app.get(f'{TestConfig.API_DOMAIN}/api/v1/search?search_term=balkan nephritis')
        self.assertEqual(search_result.status_code, 200)
        self.assertEqual(search_result.json, [])

    def test_paper_title_can_be_searched(self):
        # the first paper should be retrieved as the string Balkan Nephritis only exists within the first paper

        paper_to_retrieve = PaperStore(title="Coronaviruses in Balkan nephritis", journal="American Heart Journal",
                                       authors="Georgescu, Leonida; Diosi, Peter; Buţiu, Ioan; Plavoşin, Livia; Herzog, Georgeta",
                                       paper_url="https://doi.org/10.1016/0002-8703(80)90355-5",
                                       publish_date="1980-03-31",
                                       abstract="This is a journal article that explores coronaviruses in balkan nephritis")

        paper_to_ignore = PaperStore(title="Predict7, a program for protein structure prediction",
                                     journal="Biochemical and Biophysical Research Communications",
                                     authors="Cármenes, R.S.; Freije, J.P.; Molina, M.M.; Martín, J.M.",
                                     paper_url="https://doi.org/10.1016/0006-291x(89)90049-1",
                                     publish_date="1989-03-15",
                                     abstract="This is a journal article that explores protein structure prediction in coronaviruses")

        db.session.add_all([paper_to_retrieve, paper_to_ignore])
        db.session.commit()

        search_result = self.app.get(f'{TestConfig.API_DOMAIN}/api/v1/search?search_term=balkan nephritis')

        # because we have separate tests to confirm the exact structure of the JSON produces by PaperSchema. We can use the Schema class to auto generate the result to assert agaisnt vs using hardcoded list of dicts!

        self.assertEqual(search_result.json, [PaperSchema().dump(paper_to_retrieve)])

    def test_paper_authors_can_be_searched(self):
        paper_to_ignore = PaperStore(title="Coronaviruses in Balkan nephritis", journal="American Heart Journal",
                                     authors="Georgescu, Leonida; Diosi, Peter; Buţiu, Ioan; Plavoşin, Livia; Herzog, Georgeta",
                                     paper_url="https://doi.org/10.1016/0002-8703(80)90355-5",
                                     publish_date="1980-03-31")

        paper_to_retrieve = PaperStore(title="Predict7, a program for protein structure prediction",
                                       journal="Biochemical and Biophysical Research Communications",
                                       authors="Cármenes, R.S.; Freije, J.P.; Molina, M.M.; Martín, J.M.",
                                       paper_url="https://doi.org/10.1016/0006-291x(89)90049-1",
                                       publish_date="1989-03-15")

        db.session.add_all([paper_to_retrieve, paper_to_ignore])
        db.session.commit()

        search_result = self.app.get(f'{TestConfig.API_DOMAIN}/api/v1/search?search_term=cármenes, r.s')

        self.assertEqual(search_result.json, [PaperSchema().dump(paper_to_retrieve)])

    def test_paper_journal_name_can_be_searched(self):
        paper_to_ignore = PaperStore(title="Coronaviruses in Balkan nephritis", journal="American Heart Journal",
                                     authors="Georgescu, Leonida; Diosi, Peter; Buţiu, Ioan; Plavoşin, Livia; Herzog, Georgeta",
                                     paper_url="https://doi.org/10.1016/0002-8703(80)90355-5",
                                     publish_date="1980-03-31")

        paper_to_retrieve = PaperStore(title="Predict7, a program for protein structure prediction",
                                       journal="Biochemical and Biophysical Research Communications",
                                       authors="Cármenes, R.S.; Freije, J.P.; Molina, M.M.; Martín, J.M.",
                                       paper_url="https://doi.org/10.1016/0006-291x(89)90049-1",
                                       publish_date="1989-03-15")

        db.session.add_all([paper_to_retrieve, paper_to_ignore])
        db.session.commit()

        search_result = self.app.get(f'{TestConfig.API_DOMAIN}/api/v1/search?search_term=Biochemical and Biophysical Research Communications')

        self.assertEqual(search_result.json, [PaperSchema().dump(paper_to_retrieve)])

    def test_paper_abstract_can_be_searched(self):
        # Both papers have coronvavirus in their abstract and nowhere else and both should be retrieved as a result

        paper_1 = PaperStore(title="New Viruses in Balkan nephritis", journal="American Heart Journal",
                             authors="Georgescu, Leonida; Diosi, Peter; Buţiu, Ioan; Plavoşin, Livia; Herzog, Georgeta",
                             paper_url="https://doi.org/10.1016/0002-8703(80)90355-5", publish_date="1980-03-31",
                             abstract="This paper explores coronaviruses in balkan nephritis")

        paper_2 = PaperStore(title="Predict7, a program for protein structure prediction",
                             journal="Biochemical and Biophysical Research Communications",
                             authors="Cármenes, R.S.; Freije, J.P.; Molina, M.M.; Martín, J.M.",
                             paper_url="https://doi.org/10.1016/0006-291x(89)90049-1", publish_date="1989-03-15",
                             abstract="This paper explores for coronaviruses")

        db.session.add_all([paper_1, paper_2])
        db.session.commit()

        search_result = self.app.get(f'{TestConfig.API_DOMAIN}/api/v1/search?search_term=coronavirus')

        self.assertEqual(search_result.json, PaperSchema(many=True).dump([paper_1, paper_2]))


if __name__ == "__main__":
    unittest.main()
