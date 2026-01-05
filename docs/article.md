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

Этот скрипт позволяет получать информацию о репозитории, включая релизные теги в определенном формате (`git describe --match v[0-9]* --abbrev=0 --tags`). Я сам достаточно часто использую этот скрипт, если надо координировать работу с git-репозиторием.

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

### Работа с сетью
Для работы с сетью у меня есть целый набор скриптов:

 + [check_wifi_connection.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/check_wifi_connection.sh) - отслеживание изменений подключенной Wi-Fi сети. Скрипт определяет текущую Wi-Fi сеть и уведомляет о её смене. Автоматически сохраняет последнюю SSID в файл `~/.last_ssid` и записывает изменения в лог `~/.wifi_changes.log`. Используйте для мониторинга роуминга между точками доступа.
 + [check_wifi_status.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/check_wifi_status.sh) - проверка доступности интернета через ping. Проверяет соединение с Google DNS (8.8.8.8) и уведомляет о потере/восстановлении подключения. Все события логируются в `~/.network_status.log`. Запускайте периодически через cron для постоянного мониторинга.
 + [detect_network_changes.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/detect_network_changes.sh) - обнаружение изменений внешнего IP-адреса. Мониторит публичный IP через ifconfig.me каждую минуту, фиксирует изменения и отправляет уведомления. Полезен для отслеживания переподключений, смены провайдера или динамических IP. Логирует в `~/.network_changes.log`.
 + [detect_new_devices_in_net.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/detect_new_devices_in_net.sh) - сканирование локальной сети на наличие новых устройств. Использует arp-scan для обнаружения MAC-адресов, сравнивает с сохранённым списком `~/.known_devices.txt` и уведомляет о новых девайсах. Требует установки `arp-scan`. Запускайте периодически для безопасности домашней сети.
 + [httpstatus.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/httpstatus.sh) - справочник HTTP-статус кодов. Выводит полный список кодов от 100 до 511 с описаниями. Поддерживает поиск по ключевым словам при передаче аргументов. Используйте как `./httpstatus.sh 404` для быстрого поиска или `./httpstatus.sh` для полного списка.
 + [list_of_wifi_nets.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/list_of_wifi_nets.sh) - мониторинг доступных Wi-Fi сетей в реальном времени. Показывает SSID, уровень сигнала и индикаторы качества, сортирует по силе сигнала. Обновляет список каждые 5 секунд. Использует nmcli. Запускайте при поиске лучшей точки доступа.
 + [monitoring_net_activity.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/monitoring_net_activity.sh) - мониторинг сетевого трафика в реальном времени. Измеряет скорость входящего (RX) и исходящего (TX) трафика на указанном интерфейсе (по умолчанию wlo1), обновляя данные каждую секунду. Показывает скорость в KB/s. Используйте для анализа загрузки сети.
 + [network_analysis.sh](https://github.com/alexeev-prog/usefulscripts/blob/main/shell_scripts/network_analysis.sh) - комплексный анализ сетевого состояния системы. Собирает статистику интерфейсов, подсчитывает соединения по состояниям, определяет топ-10 процессов по сетевой активности, показывает нестандартные открытые порты и статистику ошибок. Запускайте для диагностики сетевых проблем.

## Заключение
Спасибо за прочтение статьи! Я надеюсь, вы узнали что‑то новенькое, или, может, какой‑нибудь трюк натолкнул вас на другой интересный алгоритм. Если нашли нюанс в самой статье — пишите в комментарии.

Если вам понравился изложенный материал, могу предложить вам подписаться на [мой блог в телеграме](https://t.me/hex_warehouse). Если, конечно, вам статья понравилась и вы хотите видеть чуть больше.

А сами скрипты вы можете увидеть в [моем репозитории The Art Of Fun C](https://github.com/alexeev-prog/usefulscripts).

### Источники

 + ["Мои личные скрипты для повседневной работы"](https://habr.com/ru/companies/ruvds/articles/961514/)
