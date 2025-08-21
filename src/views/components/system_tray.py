"""
Module de barre système fournissant l'icône de la barre, le menu et l'indication d'état.
"""

from typing import Optional

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QIcon, QPainter, QPixmap
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon, QWidget

from src.utils.logging_config import get_logger


class SystemTray(QObject):
    """
    Composant de la barre système.
    """

    # 定义信号
    show_window_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    quit_requested = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.logger = get_logger("SystemTray")
        self.parent_widget = parent

        # 托盘相关组件
        self.tray_icon = None
        self.tray_menu = None

        # 状态相关
        self.current_status = ""
        self.is_connected = True

        # 初始化托盘
        self._setup_tray()

    def _setup_tray(self):
        """
        Configure l'icône de la barre système.
        """
        try:
            # 检查系统是否支持系统托盘
            if not QSystemTrayIcon.isSystemTrayAvailable():
                self.logger.warning("Le système ne prend pas en charge la barre système")
                return

            # 创建托盘菜单
            self._create_tray_menu()

            # 创建系统托盘图标（不绑定 QWidget 作为父对象，避免窗口生命周期影响托盘图标，防止 macOS 下隐藏/关闭时崩溃）
            self.tray_icon = QSystemTrayIcon()
            self.tray_icon.setContextMenu(self.tray_menu)

            # 连接托盘图标的事件
            self.tray_icon.activated.connect(self._on_tray_activated)

            # 设置初始图标（避免在某些平台第一次绘制引发崩溃，延迟到事件循环空闲时执行）
            try:
                from PyQt5.QtCore import QTimer

                QTimer.singleShot(0, lambda: self.update_status("待命", connected=True))
            except Exception:
                self.update_status("待命", connected=True)

            # 显示系统托盘图标
            self.tray_icon.show()
            self.logger.info("Icône de la barre système initialisée")

        except Exception as e:
            self.logger.error(
                f"Échec de l'initialisation de l'icône de barre système : {e}",
                exc_info=True,
            )

    def _create_tray_menu(self):
        """
        Crée le menu contextuel de la barre système.
        """
        self.tray_menu = QMenu()

        # Élément de menu pour afficher la fenêtre principale
        show_action = QAction("Afficher la fenêtre principale", self.parent_widget)
        show_action.triggered.connect(self._on_show_window)
        self.tray_menu.addAction(show_action)

        # 添加分隔线
        self.tray_menu.addSeparator()

        # Élément de menu des paramètres
        settings_action = QAction("Paramètres", self.parent_widget)
        settings_action.triggered.connect(self._on_settings)
        self.tray_menu.addAction(settings_action)

        # 添加分隔线
        self.tray_menu.addSeparator()

        # Élément de menu pour quitter
        quit_action = QAction("Quitter le programme", self.parent_widget)
        quit_action.triggered.connect(self._on_quit)
        self.tray_menu.addAction(quit_action)

    def _on_tray_activated(self, reason):
        """
          Gère le clic sur l'icône de la barre système.
        """
        if reason == QSystemTrayIcon.Trigger:  # 单击
            self.show_window_requested.emit()

    def _on_show_window(self):
        """
          Gère le clic sur l'élément "Afficher la fenêtre".
        """
        self.show_window_requested.emit()

    def _on_settings(self):
        """
          Gère le clic sur l'élément "Paramètres".
        """
        self.settings_requested.emit()

    def _on_quit(self):
        """
          Gère le clic sur l'élément "Quitter".
        """
        self.quit_requested.emit()

    def update_status(self, status: str, connected: bool = True):
        """Met à jour l'état de l'icône de la barre système.

        Args:
            status: texte d'état (en chinois)
            connected: état de connexion
        """
        if not self.tray_icon:
            return

        self.current_status = status
        self.is_connected = connected

        try:
            icon_color = self._get_status_color(status, connected)

            # 创建指定颜色的图标
            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor(0, 0, 0, 0))  # 透明背景

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(icon_color))
            painter.setPen(QColor(0, 0, 0, 0))  # 透明边框
            painter.drawEllipse(2, 2, 12, 12)
            painter.end()

            # 设置图标
            self.tray_icon.setIcon(QIcon(pixmap))

            # Définir le texte de l'info-bulle
            tooltip = f"Assistant IA Xiaozhi - {self._translate_status(status)}"
            self.tray_icon.setToolTip(tooltip)

        except Exception as e:
            self.logger.error(
                f"Échec de la mise à jour de l'icône de barre système : {e}"
            )

    def _get_status_color(self, status: str, connected: bool) -> QColor:
        """Renvoie la couleur correspondant à l'état.

        Args:
            status: texte d'état
            connected: état de connexion

        Returns:
            QColor: couleur correspondante
        """
        if not connected:
            return QColor(128, 128, 128)  # 灰色 - 未连接

        if "错误" in status:
            return QColor(255, 0, 0)  # Rouge - erreur
        elif "聆听中" in status:
            return QColor(255, 200, 0)  # Jaune - en écoute
        elif "说话中" in status:
            return QColor(0, 120, 255)  # Bleu - en train de parler
        else:
            return QColor(0, 180, 0)  # Vert - en attente/démarré

    def _translate_status(self, status: str) -> str:
        """Traduit les états chinois en français pour l'affichage."""
        mapping = {
            "待命": "En attente",
            "聆听中": "En écoute",
            "说话中": "En train de parler",
            "错误": "Erreur",
        }
        return mapping.get(status, status)

    def show_message(
        self,
        title: str,
        message: str,
        icon_type=QSystemTrayIcon.Information,
        duration: int = 2000,
    ):
        """显示托盘通知消息.

        Args:
            title: 通知标题
            message: 通知内容
            icon_type: 图标类型
            duration: 显示时间(毫秒)
        """
        if self.tray_icon and self.tray_icon.isVisible():
            self.tray_icon.showMessage(title, message, icon_type, duration)

    def hide(self):
        """
        隐藏托盘图标.
        """
        if self.tray_icon:
            self.tray_icon.hide()

    def is_visible(self) -> bool:
        """
        检查托盘图标是否可见.
        """
        return self.tray_icon and self.tray_icon.isVisible()

    def is_available(self) -> bool:
        """
        检查系统托盘是否可用.
        """
        return QSystemTrayIcon.isSystemTrayAvailable()
