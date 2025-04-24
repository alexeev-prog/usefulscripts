#!/bin/bash

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
