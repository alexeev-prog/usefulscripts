#!/usr/bin/env python3

import os
import re
import subprocess
import statistics
import argparse
import json
from typing import List, Tuple


def is_root() -> bool:
    return os.getuid() == 0


def get_systemd_version() -> str:
    try:
        text = subprocess.check_output(
            ["systemctl", "--version"], encoding="utf8", stderr=subprocess.DEVNULL
        )
        version = text.split(" ")[1].strip()
        return version
    except Exception as ex:
        raise Exception(f"Не удалось получить версию systemd: {ex}")


def disable_service(service: str):
    if is_root():
        process = subprocess.run(
            ["systemctl", "disable", "--now", service],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
    else:
        process = subprocess.run(
            ["sudo", "systemctl", "disable", "--now", service],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )

    if process.returncode != 0:
        print(f"Ошибка: {process.stderr}")
    else:
        print(f"Служба '{service}' успешно отключена")


def enable_service(service: str):
    if is_root():
        process = subprocess.run(
            ["systemctl", "enable", "--now", service],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
    else:
        process = subprocess.run(
            ["sudo", "systemctl", "enable", "--now", service],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )

    if process.returncode != 0:
        print(f"Ошибка: {process.stderr}")
    else:
        print(f"Служба '{service}' успешно включена")


def restart_service(service: str):
    if is_root():
        process = subprocess.run(
            ["systemctl", "restart", service],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
    else:
        process = subprocess.run(
            ["sudo", "systemctl", "restart", service],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )

    if process.returncode != 0:
        print(f"Ошибка: {process.stderr}")
    else:
        print(f"Служба '{service}' успешно перезапущена")


def stop_service(service: str):
    if is_root():
        process = subprocess.run(
            ["systemctl", "stop", service],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
    else:
        process = subprocess.run(
            ["sudo", "systemctl", "stop", service],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )

    if process.returncode != 0:
        print(f"Ошибка: {process.stderr}")
    else:
        print(f"Служба '{service}' успешно остановлена")


def start_service(service: str):
    if is_root():
        process = subprocess.run(
            ["systemctl", "start", service],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
    else:
        process = subprocess.run(
            ["sudo", "systemctl", "start", service],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )

    if process.returncode != 0:
        print(f"Ошибка: {process.stderr}")
    else:
        print(f"Служба '{service}' успешно запущена")


def get_service_status(service: str):
    try:
        if is_root():
            process = subprocess.run(
                ["systemctl", "status", "--no-pager", service],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True,
            )
        else:
            process = subprocess.run(
                ["sudo", "systemctl", "status", "--no-pager", service],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True,
            )

        print(process.stdout)
        if process.stderr:
            print(f"Предупреждение: {process.stderr}")

    except Exception as ex:
        print(f"Ошибка при получении статуса службы: {ex}")


def list_failed_services():
    try:
        if is_root():
            text = subprocess.check_output(
                ["systemctl", "--failed", "--no-pager"],
                encoding="utf8",
                stderr=subprocess.DEVNULL,
            )
        else:
            text = subprocess.check_output(
                ["sudo", "systemctl", "--failed", "--no-pager"],
                encoding="utf8",
                stderr=subprocess.DEVNULL,
            )

        print("Неудачные службы:")
        print(text)

    except Exception as ex:
        print(f"Ошибка при получении списка неудачных служб: {ex}")


def list_active_services(unit_type: str = "service"):
    try:
        if is_root():
            text = subprocess.check_output(
                [
                    "systemctl",
                    "list-units",
                    "--type=" + unit_type,
                    "--state=active",
                    "--no-pager",
                ],
                encoding="utf8",
                stderr=subprocess.DEVNULL,
            )
        else:
            text = subprocess.check_output(
                [
                    "sudo",
                    "systemctl",
                    "list-units",
                    "--type=" + unit_type,
                    "--state=active",
                    "--no-pager",
                ],
                encoding="utf8",
                stderr=subprocess.DEVNULL,
            )

        print(f"Активные {unit_type}:")
        print(text)

    except Exception as ex:
        print(f"Ошибка при получении списка активных служб: {ex}")


def parse_service_times() -> Tuple[List[float], List[str], List[str]]:
    times, units, names = [], [], []

    try:
        text = subprocess.check_output(
            ["systemd-analyze", "blame"],
            encoding="utf8",
            stderr=subprocess.DEVNULL,
        )

        for line in text.strip().split("\n"):
            if line:
                match = re.match(r"\s*(\d+(?:\.\d+)?)(ms|s)\s+(\S+)", line)
                if match:
                    time_val = float(match.group(1))
                    unit = match.group(2)
                    name = match.group(3)

                    if unit == "s":
                        time_val *= 1000

                    times.append(time_val)
                    units.append("ms")
                    names.append(name)

    except Exception as ex:
        print(f"Ошибка при анализе времени служб: {ex}")

    return times, units, names


def analyze_startup_time() -> bool:
    try:
        subprocess.check_output(
            ["systemd-analyze"],
            encoding="utf8",
            stderr=subprocess.DEVNULL,
        )
    except Exception as ex:
        print(f"Ошибка при выполнении systemd-analyze: {ex}")
        return False

    times, units, names = parse_service_times()

    if not times:
        print("Не удалось получить данные о службах")
        return False

    print("Время запуска служб:")
    for time, unit, name in zip(times, units, names):
        startup_ftime = f"{time:.1f}{unit}"
        print(f"{startup_ftime:10} -- {name}")

    slowest_idx = times.index(max(times))
    fastest_idx = times.index(min(times))

    slowest_startup_ftime = f"{times[slowest_idx]:.1f}{units[slowest_idx]}"
    fastest_startup_ftime = f"{times[fastest_idx]:.1f}{units[fastest_idx]}"

    average = statistics.mean(times)
    median = statistics.median(times)
    total_speed = sum(times)

    print("\nСтатистика загрузки:")
    print(f"Самая медленная служба ({slowest_startup_ftime}): {names[slowest_idx]}")
    print(f"Самая быстрая служба ({fastest_startup_ftime}): {names[fastest_idx]}")
    print(f"Среднее арифметическое времени запуска служб: {average:.1f}ms")
    print(f"Медиана времени запуска служб: {median:.1f}ms")
    print(f"Общее время запуска всех служб: {total_speed:.1f}ms")

    slow_services = [(name, time) for time, name in zip(times, names) if time > 1000]
    if slow_services:
        print("\nСлужбы с временем запуска > 1000ms:")
        for name, time in sorted(slow_services, key=lambda x: x[1], reverse=True):
            print(f"  {time:.1f}ms - {name}")

    return True


def get_system_stats():
    try:
        if is_root():
            mem_output = subprocess.check_output(
                ["systemd-cgtop", "--raw", "--iterations=1", "--order=memory"],
                encoding="utf8",
                stderr=subprocess.DEVNULL,
                timeout=5,
            )
            cpu_output = subprocess.check_output(
                ["systemd-cgtop", "--raw", "--iterations=1", "--order=cpu"],
                encoding="utf8",
                stderr=subprocess.DEVNULL,
                timeout=5,
            )
        else:
            mem_output = subprocess.check_output(
                ["sudo", "systemd-cgtop", "--raw", "--iterations=1", "--order=memory"],
                encoding="utf8",
                stderr=subprocess.DEVNULL,
                timeout=5,
            )
            cpu_output = subprocess.check_output(
                ["sudo", "systemd-cgtop", "--raw", "--iterations=1", "--order=cpu"],
                encoding="utf8",
                stderr=subprocess.DEVNULL,
                timeout=5,
            )

        print("Топ по использованию памяти:")
        print(mem_output)
        print("\nТоп по использованию CPU:")
        print(cpu_output)

    except subprocess.TimeoutExpired:
        print("Таймаут при получении статистики")
    except Exception as ex:
        print(f"Ошибка при получении статистики: {ex}")


def analyze_critical_chain(service: str):
    try:
        if is_root():
            text = subprocess.check_output(
                ["systemd-analyze", "critical-chain", service],
                encoding="utf8",
                stderr=subprocess.DEVNULL,
            )
        else:
            text = subprocess.check_output(
                ["sudo", "systemd-analyze", "critical-chain", service],
                encoding="utf8",
                stderr=subprocess.DEVNULL,
            )

        print(f"Критическая цепочка для {service}:")
        print(text)

    except Exception as ex:
        print(f"Ошибка при анализе цепочки: {ex}")


def export_startup_report(filename: str = "systemd_startup_report.json"):
    try:
        times, units, names = parse_service_times()

        report = {"services": [], "statistics": {}}

        for time, name in zip(times, names):
            report["services"].append({"name": name, "startup_time_ms": time})

        if times:
            report["statistics"] = {
                "total_services": len(times),
                "average_startup_time_ms": statistics.mean(times),
                "median_startup_time_ms": statistics.median(times),
                "max_startup_time_ms": max(times),
                "min_startup_time_ms": min(times),
                "total_startup_time_ms": sum(times),
                "slowest_service": names[times.index(max(times))],
                "fastest_service": names[times.index(min(times))],
            }

        with open(filename, "w") as f:
            json.dump(report, f, indent=2)

        print(f"Отчет сохранен в {filename}")

    except Exception as ex:
        print(f"Ошибка при сохранении отчета: {ex}")


def main():
    parser = argparse.ArgumentParser(
        description="Утилита для управления службами systemd и анализа времени загрузки",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    subparsers.add_parser("version", help="Получить версию systemd")

    disable_parser = subparsers.add_parser("disable", help="Выключить службу")
    disable_parser.add_argument("-s", "--service", required=True, help="Имя службы")

    enable_parser = subparsers.add_parser("enable", help="Включить службу")
    enable_parser.add_argument("-s", "--service", required=True, help="Имя службы")

    restart_parser = subparsers.add_parser("restart", help="Перезапустить службу")
    restart_parser.add_argument("-s", "--service", required=True, help="Имя службы")

    stop_parser = subparsers.add_parser("stop", help="Остановить службу")
    stop_parser.add_argument("-s", "--service", required=True, help="Имя службы")

    start_parser = subparsers.add_parser("start", help="Запустить службу")
    start_parser.add_argument("-s", "--service", required=True, help="Имя службы")

    status_parser = subparsers.add_parser("status", help="Показать статус службы")
    status_parser.add_argument("-s", "--service", required=True, help="Имя службы")

    subparsers.add_parser("startuptime", help="Анализ времени запуска системы и служб")

    subparsers.add_parser("failed", help="Показать неудачные службы")

    active_parser = subparsers.add_parser("active", help="Показать активные службы")
    active_parser.add_argument(
        "-t", "--type", default="service", help="Тип юнитов (service, socket, timer)"
    )

    subparsers.add_parser("stats", help="Показать статистику системы")

    chain_parser = subparsers.add_parser(
        "chain", help="Анализ критической цепочки службы"
    )
    chain_parser.add_argument("-s", "--service", required=True, help="Имя службы")

    export_parser = subparsers.add_parser("export", help="Экспорт отчета в JSON")
    export_parser.add_argument(
        "-f",
        "--file",
        default="systemd_startup_report.json",
        help="Имя файла для экспорта",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "version":
            version = get_systemd_version()
            print(f"Версия systemd: {version}")

        elif args.command == "disable":
            disable_service(args.service)

        elif args.command == "enable":
            enable_service(args.service)

        elif args.command == "restart":
            restart_service(args.service)

        elif args.command == "stop":
            stop_service(args.service)

        elif args.command == "start":
            start_service(args.service)

        elif args.command == "status":
            get_service_status(args.service)

        elif args.command == "startuptime":
            analyze_startup_time()

        elif args.command == "failed":
            list_failed_services()

        elif args.command == "active":
            list_active_services(args.type)

        elif args.command == "stats":
            get_system_stats()

        elif args.command == "chain":
            analyze_critical_chain(args.service)

        elif args.command == "export":
            export_startup_report(args.file)

    except KeyboardInterrupt:
        print("\nОперация прервана пользователем")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
