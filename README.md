# 🚀 LinuxOverlay UI

**LinuxOverlay UI** is a lightweight, open-source performance monitoring interface designed for Linux gamers. It provides an intuitive GUI to control and display system metrics (CPU, GPU, RAM, FPS, temperatures) as a standalone alternative to terminal-based MangoHud setups.

---

## 📜 License

This project is licensed under the terms of the **MIT License**.

```text
MIT License

Copyright (c) 2026 Mega Dev Studio X

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
⚙️ Prerequisites & System Requirements
Before testing or running LinuxOverlay UI, ensure your system meets the following requirements:

Supported Distributions: Ubuntu 24.04 x64+, Debian 13 x64+, Fedora 40+, SteamOS 3.6+ x64, Arch Linux (Requires GLIBC 2.39 or newer).

Architecture: 64-bit Linux environments only (x86_64).

Game Compatibility: Works with 64-bit games only (32-bit x86 games are not supported).

Wine Tools: Full Wine / Proton environment pre-installed: WineHQ Official Website

Required Dependency (python3-pyqt6)
Install the required PyQt6 library for your distribution using one of the following commands:

Ubuntu / Debian / Linux Mint:

Bash
sudo apt update && sudo apt install -y python3-pyqt6
Fedora:

Bash
sudo dnf install -y python3-qt6
Arch Linux / Manjaro:

Bash
sudo pacman -S --needed python-pyqt6
💻 How to Run from Source Code
If you downloaded the repository as a .zip file:

Extract the ZIP file to a folder on your machine.

Open the extracted directory and navigate through the subfolders until you locate main.py.

Open a terminal inside that folder.

Run the application with:

Bash
python3 main.py
📦 How to Run the AppImage
Download the LinuxOverlayUI.AppImage executable.

Right-click the .AppImage file → Properties → Permissions → Check "Allow executing file as program".

Double-click to launch, or run via terminal:

Bash
chmod +x LinuxOverlayUI.AppImage
./LinuxOverlayUI.AppImage
🤝 Community Contributions & Support
Lots of hard work went into developing this application! As an independent developer, I warmly welcome feedback, bug reports, and contributions from the Linux community to help improve this tool.

Report Issues: Open an issue on GitHub if you encounter bugs or compatibility problems.

Contribute: Feel free to fork the repository, refine the codebase, and submit Pull Requests.

Spread the Word: Share your suggestions and ideas to make gaming on Linux even better!

Thank you all for your support! ❤️
