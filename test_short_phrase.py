import pytest

class TestShortPhrase:

    def test_short_phrase(self):
        phrase = input("Set a phrase ")

        expected_max_phrase_lenght = 15
        actual_phrase_lenght = len(phrase)

        assert expected_max_phrase_lenght > actual_phrase_lenght, "Actual phrase lenght is longer than expected"