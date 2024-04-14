from enum import Enum

from model.textdoc import TextDoc


# Enum wrapper
class ExtendedEnum(Enum):
    """
    Wrapper for the Enum class that includes a function to return a list of the possible enum values.
    """

    @classmethod
    def values(cls):
        """
        Returns a list of the possible enum values.

        Returns:
            array_like: List of the possible enum values.
        """
        return list(map(lambda c: c.value, cls))


def sanitize_filename(filename):
    invalid_characters = "<>:\"/\\|?*\0"
    for char in invalid_characters:
        filename = filename.replace(char, "")
    return filename


def context_as_system_message(similar_docs: list[TextDoc]) -> str:
    system_message = ("You remember the following conversations you had with the user, based on"
                      "their query. If empty, there is no context. Keep in mind that the context"
                      "might not always be relevant:\n")
    for doc in similar_docs:
        system_message += f"{doc.date}: {doc.text}\n"
    return system_message
