# Useful Scripts

A curated collection of practical Bash, Python, and Ruby scripts for system administration, development, and automation tasks.

## Project Structure

### Shell Scripts

```bash
shell_scripts/
├── system_info/
│   ├── check-cpu.sh              # Display CPU information (AMD/Intel)
│   ├── check-gpu.sh              # Display GPU information (AMD/NVIDIA/Intel)
│   └── check_disk_space.sh       # Analyze disk usage and storage capacity
├── system_monitoring/
│   ├── monitoring_cpu_gpu_temp.sh    # Real-time CPU and GPU temperature monitoring
│   ├── check_high_cpu_usage.sh       # Identify processes with excessive CPU utilization
│   ├── memory_analysis.sh            # Comprehensive memory usage analysis
│   ├── io_analysis.sh                # I/O performance and activity monitoring
│   └── network_analysis.sh           # Network interface and bandwidth analysis
├── network_utilities/
│   ├── monitoring_net_activity.sh    # Continuous network traffic monitoring
│   ├── detect_network_changes.sh     # Detect and alert on network configuration changes
│   ├── detect_new_devices_in_net.sh  # Identify new devices on the network
│   ├── check_wifi_status.sh          # Display current WiFi connection status
│   ├── check_wifi_connection.sh      # Verify WiFi connectivity and signal strength
│   ├── list_of_wifi_nes.sh           # Scan and list available WiFi networks
│   └── httpstatus.sh                 # HTTP status code explanations (e.g., 301 → Moved Permanently)
├── device_management/
│   ├── auto_mount_devices.sh         # Automatic mounting of USB storage devices
│   ├── check_usb_devices.sh          # List connected USB devices and their properties
│   └── detect_usb_ejection.sh        # Monitor and detect USB device removal
├── system_maintenance/
│   ├── clean_arch.sh                 # Comprehensive cleanup utilities for Arch Linux
│   ├── optiarch.sh                   # System optimization for Arch Linux
│   ├── clean_broken_links.sh         # Identify and remove broken symbolic links
│   ├── delete_old_temp_files.sh      # Remove stale temporary files from /tmp/
│   ├── restart_frozen_systemd_services.sh  # Restart unresponsive systemd services
│   ├── kill_undead_processes.sh      # Terminate frozen or unresponsive processes
│   └── coredumps_watch.sh            # Monitor and manage core dump files
├── development_tools/
│   ├── check_files_inotify.sh        # File system monitoring using inotify
│   ├── jsonformat.sh                 # JSON formatting and validation
│   ├── grepline.sh                   # Extract specific line ranges from text (head | tail wrapper)
│   └── slowest_services_to_launch.sh # Analyze systemd service startup times
└── productivity/
    ├── mkcd.sh                       # Create directory and navigate to it
    ├── mksh.sh                       # Create shell script template and open for editing
    ├── tempe.sh                      # Create and enter temporary workspace directory
    └── emoji.sh                      # Emoji lookup by name (e.g., "heart" → ♥️)
```

### Python Scripts

```bash
python_scripts/
├── web_utilities/
│   ├── check_website_access.py       # Website accessibility and response time checking
│   ├── check_website_ssl_cert.py     # SSL certificate validation and expiration monitoring
│   ├── create_short_url.py           # URL shortening service integration
│   └── urldesc.py                    # URL parsing and component analysis
├── code_quality/
│   ├── format-code.py                # Python code formatting with black, ruff, and isort
│   ├── format-cx-code.py             # C/C++ code formatting and style enforcement
│   ├── analyze_cpp_code.py           # C++ code analysis and quality assessment
│   └── get_git_version.py            # Git repository version and branch information
├── file_management/
│   ├── clean_downloads_dir.py        # Automated download directory organization and sorting
│   └── full_files_renamer.py         # Batch file renaming with date/time patterns
└── requirements.txt                   # Python dependencies and package requirements
```

### Ruby Scripts

```bash
ruby_scripts/
└── getuuid.ruby                      # UUID generation and validation utilities
```

## Installation

The project includes an installation script to deploy all utilities to your local binary directory:

```bash
./installer.sh
```

This will install all scripts to `~/.local/bin/` for easy command-line access.

## Requirements

### Python Dependencies
Install required Python packages:
```bash
pip install -r python_scripts/requirements.txt
```

## Documentation

- **CHANGELOG.md**: Version history and update records
- **LICENSE**: Project licensing information

## Contributors

Acknowledgments to:

- **qdiaps** - Initial implementation of system temperature monitoring scripts

---

*Designed for developers and system administrators seeking robust automation and monitoring solutions.*
