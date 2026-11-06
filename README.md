# Домашняя работа №4

Сервис на FastAPI для сбора и валидации обращений абонентов о технических проблемах с автоматическим сохранением отчетов на диск в формате JSON.

## Установка

Создайте виртуальное окружение и установите зависимости из `requirements.txt`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
uv run fastapi dev
```

Сервер будет доступен на http://127.0.0.1:8000.  

## Проверка

Все шаблоны запросов вынесены в каталог `examples/`. Для тестирования выполните команды в терминале из корневой папки проекта:

### 1. Успешный запрос (Несколько проблем, телефон с маской)
*Сервер вернет HTTP 201 Created, так как все данные валидны.*
```bash
curl -X POST http://127.0.0.1:8000/report/ \
  -H "Content-Type: application/json" \
  -d @examples/success_multiple_problems.json
```

### 2. Успешный запрос (Одна проблема, телефон слитно через "8")
*Сервер вернет HTTP 201 Created, так как все данные валидны.*
```bash
curl -X POST http://127.0.0.1:8000/report/ \
  -H "Content-Type: application/json" \
  -d @examples/success_single_problem.json
```

### 3. Успешный запрос (Указание даты инцидента с таймзоной)
*Сервер вернет HTTP 201 Created, так как валидатор корректно приводит aware-datetime к единому стандарту сравнения.*
```bash
curl -X POST http://127.0.0.1:8000/report/ \
  -H "Content-Type: application/json" \
  -d @examples/success_with_timezone.json
```

### 4. Тест ошибки: номер телефона содержит пробелы
*Сервер вернет HTTP 422 Unprocessable Entity, так как пробелы в номере телефона запрещены.*
```bash
curl -X POST http://127.0.0.1:8000/report/ \
  -H "Content-Type: application/json" \
  -d @examples/bad_request_invalid_phone.json
```

### 5. Тест ошибки: дата рождения в будущем
*Сервер вернет HTTP 422 Unprocessable Entity, так как дата рождения не может быть больше текущей даты.*
```bash
curl -X POST http://127.0.0.1:8000/report/ \
  -H "Content-Type: application/json" \
  -d @examples/bad_request_future_date.json
```

### 6. Тест ошибки: имя и фамилия написаны с маленькой буквы
*Сервер вернет HTTP 422 Unprocessable Entity, так как регулярное выражение требует заглавную букву в начале.*
```bash
curl -X POST http://127.0.0.1:8000/report/ \
  -H "Content-Type: application/json" \
  -d @examples/bad_request_lowercase_name.json
```

### 7. Тест ошибки: пустой список проблем
*Сервер вернет HTTP 422 Unprocessable Entity, так как параметр min_length требует хотя бы одну проблему.*
```bash
curl -X POST http://127.0.0.1:8000/report/ \
  -H "Content-Type: application/json" \
  -d @examples/bad_request_empty_problems.json
```

### 8. Тест ошибки: инцидент зафиксирован раньше даты рождения абонента
*Сервер вернет HTTP 422 Unprocessable Entity, так как кросс-валидатор не допустит регистрацию проблемы до рождения пользователя.*
```bash
curl -X POST http://127.0.0.1:8000/report/ \
  -H "Content-Type: application/json" \
  -d @examples/bad_request_problem_before_birth.json
```
