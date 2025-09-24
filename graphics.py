import tkinter as tk

from home_library import *

filename = 'library.db'  # файл БД довідника
rb = DBHomeLibrary(filename)


def display_text(text, x=200, y=300, size=8, color="red"):

    text_var = tk.StringVar()

    label = tk.Label(root, textvariable=text_var, font=("Arial", size), fg=color)

    label.place(x=x, y=y, )

    text_var.set(text)

    def update_text(new_text):
        text_var.set(new_text)

    return update_text


def add_book_button_clicked():
    name_book = str(name_book_entry.get())
    list_authors = str(list_authors_entry.get())
    list_genre = str(list_genre_entry.get())
    publication_type = str(publication_type_entry.get())
    date_of_public = str(date_of_public_entry.get())
    bookcase = str(bookcase_entry.get())
    shelf = str(shelf_entry.get())
    print(name_book, list_authors, list_genre, publication_type, date_of_public, bookcase, shelf)
    rb.add_book(name_book, list_authors, list_genre, publication_type, date_of_public, bookcase, shelf)
    update_text("Дані оброблено")


def book_search_by_name_button_clicked():
    text = ''
    name_books = str(name_book_entry.get())
    for book in name_books.split(','):
        book = book.lstrip(' ')
        if len(book.split()) != 0:
            text += book + '\n' + rb.book_search_by_name(book)
    update_text(text)


def book_search_by_genre_button_clicked():
    text = ''
    list_genres = str(list_genre_entry.get())
    for genre in list_genres.split(','):
        genre = genre.lstrip(' ')
        if len(genre.split()) != 0:
            text += f'Жанр: {genre}\n{rb.book_search_by_genre(genre)}'
    update_text(text)


def book_search_by_author_button_clicked():
    text = ''
    list_authors = str(list_authors_entry.get())
    for a in list_authors.split(','):
        a = a.lstrip(' ')
        if len(a.split()) != 0:
            text += f'Автор: {a}\n{rb.book_search_by_author(a)}'
    update_text(text)


def book_search_by_publication_type_button_clicked():
    text = ''
    publication_types = str(publication_type_entry.get())
    for p in publication_types.split(','):
        p = p.lstrip(' ')
        if len(p.split()) != 0:
            text += p + '\n' + rb.book_search_by_publication_type(p)
    update_text(text)


def book_search_by_date_button_clicked():
    text = ''
    date_of_publics = str(date_of_public_entry.get())
    for d in date_of_publics.split(','):
        d = d.lstrip(' ')
        if len(d.split()) != 0:
            text += f'Дата: {d}\n{rb.book_search_by_date_of_public(d)}'
    update_text(text)


def book_search_by_bookcase_button_clicked():
    text = ''
    bookcases = str(bookcase_entry.get())
    for bc in bookcases.split(','):
        bc = bc.lstrip(' ')
        if len(bc.split()) != 0:
            text += f'Шафа = {bc}\n{rb.book_search_by_location(bc)}'
    update_text(text)


def book_search_by_shelf_button_clicked():
    text = ''
    bookcases = str(bookcase_entry.get())
    shelfs = str(shelf_entry.get())
    for bc in bookcases.split(','):
        bc = bc.lstrip(' ')
        if len(bc.split()) != 0:
            for sh in shelfs.split(','):
                sh = sh.lstrip(' ')
                if len(sh.split()) != 0:
                    text += f"Шафа = {bc}; Полиця = {sh}\n{rb.book_search_by_location(bc, sh)}"
    update_text(text)


def change_book_button_clicked():
    id_book = str(id_book_entry.get())
    name_book = str(name_book_entry.get())
    list_authors = str(list_authors_entry.get())
    list_genre = str(list_genre_entry.get())
    publication_type = str(publication_type_entry.get())
    date_of_public = str(date_of_public_entry.get())
    bookcase = str(bookcase_entry.get())
    shelf = str(shelf_entry.get())
    if len(name_book.split()) == 0:
        name_book = None
    if len(publication_type.split()) == 0:
        publication_type = None
    if len(list_authors.split()) == 0:
        list_authors = None
    if len(list_genre.split()) == 0:
        list_genre = None
    if len(date_of_public.split()) == 0:
        date_of_public = None
    if len(bookcase.split()) == 0:
        bookcase = None
    if len(shelf.split()) == 0:
        shelf = None
    print(name_book, list_authors, list_genre, publication_type, date_of_public, bookcase, shelf)
    rb.change_book(id_book, name_book, list_authors, list_genre, publication_type, date_of_public, bookcase, shelf)
    update_text("Зміни внесено")


root = tk.Tk()
root.title("Home Library")
root.geometry("1600x400")

# Create labels
tk.Label(root, text="Назва книги:").grid(row=0, column=0)
tk.Label(root, text="Автор/(и):").grid(row=0, column=1)
tk.Label(root, text="Жанр/(и) :").grid(row=0, column=2)
tk.Label(root, text="Вид видавництва:").grid(row=0, column=3)
tk.Label(root, text="Дата випуску:").grid(row=0, column=4)
tk.Label(root, text="Шафа:").grid(row=0, column=5)
tk.Label(root, text="Полиця:").grid(row=0, column=6)

# Вікна першого рівня

name_book_entry = tk.Entry(root)
name_book_entry.grid(row=1, column=0, padx=2)
list_authors_entry = tk.Entry(root)
list_authors_entry.grid(row=1, column=1, padx=2)
list_genre_entry = tk.Entry(root)
list_genre_entry.grid(row=1, column=2, padx=2)
publication_type_entry = tk.Entry(root)
publication_type_entry.grid(row=1, column=3, padx=2)
date_of_public_entry = tk.Entry(root)
date_of_public_entry.grid(row=1, column=4, padx=2)
bookcase_entry = tk.Entry(root)
bookcase_entry.grid(row=1, column=5, padx=2)
shelf_entry = tk.Entry(root)
shelf_entry.grid(row=1, column=6, padx=2)

# Вікна другого рівня
id_book_entry = tk.Entry(root)
id_book_entry.grid(row=10, column=0, padx=25)
tk.Label(root, text="ID:").grid(row=9, column=0)

# Кнопки першого рівня

add_book_button = tk.Button(root, text="Додати книгу", command=add_book_button_clicked, activebackground='blue')
add_book_button.grid(row=7, column=0, pady=10)

book_search_by_name_button = tk.Button(root, text="Знайти книгу за назв(ою)/(ами)",
               command=book_search_by_name_button_clicked, activebackground='blue')
book_search_by_name_button.grid(row=8, column=0)

book_search_by_author_button = tk.Button(root, text="Знайти книгу за автор(ом)/(ами)",
                 command=book_search_by_author_button_clicked, activebackground='blue')
book_search_by_author_button.grid(row=8, column=1)
tk.Label(root, text="Введіть авторів через кому\n"
                    "Наприклад 'Тарас Шевченко, Леся Українка'").grid(row=7, column=1)

book_search_by_genre_button = tk.Button(root, text="Знайти книгу за жанр(ом)/(ами)",
                command=book_search_by_genre_button_clicked, activebackground='blue')
book_search_by_genre_button.grid(row=8, column=2)
tk.Label(root, text="Введіть жанри через кому\nНаприклад 'Романтика, Лірика'").grid(row=7, column=2)

book_search_by_publication_type_button = tk.Button(root, text="Знайти книгу за вид(ом)/(ами)",
              command=book_search_by_publication_type_button_clicked, activebackground='blue')
book_search_by_publication_type_button.grid(row=8, column=3)
tk.Label(root, text="Введіть види через кому\nНаприклад 'Підручник, художня література'").grid(row=7, column=3)

book_search_by_date_button = tk.Button(root, text="Знайти книгу за дат(ою)/(ами)",
              command=book_search_by_date_button_clicked, activebackground='blue')
book_search_by_date_button.grid(row=8, column=4)
tk.Label(root, text="Введіть дати через кому у форматі dd.mm.yyyy\n"
                    "Наприклад '12.12.1900, 10.12.2003'").grid(row=7, column=4)

book_search_by_bookcase_button = tk.Button(root, text="Знайти книгу за шаф(ою)/(ами)",
              command=book_search_by_bookcase_button_clicked, activebackground='blue')
book_search_by_bookcase_button.grid(row=8, column=5)
tk.Label(root, text="Введіть шафи через кому\nНаприклад 'купе, дубова'").grid(row=7, column=5)

book_search_by_shelf_button = tk.Button(root, text="Знайти книгу за полиц(ею)/(ями)",
                command=book_search_by_shelf_button_clicked, activebackground='blue')
book_search_by_shelf_button.grid(row=8, column=6)
tk.Label(root, text="Введіть полиці через кому\nНаприклад '4, 2'").grid(row=7, column=6)

# Кнопки другого рівня

change_book_button = tk.Button(root, text="Змінити дані", command=change_book_button_clicked)
change_book_button.grid(row=9, column=1, pady=10)
tk.Label(root, text="Будуть внесені зміни до полів з введеними даними.\n"
                    "Якщо якесь поле пусте, то його данні залишаться без змін\n"
                    "Якщо книги з таким ID немає, то нічого не відбудеться").grid(row=10, column=1, pady=10)

update_text = display_text("Тут буде з'являтися інформація після натискання відповідних кнопок")


root.mainloop()