class TestEx10:
    def test_userInput(self):
        phrase = input("Set a phrase less than 15 symbols: ")
        assert len(phrase) < 15, "length of phrase bigger of 15 symbols"


