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


def main():
    #Главная функция: цикл консольного меню.
    print("==== Защищённый менеджер паролей ====")

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
