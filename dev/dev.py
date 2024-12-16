import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer

# Глобальные переменные для процессов
webview_process = None
angular_process = None

# Определяем базовый путь (директория, где находится скрипт dev.py)
base_path = os.path.dirname(os.path.abspath(__file__))
# Путь к папке frontend и pywebview
frontend_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'frontend'))
pywebview_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'pywebview/main.py'))
dist_path = os.path.join(frontend_path, 'dist')

print(frontend_path)
print(pywebview_path)
print(dist_path)

# Функция для запуска сборки Angular
def start_angular_build():
    # Запуск Angular в режиме watch из директории frontend
    return subprocess.Popen(['ng', 'build', '--watch'], cwd=frontend_path)

# Функция для запуска pywebview
def start_pywebview():
    # Запуск pywebview из главной директории проекта
    return subprocess.Popen(['python', pywebview_path])

# Перезапуск процесса pywebview
def restart_pywebview():
    global webview_process
    if webview_process:
        print("Перезапуск pywebview...")
        webview_process.terminate()
        webview_process.wait()  # Ждем завершения процесса
    webview_process = start_pywebview()

# Дебаунсер для отслеживания изменений
def debounce(func, delay):
    def wrapper(*args, **kwargs):
        if hasattr(wrapper, "timer"):
            wrapper.timer.cancel()
        wrapper.timer = Timer(delay, func, args, kwargs)
        wrapper.timer.start()
    return wrapper

# Обработчик событий для изменений файлов
class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.js') or event.src_path.endswith('.html'):  # Обрабатываем изменения в сборке Angular
            print("Обнаружено изменение в файлах фронтенда, перезапуск pywebview...")
            restart_pywebview()

# Главная функция
def main():
    global angular_process
    global webview_process

    # Запускаем процесс сборки Angular
    angular_process = start_angular_build()

    # Запускаем процесс pywebview
    webview_process = start_pywebview()

    # Настроим обработчик событий для отслеживания изменений в папке с собранными файлами Angular
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, dist_path, recursive=True)
    observer.start()

    try:
        # Ждем завершения процессов
        angular_process.wait()
        observer.join()
    except KeyboardInterrupt:
        print("Прерывание. Завершаем процессы...")
        angular_process.terminate()
        webview_process.terminate()
        observer.stop()

if __name__ == "__main__":
    main()
