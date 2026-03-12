export MICRO_TRUECOLOR=1
export PYTHONDONTWRITEBYTECODE=1
export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH
export NIXPKGS_ALLOW_UNFREE=1
export NIXPKGS_ALLOW_INSECURE=1
export PATH="/home/alexeev/npm-packages/bin:/usr/local/bin/:$PATH"
export NODE_PATH="/home/alexeev/npm-packages/lib/node_modules"

set hydro_color_pwd green
set hydro_color_git yellow
set hydro_color_start blue
set hydro_color_error red
set hydro_color_prompt blue
set hydro_color_duration cyan

zoxide init fish | source

alias sortdir="python3 /home/alexeev/Desktop/Projects/usefulscripts/python_scripts/clean_downloads_dir.py"

alias ls='exa --icons'

alias rb="sudo nixos-rebuild switch --flake /home/alexeev/nixos/"
alias upd="nix flake update /home/alexeev/nixos/"
alias upg="sudo nixos-rebuild switch --upgrade --flake /home/alexeev/nixos/"
alias nixclean="sudo nix-collect-garbage -d"
alias hms="home-manager switch --flake /home/alexeev/nixos/"

alias conf="nvim nixos/nixos/configuration.nix"
alias pkgs="nvim nixos/nixos/packages.nix"

alias ll="ls -l"
alias se="sudoedit"
alias bat="bat --theme base16"
alias ff=fastfetch
alias nv=nvim
alias v=vim
alias nixfish="echo Enter to nix-shell && nix-shell . --command fish"

alias gga="git add"
alias ggc="git commit"
alias ggcm="git commit -m"
alias ggs="git status"
alias ggl="git log"
alias gglo="git log --oneline"
alias ggd="git diff"
alias ggds="git diff --staged"
alias ggr="git restore"
alias hg="history | grep "

alias ..='cd ..'
alias 2..='cd ../..'
alias 3..='cd ../../..'
alias 4..='cd ../../../..'
alias 5..='cd ../../../../..'

alias setupcargo="nix develop github:cargo2nix/cargo2nix#bootstrap"

set PATH $PATH /home/alexeev/.local/bin
set PATH $PATH /home/alexeev/npm-packages/bin
set PATH $PATH /home/alexeev/.cargo/bin

alias syslog_emerg="sudo dmesg --level=emerg,alert,crit"
alias syslog="sudo dmesg --level=err,warn"
alias xlog='grep "(EE)\|(WW)\|error\|failed" ~/.local/share/xorg/Xorg.0.log'
alias vacuum="sudo journalctl --vacuum-size=100M"
alias vacuum_time="sudo journalctl --vacuum-time=2weeks"
alias rm="rmtrash "
alias youtube='yt-dlp -f "bestvideo[height<=1080]+bestaudio" --merge-output-format mp4 --output "%(title)s.%(ext)s"'
alias youtubemp3='yt-dlp -x --audio-format mp3 --output "%(title)s_audio.%(ext)s"'

direnv hook fish | source
export NIXPKGS_ALLOW_INSECURE=1

export ALL_PROXY="http://127.0.0.1:1080"
export HTTP_PROXY="http://127.0.0.1:1080"
export HTTPS_PROXY="http://127.0.0.1:1080"

alias gitupdcom='git commit -m "Update $(date '\''+%Y-%m-%d %H:%M:%S'\'')"'
