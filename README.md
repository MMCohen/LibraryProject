
# Library system management
___

[//]: # (### welcom to...)

[//]: # (___)

[//]: # ()
[//]: # (```)

[//]: # (docker run --name mysql-w7 \ -e MYSQL_ROOT_PASSWORD=root \ -e MYSQL_DATABASE=soldiers_db \ -p 3306:3306 \ -d mysql:8)

[//]: # (```)

### system description:

`Library system management` is a system that takes care of everything you need to manage your library.

### including:
* creates the database. `sql container`, `create tables`
* connection with the database. `establish connection`
* manage members. `add member`,`delete member`, `see member details`
* manage books. `add/delete books`, `mark as borrowd/returned` 
* create fastapi server. `establish server`

to be used by libraries that want order.

___

## Technologies Used
* Docker
* fastapi and uvicorn 
* python
* mysql


---

### create docker container

code:
```dockerfile
docker run --name mysql-w7 \ -e MYSQL_ROOT_PASSWORD=root \ -e MYSQL_DATABASE=soldiers_db \ -p 3306:3306 \ -d mysql:8 
```

---

## directories structure:
```
library-api/
│
│
├── main.py
├── database/
│ ├── db_connection.py
│ ├── book_db.py
│ └── member_db.py
├── routes/
│ ├── book_routes.py
│ ├── member_routes.py
│ └── report_routes.py
├── logs/
│ └── app.log
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Tables structure:

### Table `books`:

id auto increment ?

| field                 | type                                                 | CONSTRAINT  | DESCRIPTION                     |
|-----------------------|------------------------------------------------------|-------------|---------------------------------|
| id                    | INT                                                  | PRIMARY KEY | book id                         |
| title                 | varchar(50)                                          | NOT NULL    | book title                      |
| author                | varchar(50)                                          | NOT NULL    | book author                     |
| genre                 | ENUM (Fiction, Non-Fiction, Science, History, Other) | NOT NULL    | book genre                      |
| is_available          | BOOLEAN                                              | NOT NULL    | book availability. False if not |
| id_member_by_borrowed | INT                                                  |             | if borrowed, shows woh borrowed |


### Table `members`:
id auto increment ?
email TINYTEXT ?
total_borrows AUTO_INCREMENT? how does it work?

| field         | type        | CONSTRAINT       | DESCRIPTION                    |
|---------------|-------------|------------------|--------------------------------|
| id            | INT         | PRIMARY KEY      | member id                      |
| name          | varchar(50) | NOT NULL         | member name                    |
| email         | TINYTEXT    | NOT NULL, UNIQUE | member email. must be unique   |
| is_active     | BOOLEAN     | NOT NULL         | True for active member         |
| total_borrows | INT         | AUTO_INCREMENT   | how many books member borrowed |

---

# Python moduls:

### db_connection.py:
* `get_connection` - establish connection with the sql container.
* `create_tables` - create the tables in the database if not exists. runs from main file.

### BookDB.py
* `create_book(data)` - insert new book to table books. defaults is_available=True, borrowed_by=NULL
* `get_all_books() ` - returns all books list
* `get_book_by_id(id) ` - returns one book | None
* `update_book(id, data) ` - update book by id with the data sent
* `set_available(id, val, member_id) ` - update both book to available 
* `count_total_books()` - count all books
* `count_avilable_books()` - count books with True in is_available
* `count_borrwed_books(genre)` - count borrowed books by genre
* `count_active_borrows_by_member(member_id)` - returns how many books are borrowed by member_id

### MemberDB.py
* `create_member(data)` - insert new member. default is_active=True, total_borrows=0
* `get_all_members()` - returns all members
* `get_member_by_id(id)` - return member by id | None
* `update_member(id, data)` - update member with the data that has been sent.
* `deactivate_member(id)` - update is_active=False
* `activate_member(id)` - update is_active=True
* `increment_borrows(id)` - add 1 to borrowed book
* `count_active_members()` - count members with is_active = True
* `get_top_member()` - get the member with biggest borrowed books 

---

# system rules:
1. Creating book - the user sends 1. title. 2. genre. 3. author. the system adds is_available=True, borrowed_by=NULL.
2. Genre - must be one from the: (Fiction, Non-Fiction, Science, History, Other)
3. Add member - the user sends 1. name. 2. email. the system adds is_active = True. total_borrows = 0.
4. Email - must be unique.
5. Inactive member - cannot borrow books.
6. Unavailable book - cannot be borrowed.
7. Max borrow - member can not borrow more than 3 books.
8. Return book - can be return only from the member that borrow the book.


end
