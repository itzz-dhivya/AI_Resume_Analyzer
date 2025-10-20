import mysql.connector

def connect_db(host="127.0.0.1", user="root", password="Dhivya", database="resume_analyzer"):
    try:
        conn = mysql.connector.connect(
            host=host,       # localhost or remote IP/hostname
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as e:
        print("DB connection error:", e)
        return None

def save_parsed_resume(conn, parsed: dict, match: dict = None, score: int = None):
    if conn is None:
        print("No database connection.")
        return False
    try:
        cursor = conn.cursor()
        skills = ", ".join(parsed.get("Skills", []))
        education = ", ".join(parsed.get("Education", []))

        cursor.execute("""
            INSERT INTO resume_data (name, email, phone, skills, education, experience)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (parsed.get("Name"), parsed.get("Email"), parsed.get("Phone"), skills, education, parsed.get("Experience")))
        resume_id = cursor.lastrowid

        if match is not None or score is not None:
            missing_skills = ", ".join(match.get("missing_skills", [])) if match else None
            skill_match_percent = match.get("skill_match_percent") if match else None
            cursor.execute("""
                INSERT INTO analysis_results (resume_id, skill_match, missing_skills, score)
                VALUES (%s, %s, %s, %s)
            """, (resume_id, skill_match_percent, missing_skills, score))

        conn.commit()
        cursor.close()
        return True
    except mysql.connector.Error as e:
        print("Error saving to DB:", e)
        return False

# ==== TEST CONNECTION ====
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        print("Database connected successfully!")
        conn.close()
    else:
        print("Failed to connect to database.")
