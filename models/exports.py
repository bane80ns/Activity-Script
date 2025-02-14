import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def export_to_json(user_data):
    if "message" in user_data:
        print(user_data["message"])
        return

    # Convert datetime.date to string (YYYY-MM-DD)
    if "activities" in user_data:
        new_activities = {}
        for day, activities in user_data["activities"].items():
            new_activities[str(day)] = activities
        user_data["activities"] = new_activities

    # Make filename from user first and last name
    filename = f"user_{user_data['first_name']}{user_data['last_name']}_activities.json"

    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(user_data, json_file, indent=4, ensure_ascii=False)

    print(f"Data successfully exported to {filename}")

# user_activity = activity_details_for_single_user_by_day(db, 1, 30)  # Fetch user data
# export_to_json(user_activity)


class PdfExporter:
    def __init__(self, user_activity):
        self.user_activity = user_activity
        self.filename = f"user_{user_activity['first_name']}{user_activity['last_name']}_activities.pdf"
        self.width, self.height = letter
        self.pdf = canvas.Canvas(self.filename, pagesize = letter)


    def add_title_pdf(self):
        main_title = f"Activity Report for user {self.user_activity['first_name']} {self.user_activity['last_name']}"
        self.pdf.setFont("Helvetica-Bold", 18)
        self.pdf.drawCentredString(self.width / 2, self.height - 50, main_title)


    def add_activities_pdf(self):
        sections = {}

        for date, activity_list in self.user_activity["activities"].items():
            sections[date] = []

            for activity_entry in activity_list:
                time, activity_name = activity_entry.split(" - ")
                sections[date].append({"time": time, "name": activity_name})

        y_position = self.height - 100  # Start below the title

        for section, activity_list in sections.items():
            section_str = str(section)
            self.pdf.setFont("Helvetica-Bold", 14)
            self.pdf.drawString(100, y_position, section_str)
            y_position -= 20

            self.pdf.setFont("Helvetica", 12)

            for activity in activity_list:
                activity_text = f"{activity['time']} - {activity['name']}"
                self.pdf.drawString(120, y_position, activity_text)
                y_position -= 20

            y_position -= 20

    def save_to_pdf(self):
        self.pdf.save()


    def generate_report(self):
        self.add_title_pdf()
        self.add_activities_pdf()
        self.save_to_pdf()

# def export_to_pdf(user_activity):
#     # create a PDF file
#     pdf = canvas.Canvas(
#         f"report_{user_activity['first_name']}{user_activity['last_name']}.pdf",
#         pagesize=letter,
#     )
#     width, height = letter
#
#     main_title = f"Activity Report for user {user_activity['first_name']} {user_activity['last_name']}"
#
#     # Title
#     pdf.setFont("Helvetica-Bold", 18)
#     pdf.drawCentredString(width / 2, height - 50, main_title)
#
#     # Define sections (dates for past days activities)
#     sections = {}
#     for date, activity_list in user_activity["activities"].items():
#         sections[date] = []
#
#         for activity_entry in activity_list:
#             time, activity_name = activity_entry.split(" - ")  # Extract time & name
#             sections[date].append({"time": time, "name": activity_name})
#
#     y_position = height - 100  # Start below the title
#
#     for section, activity_list in sections.items():
#         # Convert date to string
#         section_str = str(section)
#
#         # Add subsection title (Bold)
#         pdf.setFont("Helvetica-Bold", 14)
#         pdf.drawString(100, y_position, section_str)
#         y_position -= 20  # Move down for text
#
#         # Add activities
#         pdf.setFont("Helvetica", 12)
#
#         for activity in activity_list:
#             activity_text = f"{activity['time']} - {activity['name']}"
#             pdf.drawString(120, y_position, activity_text)
#             y_position -= 20
#
#         y_position -= 20
#
#     # Save the PDF
#     pdf.save()



# Create chart from user_activities
def chart(user_activities):
    matplotlib.use("TkAgg")
    dates = []
    activity_counts = []

    for activity_date, activity_list in user_activities["activities"].items():
        dates.append(activity_date.strftime("%Y-%m-%d"))
        activity_counts.append(len(activity_list))


    plt.figure(figsize=(8, 5))  # Set figure size
    plt.bar(dates, activity_counts, color='green')  # Bar chart
    plt.xlabel("Date")  # X-axis label
    plt.ylabel("Number of Activities")  # Y-axis label
    plt.title("User Activities Over Time")  # Chart title
    plt.xticks(rotation=15)  # Rotate date labels for readability
    plt.grid(axis="y", linestyle="--", alpha=0.7)  # Add horizontal grid lines


    plt.show()