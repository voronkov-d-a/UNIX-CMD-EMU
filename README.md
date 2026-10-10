# Эмулятор оболочки ОС

Эмулятор командной оболочки UNIX-подобной ОС. Вариант №6.

Практическая работа реализует консольный интерфейс, похожий на работу командной строки UNIX-подобной ОС. Поддерживаются виртуальная файловая система (VFS), стартовые скрипты, переменные окружения, основные и дополнительные команды.

## Общее описание

Приложение представляет собой CLI-эмулятор оболочки. Эмулятор работает в интерактивном режиме, формирует приглашение к вводу на основе реальных данных ОС, поддерживает раскрытие переменных окружения и выполняет команды над виртуальной файловой системой.

VFS хранится в памяти и загружается из JSON-файла. Все изменения, выполняемые командами `cp`, `mv`, `vfs-init` и другими, производятся только в памяти и не изменяют исходный JSON-файл, кроме случаев, явно предусмотренных служебными командами.

## Возможности

- Консольный интерфейс (CLI).
- Приглашение к вводу вида `username@hostname:path$`, формируемое на основе реальных данных ОС.
- Раскрытие переменных окружения реальной ОС, например `$HOME`, `$USER`, `$PATH`.
- Загрузка VFS из JSON-файла.
- Поддержка двоичных данных через `base64`.
- Выполнение стартового скрипта с комментариями.
- Отладочный вывод параметров при запуске.
- Команды для навигации, чтения, поиска и изменения VFS.
- Обработка ошибок: неверные пути, отсутствующие файлы, неверные аргументы, неизвестные команды.

## Требования

- Python 3.10+.
- Стандартная библиотека Python.
- Для запуска тестов: `pytest` или `unittest`.

## Запуск

Запуск в интерактивном режиме:

```bash
python3 src/main.py
```

Для Windows:

```bash
python src\main.py
```

Запуск с параметрами:

```bash
python3 src/main.py --vfs ./vfs/default.json --script ./scripts/start.sh
```

## Параметры командной строки

| Параметр | Описание |
|---|---|
| `-v`, `--vfs <path>` | Путь к JSON-файлу виртуальной файловой системы |
| `-s`, `--script <path>` | Путь к стартовому скрипту |
| `-d`, `--debug` | Включить отладочный вывод параметров запуска |

При запуске эмулятор выводит отладочную информацию: путь к VFS, путь к стартовому скрипту, имя пользователя, имя хоста и текущую рабочую директорию.

## Команды эмулятора

| Команда | Описание |
|---|---|
| `ls [-l] [-a] [-h] [path]` | Вывести содержимое каталога. `-l` — подробный формат; `-a` — показывать скрытые файлы; `-h` — человекочитаемый размер |
| `cd <path>` | Перейти в указанный каталог |
| `head [-n N] <file>` | Вывести первые `N` строк файла. По умолчанию `N = 10` |
| `tail [-n N] <file>` | Вывести последние `N` строк файла. По умолчанию `N = 10` |
| `find <path> [pattern]` | Найти файлы и каталоги по пути и/или шаблону |
| `cp <source> <destination>` | Скопировать файл или каталог внутри VFS |
| `mv <source> <destination>` | Переместить или переименовать файл/каталог внутри VFS |
| `vfs-init` | Сбросить текущую VFS к состоянию по умолчанию |
| `exit` | Завершить работу эмулятора |

## Виртуальная файловая система

VFS описывается JSON-файлом. Все операции выполняются в памяти. Для двоичных данных используется `base64` или аналогичное кодирование.

Пример минимального JSON-файла VFS:

```json
{
  "type": "dir",
  "name": "/",
  "children": {
    "home": {
      "type": "dir",
      "children": {
        "user": {
          "type": "dir",
          "children": {
            "hello.txt": {
              "type": "file",
              "content": "SGVsbG8sIHdvcmxkIQ==",
              "encoding": "base64"
            }
          }
        }
      }
    }
  }
}
```

## Стартовые скрипты

Стартовый скрипт содержит команды эмулятора. Комментарии оформляются синтаксисом языка реализации. Для Python используется `#`.

Пример стартового скрипта:

```bash
# Стартовый скрипт для проверки этапа 5

vfs-init
ls /
cd /home/user
head -n 3 hello.txt
tail -n 2 hello.txt
find /home -name "*.txt"
cp hello.txt copy.txt
mv copy.txt /tmp/
ls /tmp
exit
```

При выполнении стартового скрипта на экран выводится как ввод, так и вывод команд, чтобы имитировать диалог с пользователем.

## Сборка

Проект написан на Python и не требует отдельной сборки. Достаточно установленного интерпретатора Python 3.10+.

При необходимости можно создать виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Для Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

## Запуск тестов

Запуск тестов через `pytest`:

```bash
python3 -m pytest tests/test_main.py -v
```

Запуск через `unittest`:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

Если `pytest` не установлен:

```bash
pip install pytest
```

## Примеры использования

### Интерактивный режим

```bash
$ python3 src/main.py
user@host:~$ ls
home
tmp
user@host:~$ cd /home/user
user@host:/home/user$ head -n 2 hello.txt
Hello
world
user@host:/home/user$ tail -n 2 hello.txt
Hello
world
user@host:/home/user$ find /home -name "*.txt"
/home/user/hello.txt
user@host:/home/user$ cp hello.txt hello_copy.txt
user@host:/home/user$ mv hello_copy.txt /tmp/
user@host:/home/user$ ls /tmp
hello_copy.txt
user@host:/home/user$ vfs-init
VFS reset to default
user@host:/home/user$ exit
```

### Запуск со стартовым скриптом

```bash
python3 src/main.py --vfs ./vfs/default.json --script ./scripts/test_stage5.sh
```

### Обработка ошибок

```bash
user@host:~$ cd /no/such/dir
cd: /no/such/dir: No such file or directory

user@host:~$ head missing.txt
head: missing.txt: No such file or directory

user@host:~$ cp file.txt /no/such/dir/
cp: cannot create /no/such/dir/file.txt: No such file or directory

user@host:~$ unknowncmd
unknowncmd: command not found
```