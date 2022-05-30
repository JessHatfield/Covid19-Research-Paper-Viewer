import unittest

from search_api.api import create_app, db

from search_api.app.models import PaperStore, PaperSchema, ReadingList, ReadingListSchema


# Contains tests for PaperSchema Serializer class which determine which fields for the PaperStore Model are returned via API and those fields are formatted

class ReadlistSchemaTests(unittest.TestCase):
    def test_can_serialize_single_reading_list_item(self):
        reading_list_item_to_serialize = ReadingList(id=1, title="Coronaviruses in Balkan nephritis",
                                                     paper_url="https://doi.org/10.1016/0002-8703(80)90355-5")

        expected_result = ReadingListSchema().dump(reading_list_item_to_serialize)

        self.assertEqual(expected_result, {'paper_url': 'https://doi.org/10.1016/0002-8703(80)90355-5', 'id': '1',
                                           'title': 'Coronaviruses in Balkan nephritis'})
        #

    def test_can_serialize_multiple_reading_list_item(self):
        reading_list_items_to_serialize = [ReadingList(id=1, title="Coronaviruses in Balkan nephritis",
                                                       paper_url="https://doi.org/10.1016/0002-8703(80)90355-5"),
                                           ReadingList(id=2,
                                                       title="Predict7, a program for protein structure prediction",
                                                       paper_url="https://doi.org/10.1016/0006-291x(89)90049-1")]

        expected_result = ReadingListSchema(many=True).dump(reading_list_items_to_serialize)

        self.assertEqual(expected_result, [{'paper_url': 'https://doi.org/10.1016/0002-8703(80)90355-5', 'id': '1', 'title': 'Coronaviruses in Balkan nephritis'}, {'paper_url': 'https://doi.org/10.1016/0006-291x(89)90049-1', 'id': '2', 'title': 'Predict7, a program for protein structure prediction'}])


class PaperSchemaTests(unittest.TestCase):

    def test_can_serialize_single_paper(self):
        paper_to_serialize = PaperStore(id=1, title="Coronaviruses in Balkan nephritis",
                                        journal="American Heart Journal",
                                        authors="Georgescu, Leonida; Diosi, Peter; Buţiu, Ioan; Plavoşin, Livia; Herzog, Georgeta",
                                        paper_url="https://doi.org/10.1016/0002-8703(80)90355-5",
                                        publish_date="1980-03-31",
                                        abstract="This is a journal article that explores coronaviruses in balkan nephritis")

        expected_result = PaperSchema().dump(paper_to_serialize)

        self.assertEqual({'publish_date': '1980-03-31',
                          'authors': 'Georgescu, Leonida; Diosi, Peter; Buţiu, Ioan; Plavoşin, Livia; Herzog, Georgeta',
                          'title': 'Coronaviruses in Balkan nephritis', 'id': '1',
                          'paper_url': 'https://doi.org/10.1016/0002-8703(80)90355-5',
                          'abstract': 'This is a journal article that explores coronaviruses in balkan nephritis',
                          'journal': 'American Heart Journal'}, expected_result)  # add assertion here

    def test_can_serialize_multiple_papers(self):
        papers_to_serialize = [
            PaperStore(id=1, title="Coronaviruses in Balkan nephritis", journal="American Heart Journal",
                       authors="Georgescu, Leonida; Diosi, Peter; Buţiu, Ioan; Plavoşin, Livia; Herzog, Georgeta",
                       paper_url="https://doi.org/10.1016/0002-8703(80)90355-5",
                       publish_date="1980-03-31",
                       abstract="This is a journal article that explores coronaviruses in balkan nephritis"),
            PaperStore(id=2, title="Predict7, a program for protein structure prediction",
                       journal="Biochemical and Biophysical Research Communications",
                       authors="Cármenes, R.S.; Freije, J.P.; Molina, M.M.; Martín, J.M.",
                       paper_url="https://doi.org/10.1016/0006-291x(89)90049-1",
                       publish_date="1989-03-15",
                       abstract="This is a journal article that explores protein structure prediction in coronaviruses")
        ]

        expected_result = PaperSchema(many=True).dump(papers_to_serialize)
        self.assertEqual([{'title': 'Coronaviruses in Balkan nephritis', 'publish_date': '1980-03-31',
                           'paper_url': 'https://doi.org/10.1016/0002-8703(80)90355-5',
                           'journal': 'American Heart Journal',
                           'authors': 'Georgescu, Leonida; Diosi, Peter; Buţiu, Ioan; Plavoşin, Livia; Herzog, Georgeta',
                           'id': '1',
                           'abstract': 'This is a journal article that explores coronaviruses in balkan nephritis'},
                          {'title': 'Predict7, a program for protein structure prediction',
                           'publish_date': '1989-03-15', 'paper_url': 'https://doi.org/10.1016/0006-291x(89)90049-1',
                           'journal': 'Biochemical and Biophysical Research Communications',
                           'authors': 'Cármenes, R.S.; Freije, J.P.; Molina, M.M.; Martín, J.M.', 'id': '2',
                           'abstract': 'This is a journal article that explores protein structure prediction in coronaviruses'}],
                         expected_result)


if __name__ == '__main__':
    unittest.main()
