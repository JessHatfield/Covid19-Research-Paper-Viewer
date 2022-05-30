import os
import unittest

from search_api.api import create_app, db
from search_api.app.models import PaperStore, PaperSchema


class TestConfig():
    print(os.getcwd())
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), 'api.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_DOMAIN = "http://127.0.0.1:5000"


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
                                       paper_url="https://doi.org/10.1016/0002-8703(80)90355-5", publish_date="1980-03-31",
                                       abstract="This is a journal article that explores coronaviruses in balkan nephritis")

        paper_to_ignore = PaperStore(title="Predict7, a program for protein structure prediction",
                                     journal="Biochemical and Biophysical Research Communications",
                                     authors="Cármenes, R.S.; Freije, J.P.; Molina, M.M.; Martín, J.M.",
                                     paper_url="https://doi.org/10.1016/0006-291x(89)90049-1", publish_date="1989-03-15",
                                     abstract="This is a journal article that explores protein structure prediction in coronaviruses")

        db.session.add_all([paper_to_retrieve, paper_to_ignore])
        db.session.commit()

        search_result = self.app.get(f'{TestConfig.API_DOMAIN}/api/v1/search?search_term=balkan nephritis')

        self.assertEqual(search_result.json, [PaperSchema().dump(paper_to_retrieve)])

    def test_paper_authors_can_be_searched(self):
        paper_to_ignore = PaperStore(title="Coronaviruses in Balkan nephritis", journal="American Heart Journal",
                                     authors="Georgescu, Leonida; Diosi, Peter; Buţiu, Ioan; Plavoşin, Livia; Herzog, Georgeta",
                                     paper_url="https://doi.org/10.1016/0002-8703(80)90355-5", publish_date="1980-03-31")

        paper_to_retrieve = PaperStore(title="Predict7, a program for protein structure prediction",
                                       journal="Biochemical and Biophysical Research Communications",
                                       authors="Cármenes, R.S.; Freije, J.P.; Molina, M.M.; Martín, J.M.",
                                       paper_url="https://doi.org/10.1016/0006-291x(89)90049-1", publish_date="1989-03-15")

        db.session.add_all([paper_to_retrieve, paper_to_ignore])
        db.session.commit()

        search_result = self.app.get(f'{TestConfig.API_DOMAIN}/api/v1/search?search_term=cármenes, r.s')

        self.assertEqual(search_result.json, [PaperSchema().dump(paper_to_retrieve)])

    def test_paper_abstract_can_be_searched(self):
        # Both papers have coronvavirus in their abstract and nowhere else and should be retrieved as a result

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
