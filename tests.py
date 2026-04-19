from main import BooksCollector
import pytest

class TestBooksCollector:

    # 1. Добавление книг (позитивный и граничные случаи)
    @pytest.mark.parametrize("name", [
        "Нормальное название",
        "A" * 40,               # максимальная длина 40
        "Книга"                 # короткое имя
    ])
    def test_add_new_book_valid_name(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.get_books_genre()
        # У новой книги жанр должен быть пустой строкой
        assert collector.get_book_genre(name) == ""

    @pytest.mark.parametrize("invalid_name", [
        "",                     # пустая строка
        "A" * 41,               # 41 символ
        None                    # не строка (но метод отработает без ошибки)
    ])
    def test_add_new_book_invalid_name(self, invalid_name):
        collector = BooksCollector()
        collector.add_new_book(invalid_name)
        # Книга не должна добавиться
        assert invalid_name not in collector.get_books_genre()

    def test_add_new_book_duplicate(self):
        collector = BooksCollector()
        collector.add_new_book("Дубровский")
        collector.add_new_book("Дубровский")   # повтор
        # Словарь должен содержать только одну запись
        assert len(collector.get_books_genre()) == 1

    # 2. Установка и получение жанра
    def test_set_book_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Мертвые души")
        collector.set_book_genre("Мертвые души", "Детективы")
        assert collector.get_book_genre("Мертвые души") == "Детективы"

    def test_set_book_genre_for_nonexistent_book(self):
        collector = BooksCollector()
        collector.set_book_genre("Неизвестная книга", "Фантастика")
        # Книги нет в словаре, жанр не установится
        assert collector.get_book_genre("Неизвестная книга") is None

    def test_set_book_genre_invalid_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", "Роман")  # Роман не в списке genre
        assert collector.get_book_genre("Гарри Поттер") == ""  # жанр не изменился

    # 3. Получение списка книг по жанру
    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Книга1"]),
        ("Ужасы", []),
        ("Комедии", ["Книга2", "Книга3"]),
    ])
    def test_get_books_with_specific_genre(self, genre, expected_books):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.set_book_genre("Книга1", "Фантастика")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга2", "Комедии")
        collector.add_new_book("Книга3")
        collector.set_book_genre("Книга3", "Комедии")
        assert collector.get_books_with_specific_genre(genre) == expected_books

    # 4. Получение словаря всех книг
    def test_get_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book("КнигаA")
        collector.set_book_genre("КнигаA", "Ужасы")
        collector.add_new_book("КнигаB")
        expected = {"КнигаA": "Ужасы", "КнигаB": ""}
        assert collector.get_books_genre() == expected

    # 5. Книги для детей (без возрастного рейтинга)
    def test_get_books_for_children(self):
        collector = BooksCollector()
        collector.add_new_book("Детская книга")
        collector.set_book_genre("Детская книга", "Мультфильмы")  # без рейтинга
        collector.add_new_book("Страшная книга")
        collector.set_book_genre("Страшная книга", "Ужасы")       # с рейтингом
        collector.add_new_book("Без жанра")                      # жанр не установлен
        children_books = collector.get_books_for_children()
        assert "Детская книга" in children_books
        assert "Страшная книга" not in children_books
        assert "Без жанра" not in children_books

    # 6. Добавление в избранное
    def test_add_book_in_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Любимая книга")
        collector.add_book_in_favorites("Любимая книга")
        assert "Любимая книга" in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_twice(self):
        collector = BooksCollector()
        collector.add_new_book("Дубль")
        collector.add_book_in_favorites("Дубль")
        collector.add_book_in_favorites("Дубль")   # повторное добавление
        # В списке favourites книга должна быть один раз
        assert collector.get_list_of_favorites_books().count("Дубль") == 1

    def test_add_book_in_favorites_not_in_books_genre(self):
        collector = BooksCollector()
        collector.add_book_in_favorites("Нет такой книги")
        assert collector.get_list_of_favorites_books() == []

    # 7. Удаление из избранного
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Удаляемая книга")
        collector.add_book_in_favorites("Удаляемая книга")
        assert "Удаляемая книга" in collector.get_list_of_favorites_books()
        collector.delete_book_from_favorites("Удаляемая книга")
        assert "Удаляемая книга" not in collector.get_list_of_favorites_books()

    def test_delete_nonexistent_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        initial_favorites = collector.get_list_of_favorites_books().copy()
        collector.delete_book_from_favorites("Чужой")
        assert collector.get_list_of_favorites_books() == initial_favorites

    # 8. Получение списка избранных книг
    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_book_in_favorites("Книга1")
        collector.add_book_in_favorites("Книга2")
        assert collector.get_list_of_favorites_books() == ["Книга1", "Книга2"]

    # 9. Комбинированный тест: у новой книги нет жанра
    def test_new_book_has_empty_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Пустая")
        assert collector.get_book_genre("Пустая") == ""