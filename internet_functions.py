import subprocess
import speedtest


def ping():
    ping_str = subprocess.run(["ping", "-n", "1", "yandex.ru"],
                              stdout=subprocess.PIPE, encoding="CP866")
    return parse_ping(ping_str.stdout)


def upload_speed():
    st = speedtest.Speedtest(secure=True)
    return make_readable_size(st.upload())


def download_speed():
    st = speedtest.Speedtest(secure=True)
    return make_readable_size(st.download())


def make_readable_size(n_bytes):  # Прводит число к читаемому формату и добавляет единицы измерения
    sizes = ["B", "KB", "MB", "GB", "TB"]
    ind = 0

    while n_bytes > 1024 and ind <= 4:
        n_bytes /= 1024
        ind += 1
    n_bytes = round(n_bytes, 2)
    return f"{n_bytes} {sizes[ind]}"


def parse_ping(ping_str):  # Вытаскивает часть с пингом из вывода команды
    ping_str = ping_str.split("=")[2]
    result = ""

    for s in ping_str:
        if s == "м" or s == "m":
            break
        else:
            result += s
    return result + "мс"
