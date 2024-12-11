import sqlite3
import csv
from statistics import mean
#Initialize DB and create table if it doesnt exist using sql
def initialize_db(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY,
            type TEXT NOT NULL,
            severity INTEGER NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

#Insert Incidents into database file
def insert_incident(db_file, incident_type, severity, description):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO incidents (type, severity, description) VALUES (?, ?, ?)",
                   (incident_type, severity, description))
    conn.commit()
    conn.close()

#Get all incidents from database file
def fetch_all_incidents(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents")
    incidents = cursor.fetchall()
    conn.close()
    return incidents

def export_to_csv(incidents, csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Type", "Severity", "Description"])
        writer.writerows(incidents)

def calculate_statistics(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT severity FROM incidents")
    severities = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not severities:
        return {"average_severity": "No data available"}

    return {"average_severity": round(mean(severities), 2)}

def log_action(log_file, message):
    with open(log_file, 'a') as log:
        log.write(f"{message}\n")

def validate_input(incident_type, severity, description):
    if not incident_type or not severity.isdigit() or int(severity) < 1 or int(severity) > 10:
        print("Invalid input. Please check your fields.")
        return False
    return True
