class SprintType:
    THIRTYDAYS = "30d"
    SEVENDAYS = "7d"

    @classmethod
    def choices(cls):
        return [
            cls.THIRTYDAYS,
            cls.SEVENDAYS,
        ]