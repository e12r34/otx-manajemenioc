from datetime import datetime

def make_log(file,tulis):
    now=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    file.write(f"{now} {tulis}\n")