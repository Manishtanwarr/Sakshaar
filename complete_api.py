from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "Career Guidance API is running",
        "version": "1.0"
    })

@app.route('/api/health')
def health():
    db_exists = os.path.exists('career_guidance.db')

    college_count = 0
    if db_exists:
        try:
            conn = sqlite3.connect('career_guidance.db')
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM colleges')
            college_count = cursor.fetchone()[0]
            conn.close()
        except:
            college_count = 0

    return jsonify({
        "status": "healthy" if db_exists and college_count > 0 else "initializing",
        "system_ready": db_exists and college_count > 0,
        "database_exists": db_exists,
        "colleges_loaded": college_count,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/colleges')
def get_colleges():
    try:
        # Get query parameters
        course_type = request.args.get('course_type')
        region = request.args.get('region') 
        max_fee = request.args.get('max_fee', type=int)
        limit = request.args.get('limit', default=50, type=int)

        conn = sqlite3.connect('career_guidance.db')
        cursor = conn.cursor()

        query = "SELECT * FROM colleges WHERE 1=1"
        params = []

        if course_type:
            query += " AND course_type = ?"
            params.append(course_type)

        if region:
            query += " AND region = ?"
            params.append(region)

        if max_fee:
            query += " AND avg_fee_annual <= ?"
            params.append(max_fee)

        query += f" LIMIT {limit}"

        cursor.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        conn.close()

        return jsonify({
            "status": "success",
            "count": len(results),
            "colleges": results
        })

    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500

@app.route('/api/assessment/start', methods=['POST'])
def start_assessment():
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id') or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"

        # RIASEC Questions
        riasec_questions = [
            {"id": "R1", "type": "R", "question": "I enjoy working with tools and machines"},
            {"id": "I1", "type": "I", "question": "I like to analyze data and solve complex problems"},
            {"id": "A1", "type": "A", "question": "I enjoy creative activities like art or writing"},
            {"id": "S1", "type": "S", "question": "I like helping others solve their problems"},
            {"id": "E1", "type": "E", "question": "I enjoy leading and managing others"},
            {"id": "C1", "type": "C", "question": "I like organizing data and keeping detailed records"},
            {"id": "R2", "type": "R", "question": "I prefer hands-on, practical work"},
            {"id": "I2", "type": "I", "question": "I enjoy scientific experiments and research"},
            {"id": "A2", "type": "A", "question": "I like to express myself creatively"},
            {"id": "S2", "type": "S", "question": "I enjoy teaching and training people"},
            {"id": "E2", "type": "E", "question": "I like to persuade and influence others"},
            {"id": "C2", "type": "C", "question": "I prefer structured, well-defined tasks"},
            {"id": "R3", "type": "R", "question": "I like working outdoors"},
            {"id": "I3", "type": "I", "question": "I enjoy reading scientific journals"},
            {"id": "A3", "type": "A", "question": "I like attending art exhibitions"},
            {"id": "S3", "type": "S", "question": "I enjoy volunteering for good causes"},
            {"id": "E3", "type": "E", "question": "I like starting new businesses or projects"},
            {"id": "C3", "type": "C", "question": "I prefer following established procedures"},
            {"id": "R4", "type": "R", "question": "I enjoy building or fixing things"},
            {"id": "I4", "type": "I", "question": "I like theoretical discussions"},
            {"id": "A4", "type": "A", "question": "I enjoy music and performing arts"},
            {"id": "S4", "type": "S", "question": "I like counseling people with problems"},
            {"id": "E4", "type": "E", "question": "I enjoy making sales presentations"},
            {"id": "C4", "type": "C", "question": "I like keeping accurate records"},
            {"id": "R5", "type": "R", "question": "I prefer working with my hands"},
            {"id": "I5", "type": "I", "question": "I enjoy conducting research"},
            {"id": "A5", "type": "A", "question": "I like designing things"},
            {"id": "S5", "type": "S", "question": "I enjoy working with children"},
            {"id": "E5", "type": "E", "question": "I like managing people and projects"},
            {"id": "C5", "type": "C", "question": "I prefer routine, predictable work"}
        ]

        # Quiz Questions
        quiz_questions = [
            {
                "id": "academic_performance",
                "question": "What is your average academic percentage?",
                "type": "numeric",
                "range": [40, 100]
            },
            {
                "id": "course_preference", 
                "question": "Which course type interests you most?",
                "type": "single_choice",
                "options": {
                    "engineering": "Engineering (B.Tech)",
                    "medical": "Medical (MBBS)",  
                    "commerce": "Commerce (B.Com)",
                    "arts": "Arts (BA)",
                    "science": "Science (B.Sc)",
                    "management": "Management (BBA)",
                    "pharmacy": "Pharmacy (B.Pharm)"
                }
            }
        ]

        return jsonify({
            "status": "success",
            "session_id": session_id,
            "riasec_questions": riasec_questions,
            "quiz_questions": quiz_questions
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/assessment/submit', methods=['POST'])
def submit_assessment():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        session_id = data.get('session_id')
        responses = data.get('responses', {})

        if not responses:
            return jsonify({"status": "error", "message": "No responses provided"}), 400

        # Calculate RIASEC scores
        riasec_scores = calculate_riasec_scores(responses)

        # Generate Holland Code
        holland_code = generate_holland_code(riasec_scores)

        # Get course recommendations
        course_recommendations = get_course_recommendations(riasec_scores, responses)

        # Get college recommendations  
        college_recommendations = get_college_recommendations(course_recommendations)

        # Generate insights
        insights = generate_insights(holland_code, riasec_scores)

        # Create comprehensive recommendations
        recommendations = {
            "session_id": session_id,
            "personality_analysis": {
                "riasec_scores": riasec_scores,
                "holland_code": holland_code,
                "primary_type": get_personality_description(holland_code[0] if holland_code else 'R'),
                "personality_description": get_full_personality_description(holland_code)
            },
            "course_recommendations": course_recommendations,
            "college_recommendations": college_recommendations,
            "personalized_insights": insights,
            "generated_at": datetime.now().isoformat()
        }

        # Store in database
        try:
            conn = sqlite3.connect('career_guidance.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO assessments 
                (session_id, student_name, riasec_scores, holland_code, quiz_responses, recommendations)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                data.get('student_name', 'Anonymous'),
                json.dumps(riasec_scores),
                holland_code,
                json.dumps(responses),
                json.dumps(recommendations, default=str)
            ))
            conn.commit()
            conn.close()
        except Exception as db_error:
            print(f"Database storage error: {db_error}")
            # Continue even if database storage fails

        return jsonify({
            "status": "success",
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def calculate_riasec_scores(responses):
    scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    counts = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}

    for question_id, rating in responses.items():
        if isinstance(rating, (int, float)) and question_id[0] in scores:
            question_type = question_id[0]
            scores[question_type] += float(rating)
            counts[question_type] += 1

    # Convert to percentages
    for personality_type in scores:
        if counts[personality_type] > 0:
            scores[personality_type] = (scores[personality_type] / (counts[personality_type] * 5)) * 100
        else:
            scores[personality_type] = 0

    return scores

def generate_holland_code(riasec_scores):
    sorted_types = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)
    return ''.join([t[0] for t in sorted_types[:3]])

def get_course_recommendations(riasec_scores, responses):
    # Course mapping based on RIASEC types
    course_mapping = {
        "R": [("B.Tech", 85), ("B.Sc", 70)],
        "I": [("MBBS", 90), ("B.Tech", 80), ("B.Sc", 75)],
        "A": [("BA", 85), ("Fine Arts", 90)],
        "S": [("MBBS", 80), ("BA", 70), ("B.Ed", 85)],
        "E": [("BBA", 85), ("B.Com", 75)],
        "C": [("B.Com", 85), ("BBA", 70)]
    }

    recommendations = []

    # Get top 3 personality types
    sorted_types = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)[:3]

    for personality_type, score in sorted_types:
        if personality_type in course_mapping:
            for course, base_score in course_mapping[personality_type]:
                # Adjust score based on personality strength
                adjusted_score = min(95, int(base_score * (score / 100)))

                if not any(r['course'] == course for r in recommendations):
                    recommendations.append({
                        "course": course,
                        "full_name": get_full_course_name(course),
                        "match_score": adjusted_score,
                        "duration": get_course_duration(course),
                        "avg_fees": get_course_fees(course),
                        "recommendation_level": get_recommendation_level(adjusted_score),
                        "reason": f"Strong match with your {get_personality_description(personality_type)} personality"
                    })

    return sorted(recommendations, key=lambda x: x['match_score'], reverse=True)

def get_college_recommendations(course_recommendations):
    if not course_recommendations:
        return []

    try:
        conn = sqlite3.connect('career_guidance.db')
        cursor = conn.cursor()

        college_recs = []

        for course in course_recommendations[:3]:  # Top 3 courses
            cursor.execute('''
                SELECT * FROM colleges 
                WHERE course_type = ? 
                ORDER BY (CASE WHEN is_government = 1 THEN 0 ELSE 1 END), avg_fee_annual
                LIMIT 3
            ''', (course['course'],))

            columns = [desc[0] for desc in cursor.description]
            colleges = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for college in colleges:
                college_recs.append({
                    "college_name": college['college_name'],
                    "course_type": college['course_type'],
                    "location": f"{college['city']}, {college['region']}",
                    "annual_fee": college['avg_fee_annual'],
                    "college_type": college['category'],
                    "admission_mode": college['admission_mode'] or 'Merit-based',
                    "admission_probability": calculate_admission_probability(college),
                    "reason": f"Top choice for {course['course']}"
                })

        conn.close()
        return college_recs[:6]  # Return top 6

    except Exception as e:
        print(f"Error getting college recommendations: {e}")
        return []

def calculate_admission_probability(college):
    # Simple probability based on college type and difficulty
    base_prob = 0.7
    if college.get('is_government') == 1:
        base_prob *= 0.8  # Government colleges are more competitive
    if college.get('admission_difficulty', 1) > 3:
        base_prob *= 0.6  # High difficulty reduces probability
    return min(0.95, max(0.3, base_prob))

def generate_insights(holland_code, riasec_scores):
    insights = []

    if holland_code:
        insights.append(f"Your Holland Code is {holland_code}, indicating your primary career interests.")

        top_type = max(riasec_scores.items(), key=lambda x: x[1])[0]
        insights.append(f"Your strongest personality type is {get_personality_description(top_type)}.")

        # Add specific insights based on top type
        type_insights = {
            "R": "Consider careers in engineering, technology, or hands-on technical fields.",
            "I": "You're well-suited for research, analysis, and scientific careers.",
            "A": "Creative fields like design, writing, or arts would be fulfilling.",
            "S": "Helping professions like healthcare, education, or counseling are ideal.",
            "E": "Leadership roles in business, management, or entrepreneurship suit you.",
            "C": "Organized careers in finance, administration, or data management fit well."
        }

        if top_type in type_insights:
            insights.append(type_insights[top_type])

    insights.append("Consider exploring careers that match your personality profile for better job satisfaction.")
    insights.append("Talk to professionals in your recommended fields to learn more.")

    return insights

def get_personality_description(personality_type):
    descriptions = {
        "R": "Realistic (Doer)",
        "I": "Investigative (Thinker)", 
        "A": "Artistic (Creator)",
        "S": "Social (Helper)",
        "E": "Enterprising (Persuader)",
        "C": "Conventional (Organizer)"
    }
    return descriptions.get(personality_type, personality_type)

def get_full_personality_description(holland_code):
    if not holland_code:
        return "Your personality profile indicates diverse interests."

    primary = holland_code[0]
    descriptions = {
        "R": "You prefer practical, hands-on work and enjoy building or fixing things.",
        "I": "You enjoy analyzing problems, conducting research, and working with ideas.",
        "A": "You value creativity, self-expression, and artistic activities.",
        "S": "You enjoy helping others and working in team-oriented environments.",
        "E": "You like leading others, taking risks, and persuading people.",
        "C": "You prefer organized, detail-oriented work with clear procedures."
    }

    return descriptions.get(primary, "Your personality shows unique characteristics.")

def get_full_course_name(course):
    full_names = {
        "B.Tech": "Bachelor of Technology",
        "MBBS": "Bachelor of Medicine and Bachelor of Surgery",
        "B.Com": "Bachelor of Commerce",
        "BA": "Bachelor of Arts",
        "B.Sc": "Bachelor of Science",
        "BBA": "Bachelor of Business Administration",
        "B.Pharm": "Bachelor of Pharmacy"
    }
    return full_names.get(course, course)

def get_course_duration(course):
    durations = {
        "B.Tech": "4 years",
        "MBBS": "5.5 years",
        "B.Com": "3 years", 
        "BA": "3 years",
        "B.Sc": "3 years",
        "BBA": "3 years",
        "B.Pharm": "4 years"
    }
    return durations.get(course, "3-4 years")

def get_course_fees(course):
    fees = {
        "B.Tech": "₹2-8 Lakh/year",
        "MBBS": "₹1,400-10 Lakh/year",
        "B.Com": "₹5,000-50,000/year",
        "BA": "₹5,000-40,000/year", 
        "B.Sc": "₹6,000-60,000/year",
        "BBA": "₹20,000-3 Lakh/year",
        "B.Pharm": "₹30,000-2 Lakh/year"
    }
    return fees.get(course, "Varies by college")

def get_recommendation_level(score):
    if score >= 85:
        return "Highly Recommended"
    elif score >= 70:
        return "Recommended"
    elif score >= 60:
        return "Good Match"
    else:
        return "Consider"

if __name__ == '__main__':
    print("🚀 Starting Complete Career Guidance API...")
    print("✅ API available at: http://localhost:5000")
    print("✅ Health check: http://localhost:5000/api/health")
    print("✅ Colleges: http://localhost:5000/api/colleges") 
    print("✅ Assessment: http://localhost:5000/api/assessment/start")
    print("\nPress Ctrl+C to stop")

    app.run(host='0.0.0.0', port=5000, debug=True)
