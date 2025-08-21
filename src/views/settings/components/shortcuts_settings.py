from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class ShortcutsSettingsWidget(QWidget):
    """
    Composant de configuration des raccourcis.
    """

    # 信号定义
    settings_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager.get_instance()
        self.shortcuts_config = self.config.get_config("SHORTCUTS", {})
        self.init_ui()

    def init_ui(self):
        """
        Initialise l'interface utilisateur.
        """
        layout = QVBoxLayout()

        # Option d'activation des raccourcis
        self.enable_checkbox = QCheckBox("Activer les raccourcis globaux")
        self.enable_checkbox.setChecked(self.shortcuts_config.get("ENABLED", True))
        self.enable_checkbox.toggled.connect(self.on_settings_changed)
        layout.addWidget(self.enable_checkbox)

        # Groupe de configuration des raccourcis
        shortcuts_group = QGroupBox("Configuration des raccourcis")
        shortcuts_layout = QVBoxLayout()

        # Créer les widgets de configuration pour chaque raccourci
        self.shortcut_widgets = {}

        # Appuyer pour parler
        self.shortcut_widgets["MANUAL_PRESS"] = self.create_shortcut_config(
            "Appuyer pour parler", self.shortcuts_config.get("MANUAL_PRESS", {})
        )
        shortcuts_layout.addWidget(self.shortcut_widgets["MANUAL_PRESS"])

        # Conversation automatique
        self.shortcut_widgets["AUTO_TOGGLE"] = self.create_shortcut_config(
            "Conversation automatique", self.shortcuts_config.get("AUTO_TOGGLE", {})
        )
        shortcuts_layout.addWidget(self.shortcut_widgets["AUTO_TOGGLE"])

        # Interrompre la conversation
        self.shortcut_widgets["ABORT"] = self.create_shortcut_config(
            "Interrompre la conversation", self.shortcuts_config.get("ABORT", {})
        )
        shortcuts_layout.addWidget(self.shortcut_widgets["ABORT"])

        # Changer de mode
        self.shortcut_widgets["MODE_TOGGLE"] = self.create_shortcut_config(
            "Changer de mode", self.shortcuts_config.get("MODE_TOGGLE", {})
        )
        shortcuts_layout.addWidget(self.shortcut_widgets["MODE_TOGGLE"])

        # Afficher/Masquer la fenêtre
        self.shortcut_widgets["WINDOW_TOGGLE"] = self.create_shortcut_config(
            "Afficher/Masquer la fenêtre", self.shortcuts_config.get("WINDOW_TOGGLE", {})
        )
        shortcuts_layout.addWidget(self.shortcut_widgets["WINDOW_TOGGLE"])

        shortcuts_group.setLayout(shortcuts_layout)
        layout.addWidget(shortcuts_group)

        # Zone de boutons
        btn_layout = QHBoxLayout()
        self.reset_btn = QPushButton("Réinitialiser")
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        btn_layout.addWidget(self.reset_btn)

        self.apply_btn = QPushButton("Appliquer")
        self.apply_btn.clicked.connect(self.apply_settings)
        btn_layout.addWidget(self.apply_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def create_shortcut_config(self, title, config):
        """
        Crée un widget de configuration de raccourci.
        """
        widget = QWidget()
        layout = QHBoxLayout()

        # Titre
        layout.addWidget(QLabel(f"{title}:"))

        # Sélection du modificateur
        modifier_combo = QComboBox()
        modifier_combo.addItems(["Ctrl", "Alt", "Shift"])
        current_modifier = config.get("modifier", "ctrl").title()
        modifier_combo.setCurrentText(current_modifier)
        modifier_combo.currentTextChanged.connect(self.on_settings_changed)
        layout.addWidget(modifier_combo)

        # Sélection de la touche
        key_combo = QComboBox()
        key_combo.addItems([chr(i) for i in range(ord("a"), ord("z") + 1)])  # a-z
        current_key = config.get("key", "j").lower()
        key_combo.setCurrentText(current_key)
        key_combo.currentTextChanged.connect(self.on_settings_changed)
        layout.addWidget(key_combo)

        widget.setLayout(layout)
        widget.modifier_combo = modifier_combo
        widget.key_combo = key_combo
        return widget

    def on_settings_changed(self):
        """
        Rappel lors d'un changement de configuration.
        """
        self.settings_changed.emit()

    def apply_settings(self):
        """
        Applique les paramètres.
        """
        try:
            # 更新启用状态
            self.config.update_config(
                "SHORTCUTS.ENABLED", self.enable_checkbox.isChecked()
            )

            # 更新各个快捷键配置
            for key, widget in self.shortcut_widgets.items():
                modifier = widget.modifier_combo.currentText().lower()
                key_value = widget.key_combo.currentText().lower()

                self.config.update_config(f"SHORTCUTS.{key}.modifier", modifier)
                self.config.update_config(f"SHORTCUTS.{key}.key", key_value)

            # 重新加载配置
            self.config.reload_config()
            self.shortcuts_config = self.config.get_config("SHORTCUTS", {})

            logger.info("Paramètres des raccourcis sauvegardés")

        except Exception as e:
            logger.error(f"Échec de l'enregistrement des raccourcis : {e}")

    def reset_to_defaults(self):
        """
        Restaure les paramètres par défaut.
        """
        # Configuration par défaut
        defaults = {
            "ENABLED": True,
            "MANUAL_PRESS": {"modifier": "ctrl", "key": "j"},
            "AUTO_TOGGLE": {"modifier": "ctrl", "key": "k"},
            "ABORT": {"modifier": "ctrl", "key": "q"},
            "MODE_TOGGLE": {"modifier": "ctrl", "key": "m"},
            "WINDOW_TOGGLE": {"modifier": "ctrl", "key": "w"},
        }

        # Mettre à jour l'UI
        self.enable_checkbox.setChecked(defaults["ENABLED"])

        for key, config in defaults.items():
            if key == "ENABLED":
                continue

            widget = self.shortcut_widgets.get(key)
            if widget:
                widget.modifier_combo.setCurrentText(config["modifier"].title())
                widget.key_combo.setCurrentText(config["key"].lower())

        # Déclencher le signal de changement
        self.on_settings_changed()
