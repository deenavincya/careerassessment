from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'deenavincya@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'eiievgfwznzlwija'        # App Password
app.config['MAIL_DEFAULT_SENDER'] = 'jajeeva915@gmail.com'

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    age = request.form.get('age')
    education = request.form.get('education')
    field_of_study = request.form.get('field_of_study')

    # Collect Interests
    interest_areas = [
        'Technology & Programming',
        'Healthcare & Medicine',
        'Business & Finance',
        'Arts & Creative Fields',
        'Education & Training',
        'Science & Research'
    ]
    interests = []
    for i, area in enumerate(interest_areas, start=1):
        score = int(request.form.get(f'interest_{i}', 0))
        interests.append({'name': area, 'score': score})

    # Top 3 Interests
    top_interests = sorted(interests, key=lambda x: x['score'], reverse=True)[:3]

    # Collect Skills
    skills_list = [
        'Problem Solving & Critical Thinking',
        'Communication & Leadership',
        'Technical & Analytical Skills',
        'Creativity & Innovation'
    ]
    skills = []
    for i, skill in enumerate(skills_list, start=1):
        score = int(request.form.get(f'skill_{i}', 0))
        skills.append({'name': skill, 'score': score})

    strong_skills = sorted(skills, key=lambda x: x['score'], reverse=True)[:3]

    # Work preferences
    work_env = request.form.get('work_environment')
    team_size = request.form.get('team_size')
    work_schedule = request.form.get('work_schedule')

    # Motivations
    motivations = request.form.getlist('motivations')

    # Additional info
    experience = request.form.get('experience')
    career_goals = request.form.get('career_goals')
    constraints = request.form.get('constraints')

    # Dummy personality analysis (you can change it)
    personality = {
        "Innovative": 75,
        "Team Player": 85,
        "Strategic Thinker": 65
    }

    # Dummy career matches (based on interests and skills)
    career_matches = [
        {
            "title": "Software Developer",
            "match_percent": 90,
            "description": "Develops applications and systems using programming skills.",
            "traits": ["Analytical Thinking", "Creativity", "Problem Solving"]
        },
        {
            "title": "Data Analyst",
            "match_percent": 82,
            "description": "Analyzes data to derive business insights and trends.",
            "traits": ["Technical Skills", "Curiosity", "Logic"]
        },
        {
            "title": "Project Manager",
            "match_percent": 78,
            "description": "Manages project planning, execution, and team coordination.",
            "traits": ["Leadership", "Time Management", "Team Coordination"]
        }
    ]

    # Recommendations
    recommendations = [
        {"title": "Improve Communication", "description": "Join a speaking club or take an online course."},
        {"title": "Build a Portfolio", "description": "Start personal or open-source projects to showcase your skills."},
        {"title": "Networking", "description": "Connect with professionals on LinkedIn or join career events."}
    ]

    data = {
        "name": name,
        "age": age,
        "education": education,
        "field_of_study": field_of_study,
        "top_interests": top_interests,
        "strong_skills": strong_skills,
        "personality": personality,
        "career_matches": career_matches,
        "motivations": motivations,
        "experience": experience,
        "career_goals": career_goals,
        "constraints": constraints,
        "recommendations": recommendations
    }

    # Send email to HR
    try:
        msg = Message("New Career Assessment Submitted", recipients=['jajeeva915@gmail.com'])
        msg.body = f"""
        A new career assessment has been submitted.

        Name: {name}
        Age: {age}
        Education: {education}
        Field of Study: {field_of_study}
        Top Interests: {[i['name'] for i in top_interests]}
        Strong Skills: {[s['name'] for s in strong_skills]}
        Career Goals: {career_goals}
        Motivations: {', '.join(motivations)}
        """
        mail.send(msg)
        print("Email sent successfully to HR.")
    except Exception as e:
        print(f"Failed to send email: {e}")

    return render_template("report.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)