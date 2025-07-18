from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
with open("meta_data.json", "r") as my_file:
    books_json = my_file.read()

books = json.loads(books_json)

template = env.get_template('template.html')
rendered_page = template.render(books=books)

with open("index.html", "w", encoding='utf8') as my_file:
    my_file.write(rendered_page)
