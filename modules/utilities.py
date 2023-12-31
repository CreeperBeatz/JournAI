from enum import Enum


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
