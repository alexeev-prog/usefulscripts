#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
END='\033[0m'
BOLD='\033[1m'
GRAY='\033[2m'
ITALIC='\033[3m'

printf "${GRAY}   ____        __  _  ${BLUE}${BOLD}  ___              __   ${END}\n"
printf "${GRAY}  / __ \____  / /_(_) ${BLUE}${BOLD} /   |  __________/ /_  ${END}\n"
printf "${GRAY} / / / / __ \/ __/ / ${BLUE}${BOLD} / /| | / ___/ ___/ __ \ ${END}\n"
printf "${GRAY}/ /_/ / /_/ / /_/ / ${BLUE}${BOLD} / ___ |/ /  / /__/ / / / ${END}\n"
printf "${GRAY}\____/ .___/\__/_/ ${BLUE}${BOLD} /_/  |_/_/   \___/_/ /_/  ${END}\n"
printf "${GRAY}    /_/                                       ${END}\n"

printf "${CYAN}${ITALIC}  >  A tool for fast optimization of Arch${END}\n"
printf "Made with ${RED}love${END} by ${PURPLE}Alexeev Bronislav${END}\n\n"

COMMAND=$1

function is_pkg_installed() {
	pkg=$1
	if pacman -Qs "$pkg" > /dev/null; then
		printf "${ITALIC}${GREY}${pkg} is installed${END}\n"
	else
		printf "${CYAN}${ITALIC}${pkg} installing...${END}\n"
		sudo pacman -S $pkg --noconfirm
	fi
}

function update {
	printf "${BLUE}[+] Start full update${END}\n"
	printf "${CYAN}[+] Pacman keyring init...${END}\n"
	sudo pacman-key --init
	printf "${CYAN}[+] Pacman keyring populate by archlinux repo...${END}\n"
	sudo pacman-key --populate archlinux
	printf "${CYAN}[+] Pacman keyring refresh...${END}\n"
	sudo pacman-key --refresh-keys
	printf "${CYAN}[+] Full system update${END}\n"
	sudo pacman -Syu
}

function cachyos_kernel {
	printf "${BLUE}[+] Cachy OS optimized linux kernel installing...${END}\n"
	printf "${ITALIC}${CYAN}Download cachyos-repo.tar.xz...\n"
	wget https://mirror.cachyos.org/cachyos-repo.tar.xz
	printf "${ITALIC}${CYAN}Unpacking cachyos-repo.tar.xz...\n"
	tar xvf cachyos-repo.tar.xz
	rm cachyos-repo.tar.xz
	cd cachyos-repo
	printf "${YELLOW}${BOLD}Enter sudo password for start installion script\n"
	sudo ./cachyos-repo.sh
	printf "${ITALIC}${CYAN}Update system\n"
	sudo pacman -Syu
	printf "${ITALIC}${CYAN}Install linux-cachyos\n"
	sudo pacman -S linux-cachyos linux-cachyos-headers --noconfirm
	sudo grub-mkconfig -o /boot/grub/grub.cfg
	printf "${ITALIC}${CYAN}End\n"
}

function gnome_performance {
	printf "${BLUE}[+] Install default gnome desktop\n"
	is_pkg_installed "gnome"
	printf "${BLUE}[+] Install yay...\n"
	git clone https://aur.archlinux.org/yay.git /tmp/yay
	cd /tmp/yay || printf "${RED}[!] Error: /tmp/yay is not exists"; exit
	makepkg -sric
	printf "${BLUE}[+] Install gnome-shell-performance...\n"
	yay -S gnome-shell-performance --noconfirm
	printf "${BLUE}[+] Install mutter-performance...\n"
	yay -S mutter-performance --noconfirm
	printf "${ITALIC}${CYAN}End\n"

	printf "${YELLOW}[+] Mask org.gnome.SettingsDaemon.Wacom.service${END}\n"
	systemctl --user mask org.gnome.SettingsDaemon.Wacom.service
	printf "${YELLOW}[+] Mask org.gnome.SettingsDaemon.PrintNotifications.service${END}\n"
	systemctl --user mask org.gnome.SettingsDaemon.PrintNotifications.service
	printf "${YELLOW}[+] Mask org.gnome.SettingsDaemon.Color.service${END}\n" 
	systemctl --user mask org.gnome.SettingsDaemon.Color.service
	printf "${YELLOW}[+] Mask org.gnome.SettingsDaemon.A11ySettings.service${END}\n"
	systemctl --user mask org.gnome.SettingsDaemon.A11ySettings.service
	printf "${YELLOW}[+] Mask org.gnome.SettingsDaemon.UsbProtection.service${END}\n"
	systemctl --user mask org.gnome.SettingsDaemon.UsbProtection.service
	printf "${YELLOW}[+] Mask org.gnome.SettingsDaemon.ScreensaverProxy.service${END}\n"
	systemctl --user mask org.gnome.SettingsDaemon.ScreensaverProxy.service
	printf "${YELLOW}[+] Mask org.gnome.SettingsDaemon.Sharing.service${END}\n"
	systemctl --user mask org.gnome.SettingsDaemon.Sharing.service
	printf "${YELLOW}[+] Mask org.gnome.SettingsDaemon.Smartcard.service${END}\n"
	systemctl --user mask org.gnome.SettingsDaemon.Smartcard.service
	printf "${YELLOW}[+] Mask org.gnome.SettingsDaemon.Housekeeping.service${END}\n"
	systemctl --user mask org.gnome.SettingsDaemon.Housekeeping.service

	printf "${ITALIC}For unmask, use command: systemctl --user unmask --now <SERVICE>${END}\n"

	printf "${BLUE}[+] GNOME Desktop installing...${END}\n"
}

function install_ucode {
	printf "${BLUE}[+] Install CPU ucode${END}\n"

	cpu_info=$(cat /proc/cpuinfo | grep 'vendor_id' | uniq)

	if [[ $cpu_info == *"GenuineIntel"* ]]; then
		printf "${CYAN}[+] Install intel-ucode${END}\n"
		sudo pacman -S intel-ucode
	else
		printf "${CYAN}[+] Install amd-ucode${END}\n"
		sudo pacman -S amd-ucode
	fi
}

function install_videodrivers {
	printf "${BLUE}[+] Install video drivers${END}"

	gpu_info=$(lspci | grep -i 'vga\|3d\|2d')

	if [[ $gpu_info == *"AMD"* ]]; then
		printf "${CYAN}[+] Install AMD video-drivers${END}"
		sudo pacman -S lib32-mesa vulkan-radeon lib32-vulkan-radeon vulkan-icd-loader lib32-vulkan-icd-loader
	elif [[  $gpu_info == *"Intel"*  ]]; then
		printf "${CYAN}[+] Install Intel video-drivers${END}"
		sudo pacman -S lib32-mesa vulkan-intel lib32-vulkan-intel vulkan-icd-loader lib32-vulkan-icd-loader intel-media-driver libva-intel-driver xf86-video-intel
	else
		printf "${RED}[!] Error: GPU ${gpu_info} is not supported${END}"
	fi
	printf "${GREEN}[+] Success!${END}"
}

function base {
	printf "${BLUE}[+] Base optimization\n"

	update
	sudo pacman -S lrzip unrar unace p7zip squashfs-tools base-devel bash wget unzip tar git pacman-contrib nano vim --noconfirm
	install_ucode
	install_videodrivers
}

function full_min {
	update
	base
	cachyos_kernel
}

function full_max {
	full_min
	gnome_performance
}

if [[ "$COMMAND" = "--kernel" ]]; then
	update
	cachyos_kernel
	install_ucode
elif [[ "$COMMAND" = "--gnome" ]]; then
	update
	gnome_performance
elif [[ "$COMMAND" = "--update" ]]; then
	update
elif [[ "$COMMAND" = "--ucode" ]]; then
	install_ucode
elif [[ "$COMMAND" = "--minfull" ]]; then
	full_min
elif [[ "$COMMAND" = "--maxfull" ]]; then
	full_max
elif [[ "$COMMAND" = "--base" ]]; then
	install_ucode
elif [[ "$COMMAND" = '--videodrivers' ]]; then
	install_videodrivers
else
	printf "${ITALIC}Usage: --help; --kernel; --gnome; --update; --ucode; --minfull; --maxfull; --base; --videodrivers${END}\n"
	printf "${BOLD}kernel${END}: install CachyOS patched optimized kernel\n"
	printf "${BOLD}gnome${END}: install gnome with mutter-performance and gnome-shell-performance from AUR\n"
	printf "${BOLD}update${END}: just full system update (with keyring)\n"
	printf "${BOLD}ucode${END}: install ucode for processors (intel or amd)\n"
	printf "${BOLD}minfull${END}: maximum installing (without gnome)\n"
	printf "${BOLD}maxfull${END}: maximum installing (with gnome)\n"
	printf "${BOLD}base${END}: install reqs and deps (with keyring)\n"
	printf "${BOLD}videodrivers${END}: install video-drivers for intel or amd GPU\n"
	printf "${ITALIC}${BOLD}Recomendation: after optiarch.bash start clean.sh (for clean system)${END}\n"
	printf "${GRAY}\nOptiArch - optimization tool (C) Alexeev Bronislav 2024; licensed undo MIT${END}\n"
fi

printf "${GREEN}Please, star repository: https://github.com/AlexeevDeveloper/optiarch\n${END}"
