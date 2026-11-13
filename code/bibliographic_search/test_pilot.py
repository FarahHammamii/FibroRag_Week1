import unittest
from pilot import dedup
class TestDedup(unittest.TestCase):
    def test_doi(self):
        items=[dict(doi='10.1/X',pmid='1',title='test',query_id='a'),dict(doi='https://doi.org/10.1/x',pmid='',title='test',query_id='b')]
        x=dedup(items);self.assertEqual(len(x),1);self.assertEqual(x[0]['query_ids'],['a','b'])
    def test_distinct(self):
        items=[dict(doi='',pmid='1',title='test',query_id='a'),dict(doi='',pmid='2',title='test',query_id='b')];self.assertEqual(len(dedup(items)),2)
if __name__=='__main__':unittest.main()
