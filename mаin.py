import random
FILE_NAME = "passwords.txt"
# разделитель полей записи в файле
SEPARATOR = "|" 
# проверочное слово для мастер-пароля         
CHECK_WORD = "PWVAULT"   
# минимальная длина мастер-пароля
MIN_KEY_LEN = 6          

LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
SYMBOLS = "!@#$%&*"

def enc(text, key):
    #Шифрует строку: код каждого символа увеличивается на код
    #символа ключа. Результат - числа через запятую
    codes = []
    for i in range(len(text)):
        # Циклически берём символы ключа с помощью остатка от деления
        shift = ord(key[i % len(key)])
        codes.append(str(ord(text[i]) + shift))
    return ",".join(codes)


def dec(text, key):
    #Расшифровывает строку, полученную из enc.
    #Если данные повреждены или ключ неверный, возвращает ''
    result = ""
    parts = text.split(",")
    for i in range(len(parts)):
        if not parts[i].isdigit():
            return ""
        code = int(parts[i]) - ord(key[i % len(key)])
        # Проверяем, что полученный код существует в таблице Unicode
        if code < 0 or code > 1114111:
            return ""
        result += chr(code)
    return result

def make_password(length):
    #Создаёт случайный пароль заданной длины (от 8 символов).
    #В пароле есть минимум по одному символу каждого вида.
    groups = [LOWER, UPPER, DIGITS, SYMBOLS]
    all_symbols = LOWER + UPPER + DIGITS + SYMBOLS
    chars = []
    # Сначала берём по одному случайному символу из каждой категории
    for group in groups:
        chars.append(random.choice(group))
    # Остальную длину добиваем случайными символами из общего набора
    while len(chars) < length:
        chars.append(random.choice(all_symbols))
    # Перемешиваем, чтобы первые 4 символа не шли в предсказуемом порядке
    random.shuffle(chars)
    return "".join(chars)

def check_strength(password):
    #Оценивает пароль: слабый, средний или сильный.
    # счётчик найденных категорий символов
    kinds = 0  
    # Проверяем наличие строчных, заглавных букв и цифр
    for group in (LOWER, UPPER, DIGITS):
        for symbol in password:
            if symbol in group:
                kinds += 1
                break
    # Проверяем наличие хотя бы одного спецсимвола
    for symbol in password:
        if symbol not in LOWER + UPPER + DIGITS:
            kinds += 1
            break

    if len(password) < 8 or kinds < 2:
        return "слабый"
    if len(password) < 12 or kinds < 4:
        return "средний"
    return "сильный"

def read_int(prompt, low, high):
    #Запрашивает целое число от low до high до тех пор,
    #пока пользователь не введёт верное значение.
    while True:
        text = input(prompt).strip()
        if not text.isdigit():
            print("Ошибка: нужно ввести целое число!")
            continue
        number = int(text)
        if low <= number <= high:
            return number
        print("Ошибка: число должно быть от", low, "до", high)


def read_text(prompt):
    #Запрашивает непустую строку без символа-разделителя.
    while True:
        # Считываем ввод и убираем пробелы по краям
        text = input(prompt).strip()
        if text == "":
            print("Ошибка: строка не может быть пустой!")
        elif SEPARATOR in text:
            # Запрещаем разделитель, чтобы не сломать структуру файла
            print("Ошибка: нельзя использовать символ", SEPARATOR)
        else:
            return text

def ask_password():
    #Спрашивает длину и возвращает сгенерированный пароль.
    length = read_int("Введите длину пароля (от 8 до 32): ", 8, 32)
    password = make_password(length)
    print("Сгенерированный пароль:", password)
    return password

def save(records, key):
    #Записывает в файл проверочную строку и все записи
    #(каждая запись - кортеж сайт, логин, пароль) в зашифрованном виде.
    file = open(FILE_NAME, "w", encoding="utf-8")
    # Первой строкой записываем зашифрованный маркер для проверки ключа
    file.write(enc(CHECK_WORD, key) + "\n")
    for record in records:
        line = SEPARATOR.join(record)
        file.write(enc(line, key) + "\n")
    file.close()


def load(key):
    #Читает записи из файла. Возвращает список кортежей
    #или None, если мастер-пароль неверный.
    file = open(FILE_NAME, "r", encoding="utf-8")
    lines = file.read().split("\n")
    file.close()

    # Сверяем расшифрованную первую строку с эталонным словом
    if dec(lines[0], key) != CHECK_WORD:
        return None

    records = []
    for line in lines[1:]:
        if line == "":
            continue
        # Расшифровываем строку и разрезаем по '|' на 3 элемента: сайт, логин, пароль
        parts = dec(line, key).split(SEPARATOR)
        if len(parts) == 3:
            records.append(tuple(parts))
        else:
            print("Повреждённая запись пропущена.")
    return records

def open_vault():
    #Создаёт новое или открывает существующее хранилище.
    #Возвращает кортеж (мастер-пароль, список записей) или None.
    # Открываем в режиме 'a', чтобы создать пустой файл при первом запуске
    open(FILE_NAME, "a").close()
    file = open(FILE_NAME, "r", encoding="utf-8")
    is_empty = file.read() == ""
    file.close()

    if is_empty:
        print("Хранилище не найдено. Создаём новое.")
        while True:
            key = input("Придумайте мастер-пароль (от 6 символов): ")
            if len(key) < MIN_KEY_LEN:
                print("Ошибка: слишком короткий мастер-пароль!")
            elif key != input("Повторите мастер-пароль: "):
                print("Ошибка: пароли не совпадают!")
            else:
                save([], key)
                return key, []

    # Даём пользователю 3 попытки на ввод правильного мастер-пароля
    for attempt in range(1, 4):
        key = input("Введите мастер-пароль: ")
        if len(key) >= MIN_KEY_LEN:
            records = load(key)
            if records is not None:
                return key, records
        print("Неверный мастер-пароль (попытка", attempt, "из 3)")
    return None

def add(records, key):
    #Добавляет запись со своим или сгенерированным паролем.
    site = read_text("Введите название сайта: ")
    login = read_text("Введите логин: ")
    # Проверяем дубликаты по паре (сайт + логин)
    for old_site, old_login, old_password in records:
        if old_site.lower() == site.lower() and old_login == login:
            print("Такая запись уже есть!")
            return
    answer = input("Сгенерировать пароль автоматически? (д/н): ")
    if answer.strip().lower() == "д":
        password = ask_password()
    else:
        password = read_text("Введите свой пароль: ")
        print("Надёжность:", check_strength(password))
    # Добавляем новую запись в виде кортежа в общий список и сразу сохраняем в файл    
    records.append((site, login, password))
    save(records, key)
    print("Запись добавлена и сохранена!")


def show(records):
    #Выводит таблицу записей, пароли скрыты звёздочками.
    if len(records) == 0:
        print("Список записей пуст")
        return
    # Выравниваем столбцы таблицы с помощью ljust()
    print("№".ljust(4) + "Сайт".ljust(22) + "Логин".ljust(22) + "Пароль")
    for i in range(len(records)):
        site, login, password = records[i]
        print(str(i + 1).ljust(4) + site[:21].ljust(22)
              + login[:21].ljust(22) + "*" * len(password))

def main():
    #Главная функция: цикл консольного меню.
    print("==== Защищённый менеджер паролей ====")
    vault = open_vault()
    if vault is None:
        print("Доступ запрещён")
        return
    key, records = vault

    while True:
        print("\n==== Менеджер паролей ====")
        print("1. Сгенерировать пароль")
        print("2. Добавить запись в хранилище")
        print("3. Показать все записи")
        print("4. Найти пароль по сайту")
        print("5. Удалить запись")
        print("6. Показать пароль по номеру записи")
        print("0. Выход")
        choice = read_int("Выберите действие: ", 0, 6)
        if choice == 0:
            print("Программа завершена")
            break
        else:
            print("Функция в разработке...")


if __name__ == "__main__":
    main()
