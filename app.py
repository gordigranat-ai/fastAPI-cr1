# app.py
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
    from typing import Dict, Any
    import uvicorn
except ModuleNotFoundError as e:
    print("="*50)
    print("ОШИБКА: Не установлены необходимые пакеты!")
    print("="*50)
    print(f"Детали: {e}")
    print("\nДля установки выполните команду:")
    print("pip install fastapi uvicorn")
    print("\nИли если используете виртуальное окружение:")
    print("python -m venv venv")
    print("venv\\Scripts\\activate  # для Windows")
    print("pip install fastapi uvicorn")
    print("="*50)
    exit(1)

# Импортируем модели и хранилище из models.py
try:
    from models import User, UserWithAge, Feedback, feedbacks
except ModuleNotFoundError:
    print("="*50)
    print("ОШИБКА: Файл models.py не найден!")
    print("Убедитесь, что файл models.py находится в той же папке, что и app.py")
    print("="*50)
    exit(1)

# Задание 1.1: Создание FastAPI-приложения
application = FastAPI(title="Контрольная работа №1", description="Технологии разработки серверных приложений")

# Задание 1.1: Корневой маршрут с JSON-ответом
@application.get("/")
async def root():
    """
    Возвращает приветственное сообщение.
    Для проверки авторелоада можно изменить сообщение на:
    {"message": "Авторелоад действительно работает"}
    """
    return {"message": "Добро пожаловать в моё приложение FastAPI!"}

# Задание 1.2: Возврат HTML-страницы
@application.get("/html", response_class=HTMLResponse)
async def get_html_page():
    """
    Возвращает HTML-страницу из файла index.html
    """
    try:
        return FileResponse("index.html")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="HTML файл не найден")

@application.get("/page", response_class=HTMLResponse)
async def get_html_page_alt():
    """
    Альтернативный маршрут для HTML страницы
    """
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head><title>Ошибка</title></head>
        <body>
            <h1>Файл index.html не найден</h1>
            <p>Создайте файл index.html в корневой папке проекта</p>
        </body>
        </html>
        """, status_code=404)

# Задание 1.3: POST-запрос для сложения двух чисел
@application.post("/calculate")
async def calculate_numbers(num1: float = 0, num2: float = 0):
    """
    Принимает два числа и возвращает их сумму.
    """
    result = num1 + num2
    return {"num1": num1, "num2": num2, "sum": result}

# Задание 1.4: GET-запрос для получения пользователя
@application.get("/users")
async def get_user():
    """
    Возвращает данные пользователя из модели User
    """
    user = User(name="Коломоец Гордей", id=1)
    return user

# Задание 1.5: POST-запрос для проверки совершеннолетия
@application.post("/user")
async def check_adult(user: UserWithAge):
    """
    Принимает пользователя с именем и возрастом,
    возвращает те же данные + поле is_adult
    """
    user_data = user.model_dump()
    user_data["is_adult"] = user.age >= 18
    return user_data

# Задание 2.1 и 2.2: POST-запрос для сохранения отзыва
@application.post("/feedback")
async def create_feedback(feedback: Feedback):
    """
    Сохраняет отзыв пользователя в список feedbacks
    """
    feedbacks.append(feedback)
    return {
        "message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён.",
        "total_feedbacks": len(feedbacks)
    }

@application.get("/feedbacks")
async def get_all_feedbacks():
    """
    Возвращает список всех отзывов
    """
    return {"feedbacks": feedbacks, "count": len(feedbacks)}

# Точка входа для запуска приложения
if __name__ == "__main__":
    print("="*50)
    print("Запуск FastAPI приложения")
    print("="*50)
    print("Доступные маршруты:")
    print("  GET  /         - Главная страница (JSON)")
    print("  GET  /html     - HTML страница")
    print("  GET  /page     - Альтернативная HTML страница")
    print("  POST /calculate?num1=5&num2=3 - Сложение чисел")
    print("  GET  /users    - Информация о пользователе")
    print("  POST /user     - Проверка совершеннолетия")
    print("  POST /feedback - Отправка отзыва")
    print("  GET  /feedbacks - Просмотр всех отзывов")
    print("="*50)
    print("Документация:")
    print("  Swagger UI: http://127.0.0.1:8000/docs")
    print("  ReDoc: http://127.0.0.1:8000/redoc")
    print("="*50)
    
    uvicorn.run(
        "app:application",
        host="127.0.0.1",
        port=8000,
        reload=True
    )