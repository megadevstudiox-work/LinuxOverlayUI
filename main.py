import sys
import os
import subprocess
import stat
import shutil
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QFileDialog, 
                             QMessageBox, QComboBox, QGroupBox, QListWidget, 
                             QListWidgetItem, QSystemTrayIcon, QMenu, QStyle, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QWindowStateChangeEvent

class MegaHardwareMonitorStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FPS PERFORMANCE ENGINE & HARDWARE MONITOR")
        self.resize(650, 750)
        
        self.msi_dir = os.path.expanduser("~/Desktop/msiafterburner")
        
        # Visual Styling (MSI Afterburner / MangoHud)
        self.setStyleSheet("""
            QMainWindow { background-color: #080a0f; }
            QLabel { color: #00FFCC; font-family: 'Fira Code', 'Courier New', monospace; font-weight: bold; }
            
            QGroupBox { 
                color: #FF5500; 
                font-weight: bold; 
                border: 1px solid #1a2233; 
                border-radius: 6px;
                margin-top: 10px; 
                padding: 12px; 
                background-color: #0d1117;
            }
            
            QListWidget {
                background-color: #05070a;
                border: 1px solid #00FFCC;
                border-radius: 5px;
                color: #FFFFFF;
                font-family: monospace;
                padding: 5px;
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #111827;
            }
            QListWidget::item:hover {
                background-color: #1f2937;
                color: #00FFCC;
            }
            QListWidget::item:selected {
                background-color: #FF5500;
                color: #FFFFFF;
            }
            
            QComboBox { 
                background-color: #111827; 
                color: #00FFCC; 
                border: 1px solid #00FFCC; 
                padding: 6px; 
                border-radius: 4px; 
                font-family: monospace; 
                font-weight: bold;
            }
            
            QPushButton {
                background-color: #00FFCC; 
                color: #000000; 
                font-weight: bold;
                border-radius: 6px; 
                padding: 12px; 
                font-size: 13px;
                border: none;
            }
            QPushButton:hover { background-color: #33FFDD; }
            QPushButton:pressed { background-color: #FF5500; color: #FFFFFF; }
        """)

        # System Tray Icon Setup
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)) 
        
        tray_menu = QMenu()
        restore_action = QAction("Open Monitor", self)
        restore_action.triggered.connect(self.restore_from_tray)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        
        tray_menu.addAction(restore_action)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

        # Scrollable Area Layout
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)
        
        self.central_widget = QWidget()
        scroll.setWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Title Label
        self.title_label = QLabel("⚡ HARDWARE MONITOR & OSD CONTROL ENGINE ⚡", self)
        self.title_label.setStyleSheet("color: #00FFCC; font-size: 15px; letter-spacing: 1px;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # 64-Bit Tool Installation Button
        self.btn_install_tools = QPushButton("🛠️ INSTALL MANGO HUD, WINE, DXVK, VULKAN & OPENGL (64-BIT)", self)
        self.btn_install_tools.setStyleSheet("QPushButton { background-color: #111827; color: #FF5500; border: 1px solid #FF5500; } QPushButton:hover { background-color: #1f2937; }")
        self.btn_install_tools.clicked.connect(self.install_all_tools_64bit)
        self.layout.addWidget(self.btn_install_tools)

        # Execution Target Platform
        self.group_plat = QGroupBox("1. Execution Platform")
        plat_layout = QVBoxLayout()
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Linux Native 64-Bit (Apps / Games)",
            "Windows EXE 64-Bit (Wine + DXVK Vulkan)"
        ])
        plat_layout.addWidget(self.type_combo)
        self.group_plat.setLayout(plat_layout)
        self.layout.addWidget(self.group_plat)

        # Hardware Component Selection
        self.group_hw = QGroupBox("2. Select Hardware Components for OSD (MSI Style)")
        hw_layout = QVBoxLayout()
        
        self.hw_list = QListWidget()
        self.hardware_items = [
            ("GPU Model Name", "gpu_name", True),
            ("GPU Usage, Temp (°C) & Clock (Mhz)", "gpu_stats", True),
            ("GPU Power Draw (W)", "gpu_power", True),
            ("VRAM Memory Usage & Clock", "vram", True),
            ("CPU Model Name", "cpu_name", True),
            ("CPU Usage, Temp (°C) & Clock (Mhz)", "cpu_stats", True),
            ("CPU Power Draw (W)", "cpu_power", True),
            ("System RAM Usage", "ram", True),
            ("FPS & Frametime Graph", "fps", True),
            ("Frametime Min/Max Stats", "frame_timing", True),
            ("Graphics Engine (DXVK / VKD3D / OpenGL / DirectX)", "engine_version", True),
            ("Distro Name & Kernel Version", "core_stats", True),
            ("System Resolution & Refresh Rate", "resolution", True)
        ]

        for name, key, default_state in self.hardware_items:
            item = QListWidgetItem(f"   [ in OSD ]  {name}")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if default_state else Qt.CheckState.Unchecked)
            item.setData(Qt.ItemDataRole.UserRole, key)
            self.hw_list.addItem(item)

        hw_layout.addWidget(self.hw_list)
        self.group_hw.setLayout(hw_layout)
        self.layout.addWidget(self.group_hw)

        # Position and Visual Customization
        self.group_options = QGroupBox("3. On-Screen Display Configuration")
        opt_layout = QHBoxLayout()
        
        self.pos_combo = QComboBox()
        self.pos_combo.addItems(["top-left", "top-right", "bottom-left", "bottom-right", "top-center"])
        
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Dark Background", "Transparent Background", "Neon Color Theme"])
        
        opt_layout.addWidget(QLabel("Position:"))
        opt_layout.addWidget(self.pos_combo)
        opt_layout.addWidget(QLabel("Theme:"))
        opt_layout.addWidget(self.font_combo)
        
        self.group_options.setLayout(opt_layout)
        self.layout.addWidget(self.group_options)

        # Launch Button
        self.btn_launch = QPushButton("🚀 SELECT GAME AND LAUNCH WITH OVERLAY 🚀", self)
        self.btn_launch.clicked.connect(self.launch_file)
        self.layout.addWidget(self.btn_launch)

        self.status_label = QLabel("Ready to launch...", self)
        self.status_label.setStyleSheet("color: #888888; font-size: 11px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status_label)

    # Handlers for minimizing directly to system tray
    def changeEvent(self, event):
        if event.type() == event.Type.WindowStateChange:
            if self.isMinimized():
                self.hide()
                event.ignore()
                return
        super().changeEvent(event)

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def restore_from_tray(self):
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.activateWindow()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.restore_from_tray()

    def install_all_tools_64bit(self):
        try:
            self.status_label.setText("STATUS: Installing 64-bit tools...")
            QApplication.processEvents()
            
            bash_script = """#!/bin/bash
echo "======================================================================="
echo " 64-BIT TOOL INSTALLATION: MANGO HUD, WINE, DXVK, VULKAN & OPENGL "
echo "======================================================================="
sudo apt update
sudo apt install -y mangohud wine64 winetricks vulkan-tools libgl1-mesa-dri mesa-vulkan-drivers

echo "--- Installing DXVK 64-bit via Winetricks ---"
WINEPREFIX=~/.wine winetricks -q dxvk

echo ""
echo "All tools have been installed successfully!"
read -p "Press [ENTER] to close this window..."
"""
            script_path = "/tmp/install_64bit_tools.sh"
            with open(script_path, "w") as f:
                f.write(bash_script)
            
            os.chmod(script_path, 0o755)
            subprocess.Popen(["x-terminal-emulator", "-e", script_path])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Installation failed: {str(e)}")

    def build_mangohud_config(self):
        config_dir = os.path.expanduser("~/.config/MangoHud")
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "MangoHud.conf")
        
        position = self.pos_combo.currentText()
        theme_index = self.font_combo.currentIndex()
        
        bg_alpha = "0.85"
        bg_color = "020B14"
        if theme_index == 1:
            bg_alpha = "0.0"
        elif theme_index == 2:
            bg_color = "05131D"

        lines = [
            "legacy_layout=0",
            f"position={position}",
            f"background_alpha={bg_alpha}",
            f"background_color={bg_color}",
            "text_color=FFFFFF",
            "font_size=24",
            "round_corners=8"
        ]

        for i in range(self.hw_list.count()):
            item = self.hw_list.item(i)
            key = item.data(Qt.ItemDataRole.UserRole)
            
            if item.checkState() == Qt.CheckState.Checked:
                if key == "gpu_name":
                    lines.append("gpu_name")
                elif key == "gpu_stats":
                    lines.extend(["gpu_stats", "gpu_temp", "gpu_core_clock", "gpu_color=46FF00"])
                elif key == "gpu_power":
                    lines.append("gpu_power")
                elif key == "vram":
                    lines.extend(["vram", "vram_color=46FF00"])
                elif key == "cpu_name":
                    lines.append("cpu_mhz")
                elif key == "cpu_stats":
                    lines.extend(["cpu_stats", "cpu_temp", "cpu_mhz", "cpu_color=367BFF"])
                elif key == "cpu_power":
                    lines.append("cpu_power")
                elif key == "ram":
                    lines.extend(["ram", "ram_color=367BFF"])
                elif key == "fps":
                    lines.extend(["fps", "fps_color=00FFCC", "frametime=1"])
                elif key == "frame_timing":
                    lines.append("frame_timing=1")
                elif key == "engine_version":
                    lines.extend(["engine_version", "vulkan_driver"])
                elif key == "core_stats":
                    lines.extend(["version", "architecture"])
                elif key == "resolution":
                    lines.append("resolution")

        with open(config_path, "w") as f:
            f.write("\n".join(lines))

    def launch_file(self):
        self.build_mangohud_config()
        
        selected_index = self.type_combo.currentIndex()
        file_filter = "All Files (*)" if selected_index == 0 else "Windows Executables (*.exe)"
        
        app_path, _ = QFileDialog.getOpenFileName(self, "Select Game Executable", os.path.expanduser("~"), file_filter)
        if not app_path:
            return

        game_dir = os.path.dirname(app_path)
        wrapper_path = os.path.join(game_dir, "run_game_osd.sh")
        
        lines = [
            "#!/bin/bash",
            f"cd \"{game_dir}\"",
            "export MANGOHUD=1",
            "export MANGOHUD_DLSYM=1"
        ]

        if selected_index == 1:
            wine_bin = "wine64" if shutil.which("wine64") else "wine"
            lines.append("export WINE_D3D_CONFIG=\"backend=vulkan\"")
            lines.append(f"exec mangohud {wine_bin} \"{app_path}\" > wine_game.log 2>&1")
        else:
            lines.append(f"exec mangohud --dlsym \"{app_path}\" \"$@\"")

        with open(wrapper_path, "w") as f:
            f.write("\n".join(lines))

        os.chmod(wrapper_path, os.stat(wrapper_path).st_mode | stat.S_IEXEC)
        
        try:
            subprocess.Popen([wrapper_path], cwd=game_dir)
            self.status_label.setText(f"Successfully launched: {os.path.basename(app_path)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to launch executable!\n\nDetails: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MegaHardwareMonitorStudio()
    window.show()
    sys.exit(app.exec())