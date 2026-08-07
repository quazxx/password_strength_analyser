import re
from dataclasses import dataclass


@dataclass
class AnalysisResult:
    score: int
    level: str
    length: int
    has_lowercase: bool
    has_uppercase: bool
    has_digit: bool
    has_symbol: bool
    has_repetition: bool
    has_sequence: bool
    is_common: bool
    recommendations: list[str]
    

def has_sequence(password: str, sequence_length: int = 4) -> bool:
    password = password.lower()

    for i in range(len(password) - sequence_length + 1):
        chunk = password[i:i + sequence_length]

        increasing = all(
            ord(chunk[j + 1]) - ord(chunk[j]) == 1
            for j in range(len(chunk) - 1)
        )

        decreasing = all(
            ord(chunk[j]) - ord(chunk[j + 1]) == 1
            for j in range(len(chunk) - 1)
        )

        if increasing or decreasing:
            return True

    return False


def has_repetition(password: str) -> bool:
    return bool(re.search(r"(.)\1{2,}", password))


def calculate_character_variety(
    has_lowercase: bool,
    has_uppercase: bool,
    has_digit: bool,
    has_symbol: bool,
) -> int:

    variety = sum([
        has_lowercase,
        has_uppercase,
        has_digit,
        has_symbol,
    ])

    if variety == 4:
        return 3

    if variety == 3:
        return 2

    if variety == 2:
        return 1

    return 0


def calculate_penalty(
    password: str,
    has_repetition: bool,
    has_sequence: bool,
    is_common: bool,
) -> int:

    penalty = 0

    if has_repetition:
        penalty += 1

    if has_sequence:
        penalty += 1

    if is_common:
        penalty += 5

    return penalty


def get_level(score: int) -> str:
    if score <= 2:
        return "Очень слабый"
    if score <= 4:
        return "Слабый"
    if score <= 6:
        return "Средний"
    if score <= 8:
        return "Сильный"

    return "Очень сильный"


def analyze_password(
    password: str,
    common_passwords: set[str],
) -> AnalysisResult:

    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_symbol = any(not char.isalnum() for char in password)

    repetition = has_repetition(password)
    sequence = has_sequence(password)
    is_common = any([password.lower() == x for x in common_passwords])

    score = 0
    recommendations = []

    length = len(password)

    # Оценка длины
    if length >= 24:
        length_score = 6
    elif length >= 20:
        length_score = 5
    elif length >= 16:
        length_score = 4
    elif length >= 12:
        length_score = 3
    elif length >= 8:
        length_score = 2
    else:
        length_score = 0
        recommendations.append(
            "Увеличьте длину пароля минимум до 12 символов."
        )

    # Оценка разнообразия символов
    variety_score = calculate_character_variety(
        has_lowercase,
        has_uppercase,
        has_digit,
        has_symbol,
    )

    if not has_lowercase:
        recommendations.append("Добавьте строчные буквы.")

    if not has_uppercase:
        recommendations.append("Добавьте заглавные буквы.")

    if not has_digit:
        recommendations.append("Добавьте цифры.")

    if not has_symbol:
        recommendations.append("Добавьте специальные символы.")

    # Штраф за предсказуемость
    penalty = calculate_penalty(
        password,
        repetition,
        sequence,
        is_common,
    )

    if repetition:
        recommendations.append(
            "Избегайте повторения одного символа несколько раз подряд."
        )

    if sequence:
        recommendations.append(
            "Избегайте последовательностей вроде 1234 или abcd."
        )

    if is_common:
        recommendations.append(
            "Этот пароль находится в списке распространённых паролей."
        )

    score = length_score + variety_score - penalty

    score = max(0, min(score, 10))


    if not recommendations:
        recommendations.append(
            "Пароль соответствует основным проверкам."
        )

    return AnalysisResult(
        score=score,
        level=get_level(score),
        length=len(password),
        has_lowercase=has_lowercase,
        has_uppercase=has_uppercase,
        has_digit=has_digit,
        has_symbol=has_symbol,
        has_repetition=repetition,
        has_sequence=sequence,
        is_common=is_common,
        recommendations=recommendations,
    )
    



