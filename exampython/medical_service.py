import mysql.connector
from datetime import datetime


def connect_to_database():
    try:
        
        conn = mysql.connector.connect(
            host="localhost", 
            user="root",  
            password="",  
            database="medical_service"
            
        )

        
        if conn.is_connected():
            print("Đã kết nối thành công tới cơ sở dữ liệu MySQL")
            return conn
        else:
            print("Không thể kết nối tới cơ sở dữ liệu MySQL")
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


connection = connect_to_database()


if connection:
    connection.close()
    print("Đã đóng kết nối với cơ sở dữ liệu")


def add_patients():
    conn = connect_to_database()
    cursor = conn.cursor()

    patients = [
        ("Nguyen A", "2010-01-01", "Male", "Ha noi", "0123456789", "nguyena@email.com"),
        ("Nguyen B", "1990-05-12", "Female", "Ha noi", "0123456789", "nguyenb@email.com"),
        ("Nguyen C", "2000-09-20", "Male", "Ha noi", "0123456789", "nguyenc@email.com")
    ]

    for patient in patients:
        query = "INSERT INTO patients (full_name, date_of_birth, gender, address, phone_number, email) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, patient)

    conn.commit()
    print("Đã thêm 3 bệnh nhân thành công.")
    cursor.close()
    conn.close()


def add_doctors():
    conn = connect_to_database()
    cursor = conn.cursor()

    doctors = [
        ("Nguyen Si", "Cardiology", "0123456789", "nguyensi@email.com", 10),
        ("Tran Binh", "Neurology", "0123456789", "tranbinh@email.com", 8),
        ("Le Hoa", "Orthopedics", "0123456789", "lehoa@email.com", 6),
        ("Nguyen Minh", "Pediatrics", "0123456789", "nguyenminh@email.com", 12),
        ("Pham Lan", "Dentistry", "0123456789", "phamlan@email.com", 7)
    ]

    for doctor in doctors:
        query = "INSERT INTO doctors (full_name, specialization, phone_number, email, years_of_experience) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, doctor)

    conn.commit()
    print("Đã thêm 5 bác sĩ thành công.")
    cursor.close()
    conn.close()


def add_appointments():
    conn = connect_to_database()
    cursor = conn.cursor()

    appointments = [
        (1, 1, "2024-11-29 09:00:00", "Kiểm tra sức khỏe định kỳ"),
        (2, 2, "2024-11-29 10:00:00", "Khám thần kinh"),
        (3, 3, "2024-11-29 11:00:00", "Khám nha khoa")
    ]

    for appointment in appointments:
        query = "INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, appointment)

    conn.commit()
    print("Đã thêm 3 cuộc hẹn cho bệnh nhân.")
    cursor.close()
    conn.close()


def generate_report():
    conn = connect_to_database()
    cursor = conn.cursor()

    query = """
    SELECT p.full_name, p.date_of_birth, p.gender, p.address, d.full_name AS doctor_name, a.reason, a.appointment_date
    FROM appointments a
    JOIN patients p ON a.patient_id = p.patient_id
    JOIN doctors d ON a.doctor_id = d.doctor_id
    """
    cursor.execute(query)
    result = cursor.fetchall()

    print("No | Patient Name | Birthday | Gender | Address | Doctor Name | Reason | Date")
    print("---------------------------------------------------------------------------------")
    for index, row in enumerate(result, start=1):
        print(f"{index} | {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]}")

    cursor.close()
    conn.close()


def show_today_appointments():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = connect_to_database()
    cursor = conn.cursor()

    query = """
    SELECT p.full_name, p.date_of_birth, p.gender, p.address, d.full_name AS doctor_name, a.status
    FROM appointments a
    JOIN patients p ON a.patient_id = p.patient_id
    JOIN doctors d ON a.doctor_id = d.doctor_id
    WHERE DATE(a.appointment_date) = %s
    """
    cursor.execute(query, (today,))
    result = cursor.fetchall()

    print("Address | No | Patient Name | Birthday | Gender | Doctor Name | Status")
    print("------------------------------------------------------------------------")
    for index, row in enumerate(result, start=1):
        print(f"{row[3]} | {index} | {row[0]} | {row[1]} | {row[2]} | {row[4]} | {row[5]}")

    cursor.close()
    conn.close()

add_patients()
add_doctors()
add_appointments()
generate_report()
show_today_appointments()
