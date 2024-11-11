from Author import Author
from AuthorJSONHandler import AuthorJSONHandler
from Book import Book

authorZamyatin = Author(name="Evgeny Zamyatin", birthdate="01.02.1884")
bookZamyatin = Book(title="We", author=authorZamyatin, quantity=10, price=500.0)

authorJSONHandler = AuthorJSONHandler(filepath="C:/Users/germa/Desktop/authors.json")
authorJSONHandler.create(author=authorZamyatin)
