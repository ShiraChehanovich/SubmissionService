
class SubmissionStatus(str):
    NEW = "new"
    BOUND = "bound"
    BIND_FAILED = "bind_failed"

    def __eq__(self, other: str):
        return self.name == other

    def __str__(self):
        return self.name

    @classmethod
    def __contains__(cls, item):
        return any(item == member.name for member in cls)