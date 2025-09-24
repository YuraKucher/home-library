"""
17. Домашня бібліотека
Скласти програму з графічним інтерфейсом, яка реалізує функціональність, що необхідна для ведення
домашньої бібліотеки. У бібліотеці зберігаються книги та періодичні видання. Усі видання розподілені
за жанрами (може бути декілька для одного видання), видом видання (науково-технічне, підручник,
художня література), рік випуску. У кожного видання може бути один або декілька авторів. Так само
вказують інформацію щодо місця збереження видання у бібліотеці (шафа, полиця).
Програма повинна дозволяти додавання/зміну/видалення видання, додавання/зміну/видалення
автора додавання/зміну/видалення виду або жанру, місць збереження. Також програма повинна
здійснювати пошук видання (видань) за назвою, автором, жанром, видом.
Дані про видання, авторів, види, жанри, місця збереження зберігаються у базі даних.
"""

import sqlite3


class DBHomeLibrary:
    def __init__(self, file_name):
        self.name = file_name

    def createrb(self):
        with sqlite3.connect(self.name) as db:
            curs = db.cursor()
            query = '''
                CREATE TABLE IF NOT EXISTS Book
            (
            id INTEGER PRIMARY KEY, 
            name VARCHAR(100),
            date_of_public VARCHAR(40),
            id_publication_type INTEGER,
            id_location INTEGER
            );
                CREATE TABLE IF NOT EXISTS Publication_type
            (
            id INTEGER PRIMARY KEY, 
            name VARCHAR(80)
            );
                CREATE TABLE IF NOT EXISTS Author
            (
            id INTEGER PRIMARY KEY, 
            name VARCHAR(100)
            );
                CREATE TABLE IF NOT EXISTS Genre
            (
            id INTEGER PRIMARY KEY, 
            name VARCHAR(100)
            );
                CREATE TABLE IF NOT EXISTS Book_Authors
            (
            id INTEGER PRIMARY KEY, 
            book_id INTEGER,
            author_id INTEGER,
            FOREIGN KEY (book_id) REFERENCES Book(id),
            FOREIGN KEY (author_id) REFERENCES Author(id)
            );
                  CREATE TABLE IF NOT EXISTS Book_Genres
            (
            id INTEGER PRIMARY KEY, 
            book_id INTEGER,
            genre_id INTEGER,
            FOREIGN KEY (book_id) REFERENCES Book(id),
            FOREIGN KEY (genre_id) REFERENCES Genre(id)
            );
                CREATE TABLE IF NOT EXISTS Storage_location
            (
            id INTEGER PRIMARY KEY, 
            bookcase VARCHAR(40),
            shelf VARCHAR(40)
            )
            '''
            curs.executescript(query)
            n = int(input('Кількість записів: '))
            for i in range(n):

                # ВИЗНАЧАЄМО НАЗВУ.

                name = input('Назва книги: ')
                ID = curs.execute("SELECT id FROM Book WHERE name=?", (name,))
                if not curs.fetchone():
                    curs.execute("INSERT INTO Book(name) VALUES (?)", (name,))
                    ID = curs.execute("SELECT id FROM Book WHERE name=?", (name,))

                # Отримуємо id книги з якою будемо працювати
                ID = ID.fetchone()[0]

                # ВИЗНАЧАЄМО АВТОРІВ

                k = int(input('Кількість авторів книги: '))
                for i in range(k):
                    name_author = input(f'Автор{i + 1}: ')
                    curs.execute("SELECT id FROM Author WHERE name=?", (name_author,))
                    if not curs.fetchone():
                        # додаємо нового автора
                        curs.execute("INSERT INTO Author(name) VALUES (?)", (name_author,))
                    # зчитуємо id автора
                    id_au = curs.execute("SELECT id FROM Author WHERE name=?", (name_author,)).fetchone()[0]
                    # додаємо інформацію що цей автор написав книгу в таблицю відношення книги до автора
                    curs.execute("INSERT INTO Book_Authors(book_id, author_id) VALUES (?, ?)", (ID, id_au))

                # ВИЗНАЧАЄМО ЖАНРИ

                k = int(input('Кількість жанрів книги: '))
                for i in range(k):
                    name_genre = input(f'Жанр{i + 1}: ')
                    curs.execute("SELECT id FROM Genre WHERE name=?", (name_genre,))
                    if not curs.fetchone():
                        # додаємо новий жанр
                        curs.execute("INSERT INTO Genre(name) VALUES (?)", (name_genre,))
                    # зчитуємо id жанру
                    id_ge = curs.execute("SELECT id FROM Genre WHERE name=?", (name_genre,)).fetchone()[0]
                    # додаємо інформацію про те що книга написана в цьому жанрі до таблиці відношення книги по жанру
                    curs.execute("INSERT INTO Book_Genres(book_id, genre_id) VALUES (?, ?)", (ID, id_ge))

                # ВИЗНАЧАЄМО ДАТУ ПУБЛІКАЦІЇ

                date = input('Дата публікації книги: ')
                curs.execute("UPDATE Book SET date_of_public=? WHERE id = ?", (date, ID))

                # ВИЗНАЧАЄМО ВИД ВИДАННЯ

                edition = input('Вид видання книги: ')
                curs.execute("SELECT id FROM Publication_type WHERE name=?", (edition,))
                if not curs.fetchone():
                    # додаємо вид видання до таблиці видів
                    curs.execute("INSERT INTO Publication_type(name) VALUES (?)", (edition,))
                id_ed = curs.execute("SELECT id FROM Publication_type WHERE name=?", (edition,)).fetchone()[0]
                curs.execute("UPDATE Book SET id_publication_type=? WHERE id = ?", (id_ed, ID))

                # ВИЗНАЧАЄМО МІСЦЕ ЗБЕРІГАННЯ

                bookcase = input('В якій шафі зберігається книга: ')
                shelf = input("На якій полиці стоїть книга: ")
                curs.execute("SELECT id FROM Storage_location WHERE bookcase = ? AND shelf = ?", [bookcase, shelf])
                if not curs.fetchone():
                    # додаємо нову локацію де зберігають книгу
                    curs.execute("INSERT INTO Storage_location(bookcase, shelf) VALUES (?, ?)", (bookcase, shelf))
                id_loc = curs.execute("SELECT id FROM Storage_location "
                                      "WHERE bookcase = ? AND shelf = ?", [bookcase, shelf]).fetchone()[0]
                curs.execute("UPDATE Book SET id_location = ? WHERE id = ?", (id_loc, ID))

    def add_author(self, name):
        conn = sqlite3.connect(self.name)
        curs = conn.cursor()
        curs.execute("SELECT id FROM Author WHERE name=?", (name,))
        if not curs.fetchone():
            curs.execute("INSERT INTO Author(name) VALUES (?)", (name,))
        conn.commit()
        conn.close()

    def add_genre(self, name):
        conn = sqlite3.connect(self.name)
        curs = conn.cursor()
        curs.execute("SELECT id FROM Genre WHERE name=?", (name,))
        if not curs.fetchone():
            curs.execute("INSERT INTO Genre(name) VALUES (?)", (name,))
        conn.commit()
        conn.close()

    def add_edition(self, name):
        conn = sqlite3.connect(self.name)
        curs = conn.cursor()
        curs.execute("SELECT id FROM Publication_type WHERE name=?", (name,))
        if not curs.fetchone():
            curs.execute("INSERT INTO Publication_type(name) VALUES (?)", (name,))
        conn.commit()
        conn.close()

    def add_location(self, bookcase, shelf):
        conn = sqlite3.connect(self.name)
        curs = conn.cursor()
        curs.execute("SELECT id FROM Storage_location WHERE bookcase = ? AND shelf = ?", [bookcase, shelf])
        if not curs.fetchone():
            curs.execute("INSERT INTO Storage_location(bookcase, shelf) VALUES (?, ?)", (bookcase, shelf))
        conn.commit()
        conn.close()

    def add_book(self, name, list_authors, list_genres, public_type, date, bookcase, shelf):
        """
        name         -  назва книги
        list_authors -  список авторів книги у вигляді 'Марк Твен, Тарас Шевченко'
        list_genres  -  спосок жанрів книги у вигляді 'Роман, Лірика'
        public_type  -  вид видання
        date         -  дата видання (текст)
        bookcase     -  назва чи означення шафи. Користувач може як забажає називати свої шафи.
                        Наприклад "купе" або "дубова"
        shelf        -  полиця на якій стоїть книга у форматі текст, адже користувач самостійно
                        обирає як називати полиці це можуть бути або цифри або наприклад слова
                        "остання", "верхня"
        """
        id_ed = 'NULL'
        id_loc = 'NULL'
        date_pub = 'NULL'
        conn = sqlite3.connect(self.name)
        curs = conn.cursor()
        # визначаємо чи не порожній рядок ввели в якось дати публікації
        if len(date.split()) != 0:
            date_pub = date
        # визначаємо чи не порожній рядок ввели в якось виду публікації
        if len(public_type.split()) != 0:
            if not curs.execute("SELECT id FROM Publication_type WHERE name=?", (public_type,)).fetchone():
                # додаємо вид видання до таблиці видів
                curs.execute("INSERT INTO Publication_type(name) VALUES (?)", (public_type,))
            id_ed = curs.execute("SELECT id FROM Publication_type WHERE name=?", (public_type,)).fetchone()[0]
        # визначаємо чи введені всі дані про місце знаходження книги
        if len(bookcase.split()) != 0 and len(shelf.split()) != 0:
            if not curs.execute("SELECT id FROM Storage_location WHERE bookcase = ? AND shelf = ?",
                                [bookcase, shelf]).fetchone():
                # додаємо нову локацію де зберігають книги
                curs.execute("INSERT INTO Storage_location(bookcase, shelf) VALUES (?, ?)", (bookcase, shelf))
            id_loc = curs.execute("SELECT id FROM Storage_location WHERE bookcase = ? AND shelf = ?",
                                  [bookcase, shelf]).fetchone()[0]
        # Перевіряємо чи введена назва книги не пуста.
        # Якщо вона пуста то книга не додається взагалі
        if len(name.split()) != 0:
            # додаємо дану книгу з назвою name та іншими введеними даними
            # Якщо якісь данні не були введені, то на їх місці додається NULL
            curs.execute("INSERT INTO "
                         "Book(name, id_publication_type, date_of_public, id_location) "
                         "VALUES (?, ?, ?, ?)",
                         (name, id_ed, date_pub, id_loc))
        # отримуємо id книги
        ID = curs.execute("SELECT id FROM Book WHERE name = ? AND id_publication_type=? "
                          "AND date_of_public=? AND id_location=?", [name, id_ed, date_pub, id_loc]).fetchone()[0]
        for author in list_authors.split(','):
            author = author.lstrip(' ')
            if len(author.split()) != 0:
                if not curs.execute("SELECT id FROM Author WHERE name=?", (author,)).fetchone():
                    # додаємо нового автора
                    curs.execute("INSERT INTO Author(name) VALUES (?)", (author,))
                id_au = curs.execute("SELECT id FROM Author WHERE name=?", (author,)).fetchone()[0]
                # якщо ID не порожній, то додаємо інформацію що цей автор написав книгу
                # в таблицю відношення книги до автора
                curs.execute("INSERT INTO Book_Authors(book_id, author_id) VALUES (?, ?)", (ID, id_au))
        for genre in list_genres.split(','):
            genre = genre.lstrip(' ')
            if len(genre.split()) != 0:
                if not curs.execute("SELECT id FROM Genre WHERE name=?", (genre,)).fetchone():
                    # додаємо новий жанр
                    curs.execute("INSERT INTO Genre(name) VALUES (?)", (genre,))
                id_ge = curs.execute("SELECT id FROM Genre WHERE name=?", (genre,)).fetchone()[0]
                # якщо ID не порожній, то додаємо інформацію що цей жанр відноситься до книги
                # в таблицю відношення книги до жанру
                curs.execute("INSERT INTO Book_Genres(book_id, genre_id) VALUES (?, ?)", (ID, id_ge))
        conn.commit()
        conn.close()

    def change_book(self, id_book, name=None, list_authors=None, list_genres=None,
                    public_type=None, date=None, bookcase=None, shelf=None):
        """
        id_book      -  ID книги
        name         -  назва книги
        list_authors -  список авторів книги у вигляді 'Марк Твен, Тарас Шевченко'
        list_genres  -  спосок жанрів книги у вигляді 'Роман, Лірика'
        public_type  -  вид видання
        date         -  дата видання (текст)
        bookcase     -  назва чи означення шафи. Користувач може як забажає називати свої шафи.
                        Наприклад "купе" або "дубова"
        shelf        -  полиця на якій стоїть книга у форматі текст, адже користувач самостійно
                        обирає як називати полиці це можуть бути або цифри або наприклад слова
                        "остання", "верхня"
        """
        conn = sqlite3.connect(self.name)
        curs = conn.cursor()
        curs.execute('SELECT * FROM Book WHERE id = ?', (id_book,))
        old_info_book = curs.fetchone()
        new_name = name if name is not None else old_info_book[1]
        new_date = date if date is not None else old_info_book[2]
        new_public_type = old_info_book[3]
        if public_type is not None:
            print("pub_type not NONE\n", public_type)
            curs.execute("SELECT id FROM Publication_type WHERE name=?", (public_type,))
            if not curs.fetchone():
                curs.execute("INSERT INTO Publication_type(name) VALUES (?)", (name,))
            new_public_type = curs.execute("SELECT id FROM Publication_type WHERE name=?", (public_type,)).fetchone()[0]
        if list_authors is not None:
            # видаляємо інформацію про всіх авторів книги з таблиці відношення авторів та книг
            curs.execute("DELETE FROM Book_Authors WHERE book_id=?", [id_book])
            for author in list_authors.split(','):
                author = author.lstrip(' ')
                if len(author.split()) != 0:
                    if not curs.execute("SELECT id FROM Author WHERE name=?", (author,)).fetchone():
                        # додаємо нового автора
                        curs.execute("INSERT INTO Author(name) VALUES (?)", (author,))
                    # зчитуємо id автора якого було введено
                    id_au = curs.execute("SELECT id FROM Author WHERE name=?", (author,)).fetchone()[0]
                    # додаємо інформацію що цей автор написав книгу в таблицю відношення книги до автора
                    curs.execute("INSERT INTO Book_Authors(book_id, author_id) VALUES (?, ?)", (id_book, id_au))
        if list_genres is not None:
            # видаляємо інформацію про всі жанри книги з таблиці відношення авторів та жанрів
            curs.execute("DELETE FROM Book_Genres WHERE book_id=?", [id_book])
            for genre in list_genres.split(','):
                genre = genre.lstrip(' ')
                if len(genre.split()) != 0:
                    if not curs.execute("SELECT id FROM Genre WHERE name=?", (genre,)).fetchone():
                        # додаємо новий жанр
                        curs.execute("INSERT INTO Genre(name) VALUES (?)", (genre,))
                    # зчитуємо id жанра якого було введено
                    id_ge = curs.execute("SELECT id FROM Genre WHERE name=?", (genre,)).fetchone()[0]
                    # додаємо інформацію що цей жанр належить книзі в таблицю відношення книги до жанру
                    curs.execute("INSERT INTO Book_Genres(book_id, genre_id) VALUES (?, ?)", (id_book, id_ge))
        new_id_loc = old_info_book[4]
        if bookcase is not None:
            if shelf is not None:
                curs.execute("SELECT id FROM Storage_location WHERE bookcase = ? AND shelf = ?", [bookcase, shelf])
                if not curs.fetchone():
                    curs.execute("INSERT INTO Storage_location(bookcase, shelf) VALUES (?, ?)", (bookcase, shelf))
            else:
                old_shelf = curs.execute("SELECT shelf FROM Storage_location WHERE id=?",
                                         [old_info_book[4]]).fetchone()[0]
                curs.execute("SELECT id FROM Storage_location WHERE bookcase = ? AND shelf = ?", [bookcase, old_shelf])
                if not curs.fetchone():
                    curs.execute("INSERT INTO Storage_location(bookcase, shelf) VALUES (?, ?)", (bookcase, shelf))
            new_id_loc = curs.execute("SELECT id FROM Storage_location WHERE bookcase = ? AND shelf = ?",
                                  [bookcase, shelf]).fetchone()[0]
        curs.execute("UPDATE Book SET name=?, date_of_public=?, id_publication_type = ?, id_location = ? "
                     "WHERE id = ?", (new_name, new_date, new_public_type, new_id_loc, id_book))
        conn.commit()
        conn.close()

    def book_search_by_name(self, name, id_book=None):
        text = ''
        conn = sqlite3.connect(self.name)
        curs = conn.cursor()
        curs.execute("SELECT * FROM Book WHERE name=?", (name,))
        if id_book:
            curs.execute("SELECT * FROM Book WHERE name=? AND id=?", [name, id_book])
        rows = curs.fetchall()
        if len(rows) != 0:
            for row in rows:
                curs.execute("SELECT * FROM Book_Authors WHERE book_id=?", (row[0],))
                rows_au = curs.fetchall()
                LIST_AUTHORS = 'NULL'
                if len(rows_au) != 0:
                    LIST_AUTHORS = ''
                    for row_au in rows_au:
                        LIST_AUTHORS += str(curs.execute("SELECT name FROM Author WHERE id=?",
                                                         (row_au[2],)).fetchone()[0] + ', ')
                curs.execute("SELECT * FROM Book_Genres WHERE book_id=?", (row[0],))
                rows_ge = curs.fetchall()
                LIST_GENRES = 'NULL'
                if len(rows_ge) != 0:
                    LIST_GENRES = ''
                    for row_ge in rows_ge:
                        LIST_GENRES += str(curs.execute("SELECT name FROM Genre WHERE id=?",
                                                        (row_ge[2],)).fetchone()[0] + ', ')
                publication_type = 'NULL'
                if row[3] != 'NULL':
                    publication_type = curs.execute("SELECT name FROM Publication_type WHERE id=?",
                                                    (row[3],)).fetchone()[0]
                location = ['NULL', 'NULL']
                if row[4] != 'NULL':
                    location = curs.execute("SELECT * FROM Storage_location WHERE id=?",
                                            (row[4],)).fetchone()[1:3]

                text += f"ID книги {row[0]}, Назва книги: {name}, Автор/(и): {LIST_AUTHORS}Жанр/(и): {LIST_GENRES}" \
                        f"Вид Публікації: {publication_type}, Дата випуску: {row[2]}, Зберігається в шафі: {location[0]}, " \
                        f"На поличці: {location[1]}\n"
        else:
            text = "Книги з такою назвою не знайдено\n"
        return text

    def book_search_by_author(self, author):
        text = ''
        conn = sqlite3.connect(self.name)
        curs = conn.cursor()
        try:
            id_au = curs.execute("SELECT id FROM Author WHERE name=?", (author,)).fetchone()[0]
            curs.execute("SELECT book_id FROM Book_Authors WHERE author_id=?", (id_au,))
            rows = curs.fetchall()
            if len(rows) != 0:
                for row in rows:
                    curs.execute("SELECT * FROM Book WHERE id=?", (row[0],))
                    row_books = curs.fetchall()
                    for book in row_books:
                        text += self.book_search_by_name(book[1], book[0]) + '\n'
            else:
                text = "Книг з таким автором не знайдено\n"
        except TypeError:
            text = "Книг такого автора не знайдено\n"
        return text

    def book_search_by_genre(self, genre):
        text = ''
        conn = sqlite3.connect(self.name)
        curs = conn.cursor()
        try:
            id_ge = curs.execute("SELECT id FROM Genre WHERE name=?", (genre,)).fetchone()[0]
            curs.execute("SELECT book_id FROM Book_Genres WHERE genre_id=?", (id_ge,))
            rows = curs.fetchall()
            if len(rows) != 0:
                for row in rows:
                    curs.execute("SELECT * FROM Book WHERE id=?", (row[0],))
                    row_books = curs.fetchall()
                    for book in row_books:
                        text += self.book_search_by_name(book[1], book[0]) + '\n'
            else:
                text = "Книг з таким жанром не знайдено\n"
        except TypeError:
            text = "Книг такого жанру не знайдено\n"
        return text

    def book_search_by_publication_type(self, public_type):
        text = ''
        conn = sqlite3.connect(self.name)
        curs = conn.cursor()
        try:
            id_au = curs.execute("SELECT id FROM Publication_type WHERE name=?", (public_type,)).fetchone()[0]
            curs.execute("SELECT id FROM Book WHERE id_publication_type=?", (id_au,))
            rows = curs.fetchall()
            for row in rows:
                curs.execute("SELECT * FROM Book WHERE id=?", (row[0],))
                row_books = curs.fetchall()
                for book in row_books:
                    text += self.book_search_by_name(book[1], book[0]) + '\n'
        except TypeError:
            text = "Книг з таким видом видавництва не знайдено\n"
        return text

    def book_search_by_date_of_public(self, date_of_public):
        text = ''
        conn = sqlite3.connect(self.name)
        curs = conn.cursor()
        try:
            curs.execute("SELECT id FROM Book WHERE date_of_public=?", (date_of_public,))
            rows = curs.fetchall()
            for row in rows:
                curs.execute("SELECT * FROM Book WHERE id=?", (row[0],))
                row_books = curs.fetchall()
                for book in row_books:
                    text += self.book_search_by_name(book[1], book[0]) + '\n'
        except TypeError:
            text = "Книг з такою датою випуску не знайдено\n"
        return text

    def book_search_by_location(self, bookcase, shelf=None):
        text = ''
        conn = sqlite3.connect(self.name)
        curs = conn.cursor()
        try:
            if shelf:
                id_loc = curs.execute("SELECT id FROM Storage_location WHERE bookcase = ? AND shelf = ?",
                                      [bookcase, shelf]).fetchall()
            else:
                id_loc = curs.execute("SELECT * FROM Storage_location WHERE bookcase = ?",
                                      (bookcase,)).fetchall()
            if len(id_loc) != 0:
                for id in id_loc:
                    curs.execute("SELECT id FROM Book WHERE id_location=?", (id[0],))
                    rows = curs.fetchall()
                    for row in rows:
                        curs.execute("SELECT * FROM Book WHERE id=?", (row[0],))
                        row_books = curs.fetchall()
                        for book in row_books:
                            text += self.book_search_by_name(book[1], book[0]) + '\n'
            else:
                text = 'Такого місця для зберігання немає\n'
        except TypeError:
            text = "Книг в даному місці зберігання не знайдено\n"
        return text


filename = 'library.db'  # файл БД довідника
rb = DBHomeLibrary(filename)

if __name__ == "__main__":
    while True:
        k = int(input('\t\tРежими роботи [1 - 2]:\n'
                      '\t1 - створення баз данних та введення книг\n'
                      'Введіть значення: '))
        if k == 1:  # створити довідник
            rb.createrb()
            print("\n------------------------------\n")
        else:
            rb.book_search_by_name('Купка')
            print("//////////////////////")
            rb.book_search_by_author('кукук')
            print("//////////////////////")
            rb.book_search_by_genre('Лірика')
            print('//////////////////////')
            # print(rb.book_search_by_publication_type('художня література'))
            print('//////////////////////')
            # print(rb.book_search_by_date_of_public('29.12.1989'))
            print('//////////////////////')
            # print(rb.book_search_by_location('дубова'))
