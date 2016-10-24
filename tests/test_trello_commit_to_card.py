import trello_commit_to_card
import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestCase(unittest.TestCase):

    def test_search_for_card_number(self):
        self.assertEquals(
                trello_commit_to_card.search_for_card_numbers("title \n somenthing #2 and #4 msg"),
                ['2', '4'])

        self.assertEquals(
                trello_commit_to_card.search_for_card_numbers("somenthing with no linked cards"),
                [])

        self.assertEquals(
                trello_commit_to_card.search_for_card_numbers("somenthing \n about only #5 card"),
                ['5'])


if __name__ == '__main__':
    unittest.main()

