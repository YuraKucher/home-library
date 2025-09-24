# 📚 Home Library Manager

### Програма з графічним інтерфейсом для ведення домашньої бібліотеки.

## 🚀 Функціонал

### 1. Додавання нових видань (книг, періодичних видань).
### 2. Редагування та видалення даних за допомогою ID книги:
#### - назви
#### - дати випуску
#### - авторів (один або кілька)
#### - жанрів (один або кілька)
#### - виду видання (підручник, художня література, науково-технічне тощо)
#### - шафа збереження
#### - полиця
### 3. Пошук видань за:
#### - назвою (одна або кілька)
#### - датою випуску (одна або кілька)
#### - автором (один або кілька)
#### - жанром (один або кілька)
#### - видом видання (один або кілька)
#### - шафа збереження (одна або кілька)
#### - полиця (одна або кілька)

## 🗄️ Структура проєкту

#### - home_library.py — головний файл, що реалізує роботу з базою даних (CRUD-операції).

#### - graphics.py — графічний інтерфейс (GUI), через який користувач взаємодіє з бібліотекою.

## 🛠️ Використані технології

#### Python

#### QLite (база даних)

#### Tkinter (графічний інтерфейс)

## 📸 Скриншоти

<img width="1600" height="543" alt="image" src="https://github.com/user-attachments/assets/abe8f420-8251-4c88-a490-a4e1692e1e85" />

## 🗄️ Структура бази даних

### Основні таблиці:

#### Book — книги та періодичні видання.

#### Publication_type — типи видань.

#### Author — автори.

#### Genre — жанри.

#### Book_Authors — зв’язок книг та авторів (many-to-many).

#### Book_Genres — зв’язок книг та жанрів (many-to-many).

#### Storage_location — місця зберігання (шафа, полиця).
<details> <summary>Приклад SQL-схеми</summary>
CREATE TABLE IF NOT EXISTS Book (
  
    id INTEGER PRIMARY KEY, 
    name VARCHAR(100),
    date_of_public VARCHAR(40),
    id_publication_type INTEGER,
    id_location INTEGER
    
);

CREATE TABLE IF NOT EXISTS Publication_type (

    id INTEGER PRIMARY KEY, 
    name VARCHAR(80)
    
);

CREATE TABLE IF NOT EXISTS Author (

    id INTEGER PRIMARY KEY, 
    name VARCHAR(100)
    
);

CREATE TABLE IF NOT EXISTS Genre (

    id INTEGER PRIMARY KEY, 
    name VARCHAR(100)
    
);

CREATE TABLE IF NOT EXISTS Book_Authors (

    id INTEGER PRIMARY KEY, 
    book_id INTEGER,
    author_id INTEGER,
    FOREIGN KEY (book_id) REFERENCES Book(id),
    FOREIGN KEY (author_id) REFERENCES Author(id)
    
);

CREATE TABLE IF NOT EXISTS Book_Genres (

    id INTEGER PRIMARY KEY, 
    book_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY (book_id) REFERENCES Book(id),
    FOREIGN KEY (genre_id) REFERENCES Genre(id)
    
);

CREATE TABLE IF NOT EXISTS Storage_location (

    id INTEGER PRIMARY KEY, 
    bookcase VARCHAR(40),
    shelf VARCHAR(40)
    
);
</details>

## ✅ Майбутні покращення
#### Більш сучасний і зручний інтерфейс
#### Можливість редагування без введення ID (через список або таблицю)
#### Імпорт/експорт даних
#### Підтримка інших форматів бази даних
#### Покращений редактор даних
#### Покращене видалення

### *Підчас першого запуску можна через консоль створити базу даних та ввести одразу книг(у\и)
<img width="838" height="188" alt="image" src="https://github.com/user-attachments/assets/23620f03-f27d-4c1e-9af8-2600bdb8b65e" />
