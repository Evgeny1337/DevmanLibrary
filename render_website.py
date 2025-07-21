from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
from livereload import Server
import json



def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    with open("meta_data.json", "r") as my_file:
        books_json = my_file.read()

    books = json.loads(books_json)
    rows_of_books = list(chunked(books, 2))
    template = env.get_template('template.html')
    rendered_page = template.render(rows_of_books=rows_of_books)

    with open("index.html", "w", encoding='utf8') as my_file:
        my_file.write(rendered_page)

def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')



if __name__ == '__main__':
    main()