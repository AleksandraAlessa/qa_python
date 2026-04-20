from main import BooksCollector
import pytest

class TestBooksCollector:

    # 1. Добавление новой книги в жанр
    @pytest.mark.parametrize("name", [
        "Нормальное название",
        "A" * 40,               # максимальная длина 40
        "Книга"                 # короткое имя
    ])
    def test_add_new_book_adds_to_books_genre(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.get_books_genre()

    # 2. Проверка на отсутвие жанра у новой книги
    @pytest.mark.parametrize("name", [
    "Нормальное название",
    "A" * 40,
    "Книга"
    ])
    def test_new_book_has_empty_genre_after_adding(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert collector.get_book_genre(name) == ""
        
     # 3. Проверка добавления новой книги с некорректным названием   
    @pytest.mark.parametrize("invalid_name", [
        "",                     # пустая строка
        "A" * 41,               # 41 символ
        
    ])
    def test_add_new_book_invalid_name(self, invalid_name):
        collector = BooksCollector()
        collector.add_new_book(invalid_name)
        # Книга не должна добавиться
        assert invalid_name not in collector.get_books_genre()
    
    # 4.Проверка на дубликат 
    def test_add_new_book_duplicate(self):
        collector = BooksCollector()
        collector.add_new_book("Дубровский")
        collector.add_new_book("Дубровский")   # повтор
        # Словарь должен содержать только одну запись
        assert len(collector.get_books_genre()) == 1

    # 5. Проверка жанра существующей книги
    def test_set_book_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Мертвые души")
        collector.set_book_genre("Мертвые души", "Детективы")
        assert collector.get_book_genre("Мертвые души") == "Детективы"

    # 6. Проверка жанра для несуществующей книги
    def test_set_book_genre_for_nonexistent_book(self):
        collector = BooksCollector()
        collector.set_book_genre("Неизвестная книга", "Фантастика")
        # Книги нет в словаре, жанр не установится
        assert collector.get_book_genre("Неизвестная книга") is None
    
    # 7. Проверка на недопустимый жанр
    def test_set_book_genre_invalid_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", "Роман")  # Роман не в списке genre
        assert collector.get_book_genre("Гарри Поттер") == ""  # жанр не изменился

    # 8. Получение списка книг по жанру
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

    # 9. Получение словаря всех книг
    def test_get_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book("КнигаA")
        collector.set_book_genre("КнигаA", "Ужасы")
        collector.add_new_book("КнигаB")
        expected = {"КнигаA": "Ужасы", "КнигаB": ""}
        assert collector.get_books_genre() == expected

    # 10. Проверка книги на детский жанр
    def test_child_friendly_genre_included_in_children_list(self):
        collector = BooksCollector()
        collector.add_new_book("Детская книга")
        collector.set_book_genre("Детская книга", "Мультфильмы")
        children_books = collector.get_books_for_children()
        assert "Детская книга" in children_books
    
    # 11. Проверка книги на соответствие возрастному жанру
    def test_age_restricted_genre_excluded_from_children_list(self):
        collector = BooksCollector()
        collector.add_new_book("Страшная книга")
        collector.set_book_genre("Страшная книга", "Ужасы")
        children_books = collector.get_books_for_children()
        assert "Страшная книга" not in children_books
    
    # 12. Проверка, что книга без жанра не попадает в жанр книг для детей
    def test_book_without_genre_not_in_children_list(self):
        collector = BooksCollector()
        collector.add_new_book("Без жанра")
        children_books = collector.get_books_for_children()
        assert "Без жанра" not in children_books

    # 13. Добавление в избранное
    def test_add_book_in_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Любимая книга")
        collector.add_book_in_favorites("Любимая книга")
        assert "Любимая книга" in collector.get_list_of_favorites_books()
    
    # 14. Проверка, что при повторном добавлении книги в избранное она не дублируется в списке
    def test_add_book_in_favorites_twice(self):
        collector = BooksCollector()
        collector.add_new_book("Дубль")
        collector.add_book_in_favorites("Дубль")
        collector.add_book_in_favorites("Дубль")   # повторное добавление
        # В списке favourites книга должна быть один раз
        assert collector.get_list_of_favorites_books().count("Дубль") == 1
    
    # 15. Проверяем, что нельзя добавить в избранное книгу, которой нет в общей коллекции книг  
    def test_add_book_in_favorites_not_in_books_genre(self):
        collector = BooksCollector()
        collector.add_book_in_favorites("Нет такой книги")
        assert collector.get_list_of_favorites_books() == []

    # 16.Проверяем, что существующую книгу можно успешно добавить в список избранного.
    def test_add_book_to_favorites_success(self):
        collector = BooksCollector()
        collector.add_new_book("Удаляемая книга")
        collector.add_book_in_favorites("Удаляемая книга")
        assert "Удаляемая книга" in collector.get_list_of_favorites_books()
   
    # 17. Проверяем, что книгу можно успешно удалить из списка избранного, и после удаления она в этом списке отсутствует. 
    def test_delete_book_from_favorites_removes_it(self):
        collector = BooksCollector()
        collector.add_new_book("Удаляемая книга")
        collector.add_book_in_favorites("Удаляемая книга")
        collector.delete_book_from_favorites("Удаляемая книга")
        assert "Удаляемая книга" not in collector.get_list_of_favorites_books()

    # 18. Проверяем удаление не существующей книги из списка
    def test_delete_nonexistent_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        initial_favorites = collector.get_list_of_favorites_books().copy()
        collector.delete_book_from_favorites("Чужой")
        assert collector.get_list_of_favorites_books() == initial_favorites

    # 19. Получение списка избранных книг
    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_book_in_favorites("Книга1")
        collector.add_book_in_favorites("Книга2")
        assert collector.get_list_of_favorites_books() == ["Книга1", "Книга2"]

    # 20. Проверяем у новой книги нет жанра
    def test_new_book_has_empty_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Пустая")
        assert collector.get_book_genre("Пустая") == ""