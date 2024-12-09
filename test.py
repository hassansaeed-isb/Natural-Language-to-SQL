import mysql.connector
import random

# Example data for employees
names = [
    "George StPierre", "Jon Jones", "Anderson Silva", "Khabib Nurmagomedov", "Conor McGregor",
    "Daniel Cormier", "Israel Adesanya", "Max Holloway", "Nate Diaz", "Tony Ferguson"
]

# Generate records for employees
def generate_insert_employees(num_records=100):
    inserts = []
    id_usr_list = []
    for i in range(num_records):
        name = random.choice(names)
        id_usr = random.randint(1000, 9999)
        id_usr_list.append(id_usr)
        inserts.append(f"({id_usr}, '{name}')")
    return ",\n".join(inserts), id_usr_list

# Generate records for salary
def generate_insert_salary(id_usr_list, num_records=100):
    inserts = []
    for i in range(num_records):
        id_usr = random.choice(id_usr_list)  # Use valid ID_Usr from employees
        year = f"2023-01-01"
        salary = random.randint(50000, 70000)
        inserts.append(f"({id_usr}, '{year}', {salary})")
    return ",\n".join(inserts)

# Generate records for studies (Ensure unique ID_study)
def generate_insert_studies(id_usr_list, num_records=100):
    institutions = ["UC San Diego", "MIT", "Harvard University", "Stanford University", "Oxford University"]
    specialties = ["Bachelor of Science in Marketing", "PhD in Data Science", "Master of Science in Computer Science"]
    
    # Track used ID_study values to ensure uniqueness
    used_study_ids = set()
    inserts = []
    for i in range(num_records):
        id_study = random.randint(1000, 9999)
        
        # Ensure that the ID_study is unique
        while id_study in used_study_ids:
            id_study = random.randint(1000, 9999)
        
        used_study_ids.add(id_study)

        id_usr = random.choice(id_usr_list)  # Use valid ID_Usr from employees
        education_level = random.choice([3, 4, 5])
        institution = random.choice(institutions)
        year = f"2022-01-01"
        speciality = random.choice(specialties)
        inserts.append(f"({id_study}, {id_usr}, {education_level}, '{institution}', '{year}', '{speciality}')")
    return ",\n".join(inserts)

# Connect to MySQL database
def connect_to_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Change this if you're using a different MySQL user
        password='new_password',  # Change this to your actual password
        database='nlp_project'  # Change this to your database name
    )
    return conn

# Function to insert data into the database
def insert_data_to_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    
    try:
        # Insert employees
        employees_query, id_usr_list = generate_insert_employees()
        cursor.execute(f"INSERT INTO employees (ID_Usr, name) VALUES {employees_query}")
        print("Inserted records into employees table")

        # Insert salary (using valid ID_Usr from employees)
        salary_query = generate_insert_salary(id_usr_list)
        cursor.execute(f"INSERT INTO salary (ID_Usr, year, salary) VALUES {salary_query}")
        print("Inserted records into salary table")

        # Insert studies (using valid ID_Usr from employees)
        studies_query = generate_insert_studies(id_usr_list)
        cursor.execute(f"INSERT INTO studies (ID_study, ID_Usr, educational_level, Institution, Years, Speciality) VALUES {studies_query}")
        print("Inserted records into studies table")
        
        # Commit the transactions
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

# Call the insert function
insert_data_to_db()
