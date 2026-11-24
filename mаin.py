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
