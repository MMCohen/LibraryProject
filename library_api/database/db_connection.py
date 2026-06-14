import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="secret",
        database="library_db"
    )


def create_tables():
    connector = get_connection()
    cursor = connector.cursor()
    book_table = """CREATE TABLE IF NOT EXISTS books(
id INT PRIMARY KEY AUTO_INCREMENT,
title varchar(50) NOT NULL,
author varchar(50) NOT NULL,
genre ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other') NOT NULL,
is_available BOOLEAN NOT NULL,
borrowed_by_member_id INT
);

    """
    member_table = """CREATE TABLE IF NOT EXISTS members(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name varchar(50) NOT NULL,
    email varchar(50) UNIQUE NOT NULL,
    is_active BOOLEAN NOT NULL,
    total_borrows INT NOT NULL
    );

        """

    cursor.execute(book_table)
    cursor.execute(member_table)

    cursor.close()
    connector.close()