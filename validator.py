import datetime


def validate_type(message):  # проверка типа
    if not isinstance(message, dict):
        return 'Запрос должен быть в формате словаря'
    else:
        return True


def validate_len(message):  # проверка длины
    if len(message) < 3:
        return 'В запросе не хватает данных'
    elif len(message) > 3:
        return 'В запросе есть лишние данные'
    else:
        return True


def validate_keys(message):  # проверка ключей
    try:  # dt_from
        message['dt_from']
    except KeyError:
        return "Ключ 'dt_from', в запросе, не найден"
    else:
        try:
            datetime.datetime.fromisoformat(message['dt_from'])
        except ValueError:
            return "Некорректная дата в ключе 'dt_from'"

    try:  # dt_upto
        message['dt_upto']
    except KeyError:
        return "Ключ 'dt_upto', в запросе, не найден"
    else:
        try:
            datetime.datetime.fromisoformat(message['dt_upto'])
        except ValueError:
            return "Некорректная дата в ключе 'dt_upto'"

    try:  # group_type
        message['group_type']
    except KeyError:
        return "Ключ 'group_type', в запросе, не найден"
    else:
        if message['group_type'] not in ('month', 'day', 'hour'):
            return ("Неверное значение ключа 'group_type'"
                    "\nДопустимые значения: ['month', 'day', 'hour']")

    return True


def validate_message(message):
    try:  # преобразуем str в dict
        message = eval(message)
    except Exception:
        return 'Ошибка в запросе'
    else:  # проверка типа
        validate_type_status = validate_type(message)
        if validate_type_status is not True:
            return validate_type_status
        else:  # проверка длины
            validate_len_status = validate_len(message)
            if validate_len_status is not True:
                return validate_len_status
            else:  # проверка ошибок в ключах
                validate_keys_status = validate_keys(message)
                if validate_keys_status is not True:
                    return validate_keys_status
                else:
                    return True
