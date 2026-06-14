import mysql.connector


class DbConnection:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 3306
        self.user = "root"
        self.password = "secret"
        self.database = "library_db"


    def get_connection(self):
        return mysql.connector.connect(
            host= self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )


    def create_tables(self):
        connector = self.get_connection()
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