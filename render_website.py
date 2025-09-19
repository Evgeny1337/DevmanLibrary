import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

PAGES_PATH = 'pages'
PAGE_ELEMENTS = 20
PAGE_COLUMNS = 2


def create_page(index, books, page_count):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    rows_of_books = list(chunked(books, PAGE_COLUMNS))
    template = env.get_template('template.html')
    next_number = index + 1
    previous_number = index - 1
    rendered_page = template.render(
        rows_of_books=rows_of_books,
        page_count=page_count,
        page_number=index,
        next_number=next_number,
        previous_number=previous_number)
    os.makedirs(PAGES_PATH, exist_ok=True)
    file_name = '{}/index{}.html'.format(PAGES_PATH, index)

    with open(file_name, 'w', encoding='utf8') as my_file:
        my_file.write(rendered_page)


def on_reload():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    meta_path = os.path.join(script_dir, 'meta_data.json')
    with open(meta_path, 'r') as my_file:
        books = json.load(my_file)
    for book in books:
        book['img_src'] = '../media/{}'.format(book['img_src'])
        book['book_path'] = '../media/{}'.format(book['book_path'])
        book['genres'] = book['genres'].split(',')
    book_pages = list(chunked(books, PAGE_ELEMENTS))
    page_count = len(book_pages)
    for index, book_page in enumerate(book_pages, start=1):
        create_page(index, book_page, page_count)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
