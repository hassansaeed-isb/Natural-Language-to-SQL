from flask import Flask, request, render_template, jsonify
import mysql.connector
import re
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch database credentials from environment variables
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Function to generate SQL query
def generate_sql(question):
    # Connect to MySQL database using environment variables
    conn = mysql.connector.connect(
        host=DB_HOST,  # The host from the .env file
        user=DB_USERNAME,  # The username from the .env file
        password=DB_PASSWORD,  # The password from the .env file
        database=DB_NAME  # The database name from the .env file
    )
    cursor = conn.cursor()

    # Normalize question to lowercase for case-insensitive comparison
    question = question.lower()

    # **Employee Queries**
    if "salary" in question and "daniel cormier" in question:
        # Get salary of employee Daniel Cormier
        sql_query = "SELECT s.salary FROM employees e JOIN salary s ON e.ID_Usr = s.ID_Usr WHERE e.name = 'Daniel Cormier';"
        cursor.execute(sql_query)
        result = cursor.fetchone()
        if result:
            return f"Generated SQL Query: {sql_query}\nResult: {result[0]}"
        else:
            return f"Generated SQL Query: {sql_query}\nResult: No data found for Daniel Cormier's salary."

    elif "how many" in question and "employees" in question:
        # Count number of employees
        sql_query = "SELECT COUNT(*) FROM employees;"
        cursor.execute(sql_query)
        result = cursor.fetchone()
        return f"Generated SQL Query: {sql_query}\nResult: {result[0]}"

    elif "employee" in question and "id" in question:
        # Get employee details by ID
        employee_id = int(re.search(r'\d+', question).group())
        sql_query = f"SELECT * FROM employees WHERE ID_Usr = {employee_id};"
        cursor.execute(sql_query)
        result = cursor.fetchall()
        if result:
            return f"Generated SQL Query: {sql_query}\nResult: {result}"
        else:
            return "Generated SQL Query: " + sql_query + "\nResult: No employee found with that ID."

    # **Salary Queries**
    elif "salary" in question and "greater than" in question:
        # Employees with salary greater than a certain threshold
        threshold_match = re.search(r"\d+", question)
        if threshold_match:
            threshold = int(threshold_match.group())
            sql_query = f"""
            SELECT e.name, s.salary 
            FROM employees e 
            JOIN salary s ON e.ID_Usr = s.ID_Usr 
            WHERE s.salary > {threshold};
            """
            cursor.execute(sql_query)
            result = cursor.fetchall()
            if result:
                employees = [f"{row[0]} - {row[1]}" for row in result]
                return f"Generated SQL Query: {sql_query}\nResult: {', '.join(employees)}"
            else:
                return f"Generated SQL Query: {sql_query}\nResult: No employees found with salary greater than {threshold}."
        else:
            return "No salary threshold found in the question."

    elif "average salary" in question:
        # Get the average salary
        sql_query = "SELECT AVG(salary) FROM salary;"
        cursor.execute(sql_query)
        result = cursor.fetchone()
        if result:
            return f"Generated SQL Query: {sql_query}\nResult: {result[0]}"
        else:
            return f"Generated SQL Query: {sql_query}\nResult: No salary data available."

    elif "salary" in question and "year" in question:
        # Get salary records for a specific year
        year_match = re.search(r"\d{4}", question)
        if year_match:
            sql_query = f"SELECT * FROM salary WHERE year = '{year_match.group()}';"
            cursor.execute(sql_query)
            result = cursor.fetchall()
            if result:
                return f"Generated SQL Query: {sql_query}\nResult: {result}"
            else:
                return f"Generated SQL Query: {sql_query}\nResult: No salary records found for the year {year_match.group()}."
        else:
            return "No year found in the question."

    elif "salary" in question and "employee" in question:
        # Get salary records for a specific employee
        employee_id = int(re.search(r'\d+', question).group())
        sql_query = f"SELECT * FROM salary WHERE ID_Usr = {employee_id};"
        cursor.execute(sql_query)
        result = cursor.fetchall()
        if result:
            return f"Generated SQL Query: {sql_query}\nResult: {result}"
        else:
            return f"Generated SQL Query: {sql_query}\nResult: No salary records found for employee with ID {employee_id}."

    # **Study Queries**
    elif "study" in question and "employee" in question:
        # Get studies for a specific employee
        employee_id = int(re.search(r'\d+', question).group())
        sql_query = f"SELECT * FROM studies WHERE ID_Usr = {employee_id};"
        cursor.execute(sql_query)
        result = cursor.fetchall()
        if result:
            return f"Generated SQL Query: {sql_query}\nResult: {result}"
        else:
            return f"Generated SQL Query: {sql_query}\nResult: No study records found for employee with ID {employee_id}."

    elif "institution" in question and "study" in question:
        # Get institutions where an employee studied
        employee_id = int(re.search(r'\d+', question).group())
        sql_query = f"SELECT DISTINCT Institution FROM studies WHERE ID_Usr = {employee_id};"
        cursor.execute(sql_query)
        result = cursor.fetchall()
        if result:
            institutions = [row[0] for row in result]
            return f"Generated SQL Query: {sql_query}\nResult: {', '.join(institutions)}"
        else:
            return f"Generated SQL Query: {sql_query}\nResult: No institutions found for employee with ID {employee_id}."

    elif "specialization" in question:
        # Get studies based on specialization (e.g., "PhD", "Bachelor", etc.)
        specialization = re.search(r"\b(?:bachelor|phd|master)\b", question, re.IGNORECASE)
        if specialization:
            sql_query = f"SELECT * FROM studies WHERE Speciality LIKE '%{specialization.group()}%';"
            cursor.execute(sql_query)
            result = cursor.fetchall()
            if result:
                return f"Generated SQL Query: {sql_query}\nResult: {result}"
            else:
                return f"Generated SQL Query: {sql_query}\nResult: No studies found with the specialization {specialization.group()}."
        else:
            return "Generated SQL Query: N/A\nResult: No specialization found in the question."

    elif "educational level" in question:
        # Get studies based on educational level (3, 4, or 5)
        level = int(re.search(r'\d+', question).group())
        sql_query = f"SELECT * FROM studies WHERE educational_level = {level};"
        cursor.execute(sql_query)
        result = cursor.fetchall()
        if result:
            return f"Generated SQL Query: {sql_query}\nResult: {result}"
        else:
            return f"Generated SQL Query: {sql_query}\nResult: No studies found with educational level {level}."

    # Default response for unsupported queries
    else:
        return "Unable to generate SQL query. Please refine your question."

    cursor.close()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_sql', methods=['POST'])
def generate_sql_route():
    question = request.form.get('question')
    sql_query_result = generate_sql(question)
    return jsonify({"sql_query": sql_query_result})

if __name__ == '__main__':
    app.run(debug=True)
