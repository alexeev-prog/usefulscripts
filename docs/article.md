# Скрипты и алиасы для вашего линукса
Каждый, кто проводит в терминале больше пяти минут, сталкивается с одним и тем же: одни и те же длинные команды приходится набирать снова и снова, а рутинные действия отнимают время и внимание. Сначала терпишь, потом — начинаешь оптимизировать.

Простейший алиас в .bashrc или .zshrc кажется небольшим открытием. Первый рабочий скрипт, сохраненный в .local/bin, ощущается как прорыв. Это не просто про лень — это про эффективность, про оптимизацию работы.

Со временем такая «мелкая оптимизация» собирается в целый личный фреймворк или набор утилит для командной строки. Это уже не пара заплаток, а твоя собственная среда, отточенная под конкретные задачи. В этой статье я хочу показать свою коллекцию таких скриптов и алиасов — не как идеальный стандарт, а 3как пример живого подхода. Возможно, какие-то решения окажутся полезными и вам, а главное — побудят создать что-то своё, еще более удобное.

---

Довольно часто в сообществе линукса можно увидеть дискуссию на тему того, когда полезны алиасы, а когда исполняемые скрипты в условном `~/.local/bin/`. Алиасы компактные и быстрые, благодаря этому ими можно заменить небольшие цепочки команд. Но у них есть минусы, например если задавать в конфиге шелла, то приходится перезагружать сессию. Поэтому иногда удобнее использовать скрипты, так как они могут быть не только на bash, но и на других доступных в системах языках программирования. Ну и понятно дело скрипты уже имеют намного большой простор для деятельности.

В этой статье я покажу и алиасы, и скрипты, которые я сам использую на ежедневной основе.

Все скрипты доступны в [моем репозитории](https://github.com/alexeev-prog/usefulscripts). Вы можете поделиться своими скриптами в комментариях или через пулл реквест.

## NixOS
Начну с набора алиасов для NixOS:

```bash
alias rb="sudo nixos-rebuild switch --flake /home/alexeev/nixos/"
alias upd="nix flake update /home/alexeev/nixos/"
alias upg="sudo nixos-rebuild switch --upgrade --flake /home/alexeev/nixos/"
alias nixclean="sudo nix-collect-garbage -d"
alias hms="home-manager switch --flake /home/alexeev/nixos/"

alias conf="nvim ~/nixos/nixos/configuration.nix"
alias pkgs="nvim ~/nixos/nixos/packages.nix"
```

Позволяет делать ребилд, обновление, очистку системы, а также быстро работать с конфигурацией и пакетами в системе.

## Git
Алиасы для git можно делать как и стандартным внешним путем:

```bash
alias gga="git add"
alias ggc="git commit"
alias ggcm="git commit -m"
alias ggs="git status"
alias ggl="git log"
alias gglo="git log --oneline"
alias ggd="git diff"
alias ggds="git diff --staged"
alias ggr="git restore"
```

Так и через конфигурирование файла `~/.gitconfig`:

```bash
[alias]
    st = status -b
    c = commit
    co = checkout
    br = branch
    slog = log --pretty=format:"%C(auto)%h%C(auto)%d\\ %C(auto,reset)%s\\ \\ [%C(auto,blue)%an%C(auto,reset),\\ %C(auto,cyan)%ar%C(auto,reset)]"
    glog = log --graph --pretty=format:"%C(auto,yellow)%h%C(auto)%d\\ %C(auto,reset)%s\\ \\ [%C(auto,blue)%an%C(auto,reset),\\ %C(auto,cyan)%ar%C(auto,reset)]"
    wlog = log --pretty=format:"%C(auto,yellow)%h%C(auto)%d%C(auto,reset)\\ by\\ %C(auto,blue)%an%C(auto,reset),\\ %C(auto,cyan)%ar%C(auto,reset)%n\\ %s%n" --stat
    gr = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)' --all
    wt = worktree
```

Я достаточно часто пользую эти алиасы для быстрой работы с репозиториями, получать логи и графы веток и коммитов.

Также я использую иногда вот такой интересный скрипт:

```python
#!/usr/bin/env python3
import os
import re


class GitVersion:
    def __init__(self):
        self._default_version = "0.1.0"
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

    @property
    def tag(self):
        stream = os.popen("git describe --match v[0-9]* --abbrev=0 --tags")
        return stream.read().strip()

    @property
    def version(self):
        version = f"{self.tag[1:]}.{self.build}"

        if version == ".":
            return self._default_version

        return version

    @property
    def default_branch(self):
        stream = os.popen("git config --get init.defaultBranch")
        result = stream.read().strip()

        if not result:
            result = "main"

        return result

    @property
    def build(self):
        stream = os.popen(f"git rev-list {self.tag}.. --count")
        return stream.read().strip()

    @property
    def branch(self):
        stream = os.popen("git branch --show-current")
        return stream.read().strip()

    @property
    def full(self):
        return f"{self.version}-{self.branch}"

    @property
    def standard(self):
        standard = f"{self.version}-{self.branch}"
        if self.branch == self.default_branch or re.match("release/.*", self.branch):
            standard = f"{self.version}"
        return standard

    @property
    def commit(self):
        stream = os.popen("git rev-parse HEAD")
        return stream.read().strip()

    @property
    def commit_hash(self):
        stream = os.popen("git rev-parse --short HEAD")
        return stream.read().strip()

    def __str__(self):
        return f"""
Tag: {self.tag}
Version: {self.version}
Full: {self.full}
Branch: {self.branch}
Build: {self.build}
Standard: {self.standard}
Commit: {self.commit}

GitRepo {self.full} {self.commit_hash}
"""


if __name__ == "__main__":
    git_version = GitVersion()
    print(git_version)
```

Этот скрипт позволяет получать информацию о репозитории, включая релизные теги в определенном формате (`git describe --match v[0-9]* --abbrev=0 --tags`). Я сам достаточно часто использую этот скрипт, если надо координировать работу с git-репозиторием. Он использует последний тег (vX.X.X) как базовую версию и добавляет количество коммитов после тега как номер сборки. Для main/release веток версия отображается без имени ветки, для остальных - с именем ветки. Если тегов нет, используется версия 0.1.0. Скрипт полезен для CI/CD пайплайнов, чтобы автоматически генерировать версии сборок.

## Полезные алиасы
Я использую достаточно часто алиасы для своего шелла. Например, я через `alias ls='exa --icons'` заменил `ls` на утилиту `exa`.

```bash
alias ll="ls -l"
alias se="sudoedit"
alias bat="bat --theme base16"
alias ff=fastfetch
alias nv=nvim
alias v=vim
alias nixfish="echo Enter to nix-shell && nix-shell . --command fish"

alias ..='cd ..'
alias 2..='cd ../..'
alias 3..='cd ../../..'
alias 4..='cd ../../../..'
alias 5..='cd ../../../../..'
```

Я использую команду nixfish когда мне нужно войти в nix-shell окружение через командную оболочку fish (так как я использую ее на регулярной основе). Остальные - это удобные сокращения команд, от вызовов программ до упрощения команды (как видно в последнем блоке, где идет переход в предыдущие директории).

Также я использую следующие:

```bash
alias syslog_emerg="sudo dmesg --level=emerg,alert,crit"
alias syslog="sudo dmesg --level=err,warn"
alias xlog='grep "(EE)\|(WW)\|error\|failed" ~/.local/share/xorg/Xorg.0.log'
alias vacuum="sudo journalctl --vacuum-size=100M"
alias vacuum_time="sudo journalctl --vacuum-time=2weeks"
alias rm="rmtrash "
alias youtube='yt-dlp -f "bestvideo[height<=1080]+bestaudio" --merge-output-format mp4 --output "%(title)s.%(ext)s"'
```

Первые 5 как видно, помогают взаимодействовать с сообщениями ядра и журналом, а также очищать их. Команду rm я заменяю на утилиту rmtrash, которая перемещает удаленный файл в корзину. Это не раз меня спасало от потери файлов. А команда youtube помогает скачивать видео через yt-dlp в нужном мне формате.

## Баш-скрипты для любых юзкейсов
Баш-скрипты позволяют реализовать более сложную или кастомизируемую логику.

Например, скрипт [tempe.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/tempe.sh) создает временную директорию и переходит в нее.

А скрипты [check-cpu.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/check-cpu.sh) и [check-gpu.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/check-gpu.sh) позволяют получить вендора процессора и видеокарты соответственно. Я использую эти скрипты если, например, нужно установить драйвера под конкретный вендор.

А вот например скрипт `clean_broken_links.sh`:

```bash
#!/usr/bin/env bash

# Target directory for scan
TARGET_DIR="$HOME"

# Search and delete broken symlinks
find "$TARGET_DIR" -xtype l -print -delete

echo "✅ All broken symlinks deleted from $TARGET_DIR"
```

Он очищает рекурсивно директорию от сломанных симлинков, что позволяет содержать систему в чистоте и не засорять ее.

Продолжая тему очистки и сортировки, можно упомянуть скрипт [clean_downloads_dir.py](https://github.com/alexeev-prog/usefulscripts/blob/main/python_scripts/clean_downloads_dir.py). Он написан на python и позволяет сортировать директорию (по умолчанию - `~/Downloads`), причем можно кастомизировать файлы с каким расширением в какую директорию сортировать, через файл extensions.json в текущей директории. Если его нет - он создается сам и заполняется значениями по умолчанию. Я лично пользуюсь им часто, и не только для директории Downloads.

В то время, когда я еще сидел на Arch Linux, я написал небольшой скрипт для очистки арча (требуется пакет pacman-contrib для paccache):

```bash
#!/usr/bin/env bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;37m'
END='\033[0m'

printf "${GREEN}Cleaning...${END}\n"

printf "${RED}[+] Full system update${END}\n"
sudo pacman -Syu

printf "${BLUE}[+] Clean pacman cache${END}\n"
sudo pacman -Scc
sudo paccache -r
sudo paccache -rk1
sudo paccache -ruk0

printf "${CYAN}[+] Clean orphans${END}\n"
sudo pacman -Rns $(pacman -Qtdq)

printf "${PURPLE}[+] Clean font cache${END}\n"
fc-cache -frv

printf "${YELLOW}[+] Clean cache and tmp${END}\n"
sudo truncate -s 0 /var/log/pacman.log
sudo truncate -s 0 /var/log/pacman.log
rm -rf ~/.cache/
sudo rm -rf /tmp/*

printf "${GREEN}End!${END}\n"
```

Кроме того, часто бывает полезно очищать старые временные файлы (`delete_old_temp_files.sh`):

```bash
#!/usr/bin/env bash

TARGET_DIR="/tmp"
MAX_AGE=7

find "$TARGET_DIR" -type f -mtime +$MAX_AGE -exec rm -v {} \;
echo "✅ Delete temporary files that are more $MAX_AGE days from $TARGET_DIR"
```

Если мне нужно получить какой нибудь эмодзи, я использую скрипт [emoji.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/emoji.sh), который позволяет получать по названию эмодзи (`emoji.sh smile`).

Также из [этой статьи](https://habr.com/ru/companies/ruvds/articles/961514/) я позаимствовал себе в систему следующие скрипты:

 + [_mkcd foo_](https://codeberg.org/EvanHahn/dotfiles/src/commit/843b9ee13d949d346a4a73ccee2a99351aed285b/home/zsh/.config/zsh/aliases.zsh#L38-L41) создаёт каталог и переходит в него через `cd`. По сути, это команда `mkdir foo && cd foo`. Я этим скриптом пользуюсь постоянно — почти при каждом создании каталога.
 + [_mksh_](https://codeberg.org/EvanHahn/dotfiles/src/commit/843b9ee13d949d346a4a73ccee2a99351aed285b/home/bin/bin/mksh) позволяет быстро создавать скрипты оболочки. К примеру, `mksh foo.sh` создаёт `foo.sh`, делает его исполняемым с помощью `chmod u+x`, добавляет префиксы Bash и открывает скрипт в редакторе (в моём случае Vim). Пригождается раз в несколько дней. Многие из перечисленных в этой статье скриптов были созданы с помощью mksh.
 + [_url "$my_url"_](https://codeberg.org/EvanHahn/dotfiles/src/commit/843b9ee13d949d346a4a73ccee2a99351aed285b/home/bin/bin/url) парсит URL-адрес на составляющие части. Использую примерно раз в месяц для получения информации об URL, зачастую просто потому, что не хочу кликать по ссылке с трекером.

## Работа с сетью
Для работы с сетью у меня есть целый набор скриптов:

 + [check_wifi_connection.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/check_wifi_connection.sh) - отслеживание изменений подключенной Wi-Fi сети. Скрипт определяет текущую Wi-Fi сеть и уведомляет о её смене. Автоматически сохраняет последнюю SSID в файл `~/.last_ssid` и записывает изменения в лог `~/.wifi_changes.log`. Используйте для мониторинга роуминга между точками доступа.
 + [check_wifi_status.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/check_wifi_status.sh) - проверка доступности интернета через ping. Проверяет соединение с Google DNS (8.8.8.8) и уведомляет о потере/восстановлении подключения. Все события логируются в `~/.network_status.log`. Запускайте периодически через cron для постоянного мониторинга.
 + [detect_network_changes.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/detect_network_changes.sh) - обнаружение изменений внешнего IP-адреса. Мониторит публичный IP через ifconfig.me каждую минуту, фиксирует изменения и отправляет уведомления. Полезен для отслеживания переподключений, смены провайдера или динамических IP. Логирует в `~/.network_changes.log`.
 + [detect_new_devices_in_net.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/detect_new_devices_in_net.sh) - сканирование локальной сети на наличие новых устройств. Использует arp-scan для обнаружения MAC-адресов, сравнивает с сохранённым списком `~/.known_devices.txt` и уведомляет о новых девайсах. Требует установки `arp-scan`. Запускайте периодически для безопасности домашней сети.
 + [httpstatus.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/httpstatus.sh) - справочник HTTP-статус кодов. Выводит полный список кодов от 100 до 511 с описаниями. Поддерживает поиск по ключевым словам при передаче аргументов. Используйте как `./httpstatus.sh 404` для быстрого поиска или `./httpstatus.sh` для полного списка.
 + [list_of_wifi_nets.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/list_of_wifi_nets.sh) - мониторинг доступных Wi-Fi сетей в реальном времени. Показывает SSID, уровень сигнала и индикаторы качества, сортирует по силе сигнала. Обновляет список каждые 5 секунд. Использует nmcli. Запускайте при поиске лучшей точки доступа.
 + [monitoring_net_activity.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/monitoring_net_activity.sh) - мониторинг сетевого трафика в реальном времени. Измеряет скорость входящего (RX) и исходящего (TX) трафика на указанном интерфейсе (по умолчанию wlo1), обновляя данные каждую секунду. Показывает скорость в KB/s. Используйте для анализа загрузки сети.
 + [network_analysis.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/network_analysis.sh) - комплексный анализ сетевого состояния системы. Собирает статистику интерфейсов, подсчитывает соединения по состояниям, определяет топ-10 процессов по сетевой активности, показывает нестандартные открытые порты и статистику ошибок. Запускайте для диагностики сетевых проблем.

## Работа с systemd
Когда-то давно я писал [статью про работу с systemd](https://habr.com/ru/companies/timeweb/articles/824146/) где в конце прилогал скрипт-обертку для самого systemd. Я его немного улучшил и модифицировал - [systemdwrapper.py](https://github.com/alexeev-prog/usefulscripts/blob/main/python_scripts).

```
usage: systemdwrapper.py [-h] {version,disable,enable,restart,stop,start,status,startuptime,failed,active,stats,chain,export} ...

Утилита для управления службами systemd и анализа времени загрузки

positional arguments:
  {version,disable,enable,restart,stop,start,status,startuptime,failed,active,stats,chain,export}
                        Доступные команды
    version             Получить версию systemd
    disable             Выключить службу
    enable              Включить службу
    restart             Перезапустить службу
    stop                Остановить службу
    start               Запустить службу
    status              Показать статус службы
    startuptime         Анализ времени запуска системы и служб
    failed              Показать неудачные службы
    active              Показать активные службы
    stats               Показать статистику системы
    chain               Анализ критической цепочки службы
    export              Экспорт отчета в JSON

options:
  -h, --help            show this help message and exit
```

Например, при запуске с командой startuptime скрипт парсит вывод команд и выводит такой результат:

```
Статистика загрузки:
Самая медленная служба (3780.0ms): NetworkManager-wait-online.service
Самая быстрая служба (7.0ms): sys-kernel-config.mount
Среднее арифметическое времени запуска служб: 159.9ms
Медиана времени запуска служб: 44.0ms
Общее время запуска всех служб: 11193.0ms

Службы с временем запуска > 1000ms:
  3780.0ms - NetworkManager-wait-online.service
```

Кроме того, у меня есть еще вспомогательный баш-скрипт `slowest_services_to_launch.sh`, который записывает топ 10 самых медленных сервисов в лог-файл:

```bash
#!/usr/bin/env bash

LOG_FILE="/var/log/boot_time.log"

echo "🕰  Analyze system startup time" | tee -a $LOG_FILE

BOOT_TIME=$(systemd-analyze)

BLAME=$(systemd-analyze blame | head -n 10)

{
    echo "⏱️ $(date)"
    echo "$BOOT_TIME"
    echo "📌 Ten most slowest services:"
    echo "$BLAME"
    echo "-----------------------------"
} >> $LOG_FILE

echo "✅ Данные сохранены." | tee -a $LOG_FILE
```

Продолжая тему работы с сервисами, иногда может пригодиться скрипт ниже. Он позволяет перезапускать определенные сервисы systemd, если они не работают:

```bash
#!/usr/bin/env bash

SERVICES=("nginx" "postgresql")
LOG_FILE="/var/log/systemd_healthcheck.log"

echo "🔍 Check services status... $(date)" | tee -a $LOG_FILE

for svc in "${SERVICES[@]}"; do
    systemctl is-active --quiet "$svc"
    STATUS=$?

    if [ $STATUS -ne 0 ]; then
        echo "❌ Service $svc does not worked. Restart him..." | tee -a $LOG_FILE
        systemctl restart "$svc"
        sleep 1
        systemctl is-active --quiet "$svc" && echo "✅ $svc started now." | tee -a $LOG_FILE
    else
        echo "✔️ $svc is worked." | tee -a $LOG_FILE
    fi
done
```

## Авто-монтирование дисков
В минимальных системах, или без наличия полноценного DE, монтирование иногда приходится осуществлять вручную. Специально для этого я написал скрипт `auto_mount_devices.sh`:

```bash
#!/usr/bin/env bash

MOUNT_DIR="$HOME/MOUNTED_DEVICE"

mkdir -p "$MOUNT_DIR"

DEVICE=$(lsblk -o NAME,TYPE,HOTPLUG | awk '$2 == "disk" && $3 == 1 {print $1}' | tail -n1)

if [ -n "$DEVICE" ]; then
    PARTITION="/dev/${DEVICE}1"

    mkdir -p "$MOUNT_DIR/$PARTITION"
    sudo mount "$PARTITION" "$MOUNT_DIR/$PARTITION"

    echo "✅ Device $PARTITION mounted to $MOUNT_DIR/$PARTITION"
else
    echo "❌ USB-device not found"
fi
```

## Проверяем остаток свободного места
Этот скрипт крайне простой, его задача в том чтобы парсить остаток свободного места и если его меньше 90%, то сообщать об этом. Этот скрипт можно оформить в виде фонового демона или интегрировать в ваш WM, к примеру.

```bash
#!/usr/bin/env bash

THRESHOLD=90
LOG_FILE="$HOME/.disk_usage.log"

DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ "$DISK_USAGE" -ge "$THRESHOLD" ]; then
    MESSAGE="⚠️ Disk space is used by $DISK_USAGE%!"
    echo "$MESSAGE" | tee -a "$LOG_FILE"
    notify-send "Disk Alert" "$MESSAGE"
fi
```

## Проверка использования процессора
Абсолютно аналогичный скрипт предыдущему, только вместо места на диске - нагрузка на процессор.

```bash
#!/usr/bin/env bash

THRESHOLD=80
LOG_FILE="$HOME/.cpu_usage.log"

CPU_LOAD=$(awk '{print $1}' < /proc/loadavg | awk '{print $1*100}')

if (( ${CPU_LOAD%.*} >= THRESHOLD )); then
    MESSAGE="⚠️ High CPU Usage: $CPU_LOAD%"
    echo "$MESSAGE" | tee -a "$LOG_FILE"
    notify-send "CPU Alert" "$MESSAGE"
fi
```

## Детектинг изменения подключенных USB-девайсов
Данный скрипт в первый запуск сохраняет текущие usb-девайсы в лог-файл, затем перепроверя и сравнивая текущие подключения с подключениями из файла. Такой скрипт можно также оформить в демон.

```bash
#!/usr/bin/env bash

LOG_FILE="/var/log/usb_changes.log"
STATE_FILE="/var/log/usb_changes/usb_state.txt"

mkdir -p /var/log/usb_changes

echo "🔍 Searching installed USB... $(date)" | tee -a "$LOG_FILE"

lsusb > /var/log/current_usb.txt

if [ ! -f "$STATE_FILE" ]; then
    cp /var/log/current_usb.txt "$STATE_FILE"
    echo "📦 First save for USB" | tee -a "$LOG_FILE"
    exit 0
fi

if ! diff "$STATE_FILE" /var/log/current_usb.txt >/dev/null; then
    echo "⚠️  USB Connections changed" | tee -a "$LOG_FILE"
    echo "--- After:" | tee -a "$LOG_FILE"
    cat "$STATE_FILE" | tee -a "$LOG_FILE"
    echo "--- Before:" | tee -a "$LOG_FILE"
    cat /var/log/current_usb.txt | tee -a "$LOG_FILE"
    cp /var/log/current_usb.txt "$STATE_FILE"
else
    echo "✅ USB Connections not changed" | tee -a "$LOG_FILE"
fi

rm /var/log/current_usb.txt
```

## Анализ использования памяти
Этот скрипт я задействую для краткой сводки по памяти, здесь собирается вывод команды free-h, информация из /proc/meminfo, сортировка проессов по использованию RSS-памяти, процессы с большим использованием грязных страниц и memory pressure.

 > Resident set size (RSS) — термин, который в контексте управления памятью в операционной системе означает размер страниц памяти, выделенных процессу и в настоящее время находящихся в ОЗУ (RAM).

 > Memory pressure — это термин, используемый для описания состояния компьютерной системы, когда её доступные ресурсы памяти используются в большом объёме

```bash
#!/usr/bin/env bash

echo "=== Memory Analysis and OOM Killer Candidate Processes ==="
echo "Timestamp: $(date)"
echo ""

echo "1. Memory Summary:"
echo "-------------------"
free -h
echo ""

echo "2. Detailed RAM and Swap Usage:"
echo "----------------------------------------"
cat /proc/meminfo | grep -E "(MemTotal|MemAvailable|SwapTotal|SwapFree|SwapCached)"
echo ""

echo "3. Top 10 Processes by Resident Memory (RSS) Usage:"
echo "-------------------------------------------------------------"
ps aux --sort=-%mem | awk 'NR<=11 {printf "%-8s %-6s %-4s %-8s %-8s %s\n", $2, $1, $4, $3, $6/1024" MB", $11}'
echo ""

echo "4. Processes with Large Amounts of Dirty Memory:"
echo "------------------------------------------------------------------"
for pid in $(ps -eo pid --no-headers); do
  if [ -f /proc/$pid/statm ]; then
    dirty_pages=$(grep -i "Private_Dirty:" /proc/$pid/smaps 2>/dev/null | awk '{sum += $2} END {print sum}')
    if [ -n "$dirty_pages" ] && [ "$dirty_pages" -gt 1000 ]; then
      proc_name=$(cat /proc/$pid/comm 2>/dev/null)
      dirty_kb=$((dirty_pages * 4))
      echo "PID: $pid, Name: $proc_name, Dirty Memory: $dirty_kb KB"
    fi
  fi
done | sort -k6 -nr | head -10
echo ""

echo "5. Memory Pressure (PSI):"
echo "---------------------------"
if [ -f /proc/pressure/memory ]; then
  cat /proc/pressure/memory
else
  echo "Memory pressure information is not supported in this kernel version."
fi
echo ""
```

Если вы хотите узнать больше о работе памяти в линуксе, я [писал об этом статью, где подробно разобрал все](https://habr.com/ru/companies/timeweb/articles/804865/).

## Вывод температуры CPU и NVIDIA GPU
Данный скрипт через sensors и nvidia-smi выводит информацию о температуре вашего процессора и видеокарты (nvidia):

```bash
#!/usr/bin/env bash

echo -e "\033[1;36m=== Temperatures ===\033[0m"

# CPU
cpu_temp=$(sensors | grep -E "Core [0-9]:" | awk '{print $3}' | sed 's/+//;s/°C//' | sort -nr | head -n1)
echo -e "🔥 \033[1;32mCPU: \033[1;33m${cpu_temp}°C\033[0m"

# GPU (NVIDIA)
if command -v nvidia-smi &> /dev/null; then
    gpu_temp=$(nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader 2>/dev/null)
    if [ -n "$gpu_temp" ]; then
        echo -e "🎮 \033[1;32mGPU: \033[1;33m${gpu_temp}°C\033[0m"
    fi
fi
```

## Авто-форматирование C/C++ кода
Этот скрипт на python я использую в своих C/C++ проектах, который является оберткой для clang-format. Для меня он удобен тем, что автоматизирует рекурсивное форматирование и стили, и можно добавлять прочие форматтеры, и запускать их всех вместе через этот скрипт.

```python
import argparse
import os
import subprocess

count = 0


def find_source_files(root_dir, ignore_dirs):
    source_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

        for filename in filenames:
            if filename.endswith((".c", ".cpp", ".h", ".hpp", ".cc", ".cxx", ".hh")):
                source_files.append(os.path.join(dirpath, filename))
    return source_files


def format_files(files, clang_format, style):
    global count

    for file in files:
        try:
            cmd = [clang_format, "-i", "--style", style, file]
            subprocess.run(cmd, check=True)
            print(f"\033[32mFormatted:\033[0m {file}")
            count += 1
        except subprocess.CalledProcessError as e:
            print(f"\033[31mError formatting {file}:\033[0m {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Recursively format C/C++ files with clang-format"
    )
    parser.add_argument("root_dir", help="Root directory to search for source files")
    parser.add_argument("--ignore", nargs="+", default=[], help="Directories to ignore")
    parser.add_argument(
        "--clang-format", default="clang-format", help="Path to clang-format executable"
    )
    parser.add_argument(
        "--style", default="file", help="Formatting style (file/Google/LLVM/etc.)"
    )

    args = parser.parse_args()

    print("\033[36m=== C/C++ Source Formatter ===\033[0m")
    print(f"\033[33mRoot directory:\033[0m {args.root_dir}")
    print(f"\033[33mIgnored directories:\033[0m {args.ignore or 'None'}")
    print(f"\033[33mStyle:\033[0m {args.style}")
    print("\033[36m" + "=" * 30 + "\033[0m")

    source_files = find_source_files(args.root_dir, args.ignore)

    if not source_files:
        print("\033[33mNo C/C++ files found to format.\033[0m")
        return

    print(f"\033[33mFound {len(source_files)} files to format:\033[0m")
    format_files(source_files, args.clang_format, args.style)
    print(f"\033[32mFormatting complete ({count} files)!\033[0m")


if __name__ == "__main__":
    main()
```

## Проверка SSL-сертификата
Данный скрипт позволяет проверить сколько дней осталось до даты истечения ssl-сертификата.

```python
#!/usr/bin/env python3
import socket
import sys
import ssl
from datetime import datetime, timezone


def check_ssl_expiry(domain, days_before=7):
    context = ssl.create_default_context()

    with socket.create_connection((domain, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()

    expiry_date = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
    remaining_days = (expiry_date - datetime.now(timezone.utc).replace(tzinfo=None)).days

    print(f'Domain: {domain}')
    print(f"Remaining days: {remaining_days}")
    print(f'Days before: {days_before}')


check_ssl_expiry(sys.argv[1])
```

## Универсальный разархиватор
Этот скрипт полезный, если вам нужно единой командой извлечь содержимое архива, автоматически подобрать команду под расширение.

```bash
#!/usr/bin/env bash
# extract.sh [archive file] [optional: output directory]

main() {
    if [ $# -lt 1 ] || [ $# -gt 2 ]; then
        echo "Usage: extract.sh [archive file] [optional: output directory]"
        exit 1
    fi

    file="$1"
    output_dir="${2:-.}"

    if ! [ -f "$file" ]; then
        echo "File $file does not exist."
        exit 1
    fi

    if ! [ -d "$output_dir" ]; then
        mkdir -p "$output_dir" || { echo "Failed to create output directory $output_dir"; exit 1; }
        echo "Created output directory $output_dir"
    fi

    extract_file "$file" "$output_dir"
}

extract_file() {
    local file=$1
    local output_dir=$2

    case "$file" in
        *.tar.xz)  command_exists "tar" && tar -xvf "$file" -C "$output_dir" ;;
        *.tar.gz)  command_exists "tar" && tar -xzf "$file" -C "$output_dir" ;;
        *.tar.bz2) command_exists "tar" && tar -xjf "$file" -C "$output_dir" ;;
        *.tar)     command_exists "tar" && tar -xf "$file" -C "$output_dir" ;;
        *.tgz)     command_exists "tar" && tar -xzf "$file" -C "$output_dir" ;;
        *.bz|*.bz2) command_exists "bzip2" && bzip2 -d -k "$file" ;;
        *.gz)      command_exists "gunzip" && gunzip "$file" -c > "$output_dir" ;;
        *.zip|*.jar) command_exists "unzip" && unzip "$file" -d "$output_dir" ;;
        *.Z)      command_exists "zcat" && zcat "$file" | tar -xvf - -C "$output_dir" ;;
        *.rar)    command_exists "rar" && rar x "$file" "$output_dir" ;;
        *.7z)     command_exists "7z" && 7z x "$file" -o"$output_dir" ;;
        *) echo "Unsupported archive format." ;;
    esac
}

command_exists() {
    command -v "$1" >/dev/null 2>&1 || { echo >&2 "I require $1 but it's not installed. Aborting."; exit 1; }
}

main "$@"
```

---

В дополнении к этому, я нашел интересный комментарий из [этой статьи](https://habr.com/ru/companies/ruvds/articles/961514/).

![](https://habrastorage.org/webt/t5/sy/ej/t5syejkizxexy5lwuf2ukkq0_qc.png)

## Заключение
3Спасибо за прочтение статьи! Я надеюсь, вы узнали что‑то новенькое, или, может, какой‑нибудь трюк натолкнул вас на другой интересный алгоритм. Если нашли нюанс в самой статье — пишите в комментарии.

Если вам понравился изложенный материал, могу предложить вам подписаться на [мой блог в телеграме](https://t.me/hex_warehouse). Если, конечно, вам статья понравилась и вы хотите видеть чуть больше.

А сами скрипты вы можете увидеть в [моем репозитории](https://github.com/alexeev-prog/usefulscripts). Там вы можете еще больше скриптов на разных языках программирования, а также через PR поделиться своими наработками.

### Источники

 + ["Мои личные скрипты для повседневной работы"](https://habr.com/ru/companies/ruvds/articles/961514/)
