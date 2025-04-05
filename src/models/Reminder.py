class Reminder:
    def __init__(self, title, description, date, time):
        self.title = title
        self.description = description
        self.date = date
        self.time = time

    def __str__(self):
        return f"{self.title}: {self.description} ({self.date} {self.time})"