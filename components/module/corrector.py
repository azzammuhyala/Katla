from typing import Literal as _lt

class Correction:

    """
    Correction
    ----------
    Correction of errors/typos with ratio
    """

    def __init__(self, database: list[str], similarity_threshold: float = 0.5, similarity_ratio_method: _lt['set', 'manual'] = 'manual') -> None:
        """
        `database`: Available dictionary database.
        `similarity_threshold`: Looking for a similarity threshold with minimum conditions. The lowest is 0 and the highest is 1.
        """
        self.__database = database.copy()
        self.__validation_database()
        self.similarity_threshold = similarity_threshold
        self.similarity_ratio_method = similarity_ratio_method

    @property
    def database(self) -> list[str]:
        return self.__database

    @database.setter
    def database(self, newdatabase: list[str]) -> None:
        self.__database = newdatabase.copy()
        self.__validation_database()

    def __validation_database(self) -> None:
        for item in self.__database:
            assert isinstance(item, str), 'can only database a str'

    def _create_bigrams(self, string: str) -> list[str]:
        """ create word bigrams from `string` """
        return [string[i] + string[i + 1] for i in range(len(string) - 1)]

    def get_similarity_ratio(self, string1: str, string2: str) -> float:

        """ get the similarity ratio of the two word `string` """

        match self.similarity_ratio_method:

            case 'set':
                bigram1, bigram2 = map(set, (self._create_bigrams(string1.lower().strip()), self._create_bigrams(string2.lower().strip())))
                common = bigram1 & bigram2
                return len(common) / max(len(bigram1), len(bigram2))

            case 'manual':
                string1, string2 = string1.lower().strip(), string2.lower().strip()
                bigram1, bigram2 = self._create_bigrams(string1), self._create_bigrams(string2)
                common = 0

                for item in bigram1:
                    if item in bigram2:
                        common += 1

                return common / max(len(bigram1), len(bigram2))
            
            case _:
                raise TypeError('invalid similarity_ratio_method')

    def get_most_ratio(self, string: str) -> tuple[float, str | None]:

        """ search for string values ​​from the database to be calculated by looking for possible similarities in question.
        Use valid characters in the form of letter characters (lower / upper) to make it easier and possible to get higher similarities """

        max_similarity = 0.0
        most_similarity_str = ''

        for data in self.database:
            current_similarity = self.get_similarity_ratio(string, data)

            if current_similarity > max_similarity:
                max_similarity = current_similarity
                most_similarity_str = data

        return (max_similarity, (most_similarity_str if max_similarity >= self.similarity_threshold else None))

    def get_list_most_ratio(self, string: str) -> list[tuple[float, str]] | list:

        """ looks for a string value from the database to be calculated by looking for the possibility of similarity above the probability of similarity above `similarity_threshold` """

        most_similarity = []

        for data in self.database:
            current_similarity = self.get_similarity_ratio(string, data)

            if current_similarity >= self.similarity_threshold:
                most_similarity.append((current_similarity, data))

        return most_similarity

    def get_correct(self, string: str) -> str | None:
        """ this is the same as the `get_most_ratio` method, the difference is that it only gets the similarity string """
        return self.get_most_ratio(string)[1]

    def get_list_correct(self, string: str) -> list[str] | list:
        """ this is the same as the `d` method, the difference is that it only gets a list of similar strings """
        list_ratio = self.get_list_most_ratio(string)
        return [item[1] for item in list_ratio]