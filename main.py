from pathlib import Path

from analyser import analyze_password


def load_common_passwords(filename: str) -> set[str]:
    path = Path(filename)

    if not path.exists():
        return set()

    with path.open("r", encoding="utf-8") as file:
        return {
            line.strip().lower()
            for line in file
            if line.strip()
        }


def print_header() -> None:
    print()
    print("================================================")
    print("|         PASSWORD STRENGTH ANALYZER           |")
    print("================================================")
    print()


def print_check(name: str, value: bool) -> None:
    status = "YES" if value else "NO"
    print(f"{name:<25} {status}")


def main() -> None:
    print_header()

    common_passwords = load_common_passwords(
        "common_passwords.txt"
    )

    password = input("Введите пароль: ")

    if not password:
        print("\nПароль не может быть пустым.")
        return

    result = analyze_password(
        password,
        common_passwords,
    )

    print()
    print("────────────────────────────────────────────────")
    print("АНАЛИЗ")
    print("────────────────────────────────────────────────")

    print(f"Длина:                   {result.length}")

    print_check(
        "Строчные буквы:",
        result.has_lowercase,
    )

    print_check(
        "Заглавные буквы:",
        result.has_uppercase,
    )

    print_check(
        "Цифры:",
        result.has_digit,
    )

    print_check(
        "Спецсимволы:",
        result.has_symbol,
    )

    print_check(
        "Повторения:",
        result.has_repetition,
    )

    print_check(
        "Последовательности:",
         result.has_sequence,
    )

    print_check(
        "Распространённый:",
        result.is_common,
    )

    print()
    print(f"Оценка:                  {result.score}/10")
    print(f"Уровень:                 {result.level}")

    print()
    print("────────────────────────────────────────────────")
    print("РЕКОМЕНДАЦИИ")
    print("────────────────────────────────────────────────")

    for recommendation in result.recommendations:
        print(f"• {recommendation}")


if __name__ == "__main__":
    main()