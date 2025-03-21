# Telegram Tickets Bot ⚠️ Архивировано  
[![No Maintenance](https://img.shields.io/badge/Status-Archived-red)](https://github.com/UNVISLATE/Telegram-Tickets-bot)  

Бот для создания и управления тикетами в Telegram через топики чата. Позволяет пользователям отправлять запросы поддержки, которые преобразуются в отдельные темы в указанном чате.  

**Важно:**
Проект больше не поддерживается. Бот функционирует, но кодовая база требует рефакторинга (наличие "технического долга"). Рекомендуется форкнуть репозиторий и адаптировать под свои нужды.  

---
## Лицензия  
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)  

Проект распространяется под лицензией **Apache 2.0**.  
- Вы можете свободно использовать, модифицировать и распространять код.  
- **Обязательно сохраняйте упоминание авторства** в исходниках.  
- Любые патенты, связанные с улучшениями проекта, автоматически доступны всем пользователям.
---
## Технологии  
- Python 3.8+  
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)  
- Топики Telegram  
---
## Настройка  
1. **Установите зависимости:**  
   ```bash
   pip install -r requirements.txt
   ```
---
## Запуск
```bash
python3 app.py
```
---
## Конфигурация (core/config.py):
1. Задайте токен бота в переменной окружения TOKEN
2. Укажите ID администратора (DEV) и владельца (OWNER)
3. Установите GROUP_ID (ID чата, где создаются топики-тикеты)
```python
TOKEN = os.environ.get("TOKEN")  # Токен бота
DEV = '1281134018'               # ID админа
OWNER = '5469853944'             # ID владельца
GROUP_ID = -1002446708871        # ID группы с топиками
```
---
## Функционал
1. Автоматическое создание топиков в указанном чате при обращении пользователя
2. Пересылка сообщений между пользователем и топиком
3. Сохранение истории сообщений
4. Система рейтинга для администраторов

### Note: Для работы с топиками убедитесь, что бот имеет права администратора в указанном чате.

