````markdown
# 🛡️ Mikrotik User Manager

Скрипт для автоматического **создания и удаления пользователей** на устройствах MikroTik через SSH.

✅ Идеально подходит для админов, управляющих десятками роутеров: автоматизация, логирование и гибкость.

---

## 📌 Основные возможности

- 🔐 Массовое создание и удаление пользователей на MikroTik
- 🎛️ Поддержка групп (`group`) и `Allowed Address`
- 📥 Загрузка IP-адресов из файла или ввод вручную
- 📝 Логирование всех действий в `logs/`
- 🔄 Умная проверка создания/удаления с ожиданием подтверждения

---

## ⚙️ Установка

Требуется Python 3.7+

Установите зависимости:

```bash
pip install netmiko colorama
````

или добавьте в `requirements.txt`:

```
netmiko==4.2.0
colorama==0.4.3
```

---

## 🚀 Быстрый старт

### 🔧 Создание пользователя

```bash
python3 mikrotik_user_manager.py --mode create
```

➡ Введите IP вручную или укажите файл.

Пример с файлом:

```bash
python3 mikrotik_user_manager.py --mode create --file ip_list.txt --group write --address 192.168.88.1,192.168.88.2
```

### 🗑️ Удаление пользователя

```bash
python3 mikrotik_user_manager.py --mode delete --file ip_list.txt
```

---

## 🛠️ Параметры

| Аргумент    | Описание                                                         |
| ----------- | ---------------------------------------------------------------- |
| `--mode`    | Режим работы: `create` или `delete` (обязательно)                |
| `--file`    | (необязательно) Путь к файлу со списком IP-адресов               |
| `--group`   | (только при `create`) Группа пользователя (по умолчанию: `full`) |
| `--address` | (только при `create`) Разрешённые IP-адреса через запятую        |

Если `--file` не указан, IP-адреса можно ввести вручную прямо в консоли.

---

## 🧾 Пример файла ip\_list.txt

```
192.168.88.1
192.168.88.2
10.0.0.1
```

---

## 📁 Логи

После выполнения создаётся лог-файл в директории `logs/`:

```bash
logs/create_admin.log
logs/delete_testuser.log
```

---

## 🔧 Зависимости

```txt
netmiko==4.2.0
colorama==0.4.3
```

---

## 👨‍💻 Автор

* GitHub: [github.com/netscripor](https://github.com/netscripor)
* Telegram: [t.me/netscripor](https://t.me/netscripor)
* Boosty: [boosty.to/netscripor](https://boosty.to/netscripor)

---
- подготовить `pyproject.toml`, если планируется публикация.

Готов продолжать?
```
