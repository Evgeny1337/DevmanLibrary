import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

PAGES_PATH = "pages"


def create_page(index, books, page_count):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    page_number = index + 1
    rows_of_books = list(chunked(books, 2))
    template = env.get_template('template.html')
    next_number = page_number + 1
    previous_number = page_number - 1
    rendered_page = template.render(
        rows_of_books=rows_of_books,
        page_count=page_count,
        page_number=page_number,
        next_number=next_number,
        previous_number=previous_number)
    os.makedirs(PAGES_PATH, exist_ok=True)
    file_name = '{}/index{}.html'.format(PAGES_PATH, page_number)

    with open(file_name, "w", encoding='utf8') as my_file:
        my_file.write(rendered_page)


def on_reload():
    with open("meta_data.json", "r") as my_file:
        books_json = my_file.read()
    books = json.loads(books_json)
    for book in books:
        book['img_src'] = '../{}'.format(book['img_src'])
        book['book_path'] = '../{}'.format(book['book_path'])
    book_pages = list(chunked(books, 20))
    page_count = len(book_pages)
    for index, book_page in enumerate(book_pages):
        create_page(index, book_page, page_count)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
