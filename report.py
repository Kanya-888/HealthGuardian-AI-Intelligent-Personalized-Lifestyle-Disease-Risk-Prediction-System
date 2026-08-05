from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
    filename,
    age,
    gender,
    bmi,
    health_score,
    risk,
    calories,
    water,
    diet,
    exercise
):

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(filename)

    story = []

    story.append(Paragraph("<b>HealthGuardian AI Report</b>", styles["Title"]))

    story.append(Paragraph(f"<b>Age:</b> {age}", styles["Normal"]))
    story.append(Paragraph(f"<b>Gender:</b> {gender}", styles["Normal"]))

    story.append(Paragraph(f"<b>BMI:</b> {bmi}", styles["Normal"]))

    story.append(
        Paragraph(f"<b>Health Score:</b> {health_score}/100", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Diabetes Risk:</b> {risk:.2f}%", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Daily Calories:</b> {calories} kcal", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Water Intake:</b> {water} L", styles["Normal"])
    )

    story.append(Paragraph("<b>Diet Recommendations</b>", styles["Heading2"]))

    for item in diet:
        story.append(Paragraph(item, styles["Normal"]))

    story.append(Paragraph("<b>Exercise Recommendations</b>", styles["Heading2"]))

    for item in exercise:
        story.append(Paragraph(item, styles["Normal"]))

    pdf.build(story)