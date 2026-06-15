
from library_api.database.db_connection import DbConnection


class EmailNotExist(Exception):
    pass

class MemberNotExist(Exception):
    pass


class MemberDb:
    def __init__(self, connection: DbConnection):
        self.connector = connection


    def create_member(self, data: dict) -> int:
        """
        create a new member
        :param data: dict
        :return: int the id of the new member
        """
        connector = self.connector.get_connection()
        cursor = connector.cursor()

        # check if email already exist:
        cursor.execute("SELECT * FROM members WHERE email = %s;", (data["email"],))
        email_exist = cursor.fetchone()
        if email_exist:
            raise EmailNotExist

        sql_txt = """
        INSERT INTO members (name, email)
        VALUES (%s, %s)
        """
        sql_vals = (data["name"], data["email"])
        try:
            cursor.execute(sql_txt, sql_vals)

            new_id = cursor.lastrowid
            connector.commit()

        finally:
            cursor.close()
            connector.close()

        return new_id


    def get_all_members(self) -> list[dict | None]:
        """
        :return: a list with all members details
        """
        connection = self.connector.get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM members;")
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return data


    def get_member_by_id(self, id):
        connector = self.connector.get_connection()
        cursor = connector.cursor(dictionary=True)

        cursor.execute("SELECT * FROM members WHERE id = %s;", (id,))
        member = cursor.fetchone()

        cursor.close()
        connector.close()

        return member



    def update_member(self, id, data: dict):
        """
        update member in the sql.
        :param id: int
        :param data: dict
        :return: True if updated. False if not.
        """
        connect = self.connector.get_connection()
        cursor = connect.cursor()

        sql_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        sql_vals = list(data.values()) + [id]

        cursor.execute(F"""
        UPDATE members
        SET {sql_clause}
        WHERE id = %s;
        """,
                       sql_vals)

        is_updated = cursor.rowcount > 0
        connect.commit()

        cursor.close()
        connect.close()

        return is_updated


    def deactivate_member(self, id):

        connect = self.connector.get_connection()
        cursor = connect.cursor(dictionary=True)

        is_id_exists = self.is_id_exist(id) # will rais MemberNotExist if not

        cursor.execute("UPDATE members SET is_active = False WHERE id = %s;", (id, ))

        is_deactivate = cursor.rowcount > 0

        connect.commit()

        cursor.close()
        connect.close()

        return is_deactivate


    def activate_member(self, id):
        pass


    def increment_borrows(self, id):
        pass


    def count_active_members(self):
        pass


    def get_top_member(self):
        pass

    def is_id_exist(self, id: int):
        """
        check if id exist raise MemberNotExist if not.
        True if exists:
        :param id:
        :return: True or MemberNotExist error.
        """
        connect = self.connector.get_connection()
        cursor = connect.cursor(dictionary=True)

        cursor.execute("SELECT * FROM members WHERE id = %s", (id,))
        member_data = cursor.fetchone()

        cursor.close()
        connect.close()

        if not member_data:
            raise MemberNotExist
        return True




if __name__ == "__main__":
    connector = DbConnection()
    member = MemberDb(connector)
    # new_member = {"name": "meir", "email": "meir@gmail.com"}
    # print(member.create_member(new_member))

    # print(member.get_member_by_id(9))

    # print(member.is_id_exist(8))

    print(member.deactivate_member(6))