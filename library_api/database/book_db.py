"""
BookDb class try
"""

from library_api.database.db_connection import get_connection

class BookDb:

    def create_book(self, data):
        connector = get_connection()
        cursor = connector.cursor()

        sql_txt = """
        INSERT INTO books(title, author, genre, is_available) 
        VALUES (%s, %s, %s, %s);
        """
        sql_vals = (data["title"], data["author"], data["genre"], True)

        cursor.execute(sql_txt, sql_vals)
        row_id = cursor.lastrowid

        connector.commit()

        cursor.close()
        connector.close()

        return row_id


    def get_all_books(self) -> list[dict | None]:
        """
        :return: list of dicts of all books
        """
        connector = get_connection()
        cursor = connector.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books;")
        data = cursor.fetchall()

        cursor.close()
        connector.close()
        return data


    def get_book_by_id(self, id):
        pass

    def update_book(self, id, data):
        pass

    def set_available(self, id, val, member_id):
        pass

    def count_total_books(self):
        pass

    def count_available_books(self):
        pass

    def count_borrowed_books(self):
        pass

    def count_by_genre(self, genre):
        pass

    def count_active_borrows_by_member(self, member_id):
        pass

if __name__ == "__main__":
    book = BookDb()
    new_book = {"title": "try", "author": "try", "genre": "other"}
    print(book.create_book(new_book))
    print(book.get_all_books())

