import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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


def export_to_pdf(user_activity):
    # create a PDF file
    pdf = canvas.Canvas(
        f"report_{user_activity['first_name']}{user_activity['last_name']}.pdf",
        pagesize=letter,
    )
    width, height = letter

    main_title = f"Activity Report for user {user_activity['first_name']} {user_activity['last_name']}"

    # Title
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width / 2, height - 50, main_title)

    # Define sections (dates for past days activities)
    sections = {}
    for date, activity_list in user_activity["activities"].items():
        sections[date] = []

        for activity_entry in activity_list:
            time, activity_name = activity_entry.split(" - ")  # Extract time & name
            sections[date].append({"time": time, "name": activity_name})

    y_position = height - 100  # Start below the title

    for section, activity_list in sections.items():
        # Convert date to string
        section_str = str(section)

        # Add subsection title (Bold)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100, y_position, section_str)
        y_position -= 20  # Move down for text

        # Add activities
        pdf.setFont("Helvetica", 12)

        for activity in activity_list:
            activity_text = f"{activity['time']} - {activity['name']}"
            pdf.drawString(120, y_position, activity_text)
            y_position -= 20

        y_position -= 20

    # Save the PDF
    pdf.save()
