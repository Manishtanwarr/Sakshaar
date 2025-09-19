#!/usr/bin/env python3

import sqlite3
import pandas as pd
import os
from datetime import datetime

def create_database_with_data():
    db_path = 'career_guidance.db'

    print("🗄️ Creating database and loading data...")
    print("=" * 50)

    try:
        # Remove existing database if it exists
        if os.path.exists(db_path):
            os.remove(db_path)
            print("🗑️ Removed existing database")

        # Create new database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("📊 Creating database tables...")

        # Create colleges table
        cursor.execute('''
            CREATE TABLE colleges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                college_id TEXT UNIQUE NOT NULL,
                college_name TEXT NOT NULL,
                course_type TEXT NOT NULL,
                category TEXT NOT NULL,
                region TEXT NOT NULL,
                city TEXT NOT NULL,
                avg_fee_annual REAL NOT NULL,
                admission_mode TEXT,
                admission_difficulty INTEGER DEFAULT 1,
                is_government INTEGER DEFAULT 0,
                is_private INTEGER DEFAULT 0,
                courses_offered TEXT,
                original_fee_structure TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create assessments table
        cursor.execute('''
            CREATE TABLE assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                student_name TEXT,
                riasec_scores TEXT,
                holland_code TEXT,
                quiz_responses TEXT,
                recommendations TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        print("✅ Database tables created successfully")

        # Load college data if CSV exists
        csv_file = 'data/jk_colleges_clean.csv'
        if os.path.exists(csv_file):
            print(f"📈 Loading college data from {csv_file}...")

            df = pd.read_csv(csv_file)
            print(f"📊 Found {len(df)} colleges in CSV")

            # Insert college data
            inserted = 0
            for _, row in df.iterrows():
                try:
                    cursor.execute('''
                        INSERT INTO colleges (
                            college_id, college_name, course_type, category, region,
                            city, avg_fee_annual, admission_mode, admission_difficulty,
                            is_government, is_private, courses_offered, 
                            original_fee_structure, address
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        str(row.get('college_id', f'COL_{inserted+1:03d}')),
                        str(row.get('college_name', 'Unknown College')),
                        str(row.get('course_type', 'General')),
                        str(row.get('category', 'Unknown')),
                        str(row.get('region', 'Unknown')),
                        str(row.get('city', 'Unknown')),
                        float(row.get('avg_fee_annual', 0)),
                        str(row.get('admission_mode', 'Merit-based')),
                        int(row.get('admission_difficulty', 1)),
                        int(row.get('is_government', 1)),
                        int(row.get('is_private', 0)),
                        str(row.get('courses_offered', 'General Courses')),
                        str(row.get('original_fee_structure', 'Contact College')),
                        str(row.get('address', 'Contact College for Address'))
                    ))
                    inserted += 1
                except Exception as e:
                    print(f"⚠️ Error inserting row {inserted + 1}: {e}")
                    continue

            print(f"✅ Successfully inserted {inserted} colleges")

        else:
            print("⚠️ CSV file not found, creating with sample data...")

            # Insert sample college data
            sample_colleges = [
                ('COL001', 'Government Gandhi Memorial Science College, Jammu', 'BA', 'Government', 'Jammu', 'Jammu', 5118, 'CUET/Merit-based', 2, 1, 0, 'BA in multiple subjects', '5,028-5,208 (Annual)', 'Canal Road, Jammu, J&K - 180001'),
                ('COL002', 'National Institute of Technology, Srinagar', 'B.Tech', 'Government', 'Kashmir', 'Srinagar', 553000, 'JEE Main + JoSAA', 4, 1, 0, 'BTech Engineering', '5.53-6.03 Lakh (4 years)', 'Hazratbal, Srinagar, J&K - 190006'),
                ('COL003', 'Government Medical College, Jammu', 'MBBS', 'Government', 'Jammu', 'Jammu', 1400, 'NEET-UG', 4, 1, 0, 'MBBS', '1,400 (Annual)', 'Gujjar Nagar, Jammu, J&K - 180001'),
                ('COL004', 'Government Medical College, Srinagar', 'MBBS', 'Government', 'Kashmir', 'Srinagar', 1400, 'NEET-UG', 4, 1, 0, 'MBBS', '1,400 (Annual)', 'Karan Nagar, Srinagar, J&K - 190010'),
                ('COL005', 'Central University of Jammu', 'BBA', 'Government', 'Jammu', 'Jammu', 24430, 'CUET-UG', 3, 1, 0, 'BBA', '24,430 (1st Year)', 'Bagla, Rahya-Suchani, Jammu, J&K - 181143')
            ]

            for college_data in sample_colleges:
                cursor.execute('''
                    INSERT INTO colleges (
                        college_id, college_name, course_type, category, region,
                        city, avg_fee_annual, admission_mode, admission_difficulty,
                        is_government, is_private, courses_offered, 
                        original_fee_structure, address
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', college_data)

            print("✅ Sample college data inserted")

        # Commit all changes
        conn.commit()

        # Verify data
        cursor.execute('SELECT COUNT(*) FROM colleges')
        college_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM assessments')
        assessment_count = cursor.fetchone()[0]

        conn.close()

        print("\n🎉 DATABASE SETUP COMPLETE!")
        print("=" * 50)
        print(f"✅ Database file: {db_path}")
        print(f"✅ Colleges loaded: {college_count}")
        print(f"✅ Assessment table: Ready ({assessment_count} records)")

        return True

    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

if __name__ == "__main__":
    success = create_database_with_data()

    if success:
        print("\n🚀 READY TO START API SERVER!")
        print("Next step: python production_api.py")
    else:
        print("\n❌ Database setup failed. Check errors above.")
