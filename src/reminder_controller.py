from models.Reminder import Reminder
from utils.database import PostgreSQLDatabase


def add_reminder(title, description, date, time):
    """
    Create and add a new reminder

    Args:
        title (str): The title of the reminder
        description (str): The description of the reminder
        date (str): The date of the reminder
        time (str): The time of the reminder

    Returns:
        None
    """
    
def get_all_future_reminders():
    """
    Get all future reminders

    Returns:
        list: A list of all future reminders
    """

    database = PostgreSQLDatabase()
    cursor = database.get_cursor()
    cursor.execute("SELECT * FROM reminders WHERE date > CURRENT_DATE")
    reminders = cursor.fetchall()
    cursor.close()
    database.close()

    return [Reminder(row[0], row[1], row[2], row[3]) for row in reminders]

def get_reminder_by_date_and_time_range(start_date, start_time, end_date, end_time):
    """
    Get reminders within a specific date and time range

    Args:
        start_date (str): The start date of the date and time range
        start_time (str): The start time of the date and time range
        end_date (str): The end date of the date and time range
        end_time (str): The end time of the date and time range

    Returns:
        list: A list of reminders within the date and time range
    """
    return []