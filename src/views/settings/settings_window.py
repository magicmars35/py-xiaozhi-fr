from pathlib import Path

from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTextEdit,
)

from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger
from src.utils.resource_finder import get_project_root, resource_finder
from src.views.settings.components.shortcuts_settings import ShortcutsSettingsWidget


class SettingsWindow(QDialog):
    """
    Fenêtre de configuration des paramètres.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(__name__)
        self.config_manager = ConfigManager.get_instance()

        # UI控件
        self.ui_controls = {}

        # 快捷键设置组件
        self.shortcuts_tab = None

        # 初始化UI
        self._setup_ui()
        self._connect_events()
        self._load_config_values()

    def _setup_ui(self):
        """
        Configure l'interface utilisateur.
        """
        try:
            from PyQt5 import uic

            ui_path = Path(__file__).parent / "settings_window.ui"
            uic.loadUi(str(ui_path), self)

            # 获取所有UI控件的引用
            self._get_ui_controls()

            # 添加快捷键设置选项卡
            self._add_shortcuts_tab()

        except Exception as e:
            self.logger.error(f"Échec de la configuration de l'UI : {e}", exc_info=True)
            raise

    def _add_shortcuts_tab(self):
        """
        Ajoute l'onglet de configuration des raccourcis.
        """
        try:
            # 获取TabWidget
            tab_widget = self.findChild(QTabWidget, "tabWidget")
            if not tab_widget:
                self.logger.error("Contrôle TabWidget introuvable")
                return

            # Crée le composant de configuration des raccourcis
            self.shortcuts_tab = ShortcutsSettingsWidget()

            # Ajoute à l'onglet
            tab_widget.addTab(self.shortcuts_tab, "Raccourcis")

            # 连接信号
            self.shortcuts_tab.settings_changed.connect(self._on_settings_changed)

            self.logger.debug("Onglet de raccourcis ajouté avec succès")

        except Exception as e:
            self.logger.error(f"Échec de l'ajout de l'onglet de raccourcis : {e}", exc_info=True)

    def _on_settings_changed(self):
        """
        Rappel lors d'un changement de paramètre.
        """
        # Des informations ou autres logiques peuvent être ajoutées ici

    def _get_ui_controls(self):
        """
        Obtient les références des contrôles UI.
        """
        # 系统选项控件
        self.ui_controls.update(
            {
                "client_id_edit": self.findChild(QLineEdit, "client_id_edit"),
                "device_id_edit": self.findChild(QLineEdit, "device_id_edit"),
                "ota_url_edit": self.findChild(QLineEdit, "ota_url_edit"),
                "websocket_url_edit": self.findChild(QLineEdit, "websocket_url_edit"),
                "websocket_token_edit": self.findChild(
                    QLineEdit, "websocket_token_edit"
                ),
                "authorization_url_edit": self.findChild(
                    QLineEdit, "authorization_url_edit"
                ),
                "activation_version_combo": self.findChild(
                    QComboBox, "activation_version_combo"
                ),
            }
        )

        # MQTT配置控件
        self.ui_controls.update(
            {
                "mqtt_endpoint_edit": self.findChild(QLineEdit, "mqtt_endpoint_edit"),
                "mqtt_client_id_edit": self.findChild(QLineEdit, "mqtt_client_id_edit"),
                "mqtt_username_edit": self.findChild(QLineEdit, "mqtt_username_edit"),
                "mqtt_password_edit": self.findChild(QLineEdit, "mqtt_password_edit"),
                "mqtt_publish_topic_edit": self.findChild(
                    QLineEdit, "mqtt_publish_topic_edit"
                ),
                "mqtt_subscribe_topic_edit": self.findChild(
                    QLineEdit, "mqtt_subscribe_topic_edit"
                ),
            }
        )

        # 唤醒词配置控件
        self.ui_controls.update(
            {
                "use_wake_word_check": self.findChild(QCheckBox, "use_wake_word_check"),
                "model_path_edit": self.findChild(QLineEdit, "model_path_edit"),
                "model_path_btn": self.findChild(QPushButton, "model_path_btn"),
                "wake_words_edit": self.findChild(QTextEdit, "wake_words_edit"),
            }
        )

        # 摄像头配置控件
        self.ui_controls.update(
            {
                "camera_index_spin": self.findChild(QSpinBox, "camera_index_spin"),
                "frame_width_spin": self.findChild(QSpinBox, "frame_width_spin"),
                "frame_height_spin": self.findChild(QSpinBox, "frame_height_spin"),
                "fps_spin": self.findChild(QSpinBox, "fps_spin"),
                "local_vl_url_edit": self.findChild(QLineEdit, "local_vl_url_edit"),
                "vl_api_key_edit": self.findChild(QLineEdit, "vl_api_key_edit"),
                "models_edit": self.findChild(QLineEdit, "models_edit"),
            }
        )

        # 按钮控件
        self.ui_controls.update(
            {
                "save_btn": self.findChild(QPushButton, "save_btn"),
                "cancel_btn": self.findChild(QPushButton, "cancel_btn"),
                "reset_btn": self.findChild(QPushButton, "reset_btn"),
            }
        )

    def _connect_events(self):
        """
        Connecte les gestionnaires d'événements.
        """
        if self.ui_controls["save_btn"]:
            self.ui_controls["save_btn"].clicked.connect(self._on_save_clicked)

        if self.ui_controls["cancel_btn"]:
            self.ui_controls["cancel_btn"].clicked.connect(self.reject)

        if self.ui_controls["reset_btn"]:
            self.ui_controls["reset_btn"].clicked.connect(self._on_reset_clicked)

        if self.ui_controls["model_path_btn"]:
            self.ui_controls["model_path_btn"].clicked.connect(
                self._on_model_path_browse
            )

    def _load_config_values(self):
        """
        Charge les valeurs de configuration dans les contrôles UI.
        """
        try:
            # 系统选项
            client_id = self.config_manager.get_config("SYSTEM_OPTIONS.CLIENT_ID", "")
            self._set_text_value("client_id_edit", client_id)

            device_id = self.config_manager.get_config("SYSTEM_OPTIONS.DEVICE_ID", "")
            self._set_text_value("device_id_edit", device_id)

            ota_url = self.config_manager.get_config(
                "SYSTEM_OPTIONS.NETWORK.OTA_VERSION_URL", ""
            )
            self._set_text_value("ota_url_edit", ota_url)

            websocket_url = self.config_manager.get_config(
                "SYSTEM_OPTIONS.NETWORK.WEBSOCKET_URL", ""
            )
            self._set_text_value("websocket_url_edit", websocket_url)

            websocket_token = self.config_manager.get_config(
                "SYSTEM_OPTIONS.NETWORK.WEBSOCKET_ACCESS_TOKEN", ""
            )
            self._set_text_value("websocket_token_edit", websocket_token)

            auth_url = self.config_manager.get_config(
                "SYSTEM_OPTIONS.NETWORK.AUTHORIZATION_URL", ""
            )
            self._set_text_value("authorization_url_edit", auth_url)

            # 激活版本
            activation_version = self.config_manager.get_config(
                "SYSTEM_OPTIONS.NETWORK.ACTIVATION_VERSION", "v1"
            )
            if self.ui_controls["activation_version_combo"]:
                combo = self.ui_controls["activation_version_combo"]
                combo.setCurrentText(activation_version)

            # MQTT配置
            mqtt_info = self.config_manager.get_config(
                "SYSTEM_OPTIONS.NETWORK.MQTT_INFO", {}
            )
            if mqtt_info:
                self._set_text_value(
                    "mqtt_endpoint_edit", mqtt_info.get("endpoint", "")
                )
                self._set_text_value(
                    "mqtt_client_id_edit", mqtt_info.get("client_id", "")
                )
                self._set_text_value(
                    "mqtt_username_edit", mqtt_info.get("username", "")
                )
                self._set_text_value(
                    "mqtt_password_edit", mqtt_info.get("password", "")
                )
                self._set_text_value(
                    "mqtt_publish_topic_edit", mqtt_info.get("publish_topic", "")
                )
                self._set_text_value(
                    "mqtt_subscribe_topic_edit", mqtt_info.get("subscribe_topic", "")
                )

            # 唤醒词配置
            use_wake_word = self.config_manager.get_config(
                "WAKE_WORD_OPTIONS.USE_WAKE_WORD", False
            )
            if self.ui_controls["use_wake_word_check"]:
                self.ui_controls["use_wake_word_check"].setChecked(use_wake_word)

            self._set_text_value(
                "model_path_edit",
                self.config_manager.get_config("WAKE_WORD_OPTIONS.MODEL_PATH", ""),
            )

            # 从 keywords.txt 文件读取唤醒词
            wake_words_text = self._load_keywords_from_file()
            if self.ui_controls["wake_words_edit"]:
                self.ui_controls["wake_words_edit"].setPlainText(wake_words_text)

            # 摄像头配置
            camera_config = self.config_manager.get_config("CAMERA", {})
            self._set_spin_value(
                "camera_index_spin", camera_config.get("camera_index", 0)
            )
            self._set_spin_value(
                "frame_width_spin", camera_config.get("frame_width", 640)
            )
            self._set_spin_value(
                "frame_height_spin", camera_config.get("frame_height", 480)
            )
            self._set_spin_value("fps_spin", camera_config.get("fps", 30))
            self._set_text_value(
                "local_vl_url_edit", camera_config.get("Local_VL_url", "")
            )
            self._set_text_value("vl_api_key_edit", camera_config.get("VLapi_key", ""))
            self._set_text_value("models_edit", camera_config.get("models", ""))

        except Exception as e:
            self.logger.error(f"加载配置值失败: {e}", exc_info=True)

    def _set_text_value(self, control_name: str, value: str):
        """
        设置文本控件的值.
        """
        control = self.ui_controls.get(control_name)
        if control and hasattr(control, "setText"):
            control.setText(str(value) if value is not None else "")

    def _set_spin_value(self, control_name: str, value: int):
        """
        设置数字控件的值.
        """
        control = self.ui_controls.get(control_name)
        if control and hasattr(control, "setValue"):
            control.setValue(int(value) if value is not None else 0)

    def _get_text_value(self, control_name: str) -> str:
        """
        获取文本控件的值.
        """
        control = self.ui_controls.get(control_name)
        if control and hasattr(control, "text"):
            return control.text().strip()
        return ""

    def _get_spin_value(self, control_name: str) -> int:
        """
        获取数字控件的值.
        """
        control = self.ui_controls.get(control_name)
        if control and hasattr(control, "value"):
            return control.value()
        return 0

    def _on_save_clicked(self):
        """
        Événement clic sur le bouton Enregistrer.
        """
        try:
            # 收集所有配置数据
            success = self._save_all_config()

            if success:
                # 显示保存成功并提示重启
                reply = QMessageBox.question(
                    self,
                    "Configuration enregistrée",
                    "La configuration a été enregistrée !\n\nPour appliquer les modifications, il est recommandé de redémarrer le logiciel.\nVoulez-vous redémarrer maintenant ?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes,
                )

                if reply == QMessageBox.Yes:
                    self._restart_application()
                else:
                    self.accept()
            else:
                QMessageBox.warning(
                    self,
                    "Erreur",
                    "Échec de l'enregistrement de la configuration, vérifiez les valeurs saisies.",
                )

        except Exception as e:
            self.logger.error(f"Échec de l'enregistrement de la configuration : {e}", exc_info=True)
            QMessageBox.critical(
                self, "Erreur", f"Une erreur est survenue lors de l'enregistrement : {str(e)}"
            )

    def _save_all_config(self) -> bool:
        """
        Enregistre toutes les configurations.
        """
        try:
            # 系统选项 - 网络配置
            ota_url = self._get_text_value("ota_url_edit")
            if ota_url:
                self.config_manager.update_config(
                    "SYSTEM_OPTIONS.NETWORK.OTA_VERSION_URL", ota_url
                )

            websocket_url = self._get_text_value("websocket_url_edit")
            if websocket_url:
                self.config_manager.update_config(
                    "SYSTEM_OPTIONS.NETWORK.WEBSOCKET_URL", websocket_url
                )

            websocket_token = self._get_text_value("websocket_token_edit")
            if websocket_token:
                self.config_manager.update_config(
                    "SYSTEM_OPTIONS.NETWORK.WEBSOCKET_ACCESS_TOKEN", websocket_token
                )

            authorization_url = self._get_text_value("authorization_url_edit")
            if authorization_url:
                self.config_manager.update_config(
                    "SYSTEM_OPTIONS.NETWORK.AUTHORIZATION_URL", authorization_url
                )

            # 激活版本
            if self.ui_controls["activation_version_combo"]:
                activation_version = self.ui_controls[
                    "activation_version_combo"
                ].currentText()
                self.config_manager.update_config(
                    "SYSTEM_OPTIONS.NETWORK.ACTIVATION_VERSION", activation_version
                )

            # MQTT配置
            mqtt_config = {}
            mqtt_endpoint = self._get_text_value("mqtt_endpoint_edit")
            if mqtt_endpoint:
                mqtt_config["endpoint"] = mqtt_endpoint

            mqtt_client_id = self._get_text_value("mqtt_client_id_edit")
            if mqtt_client_id:
                mqtt_config["client_id"] = mqtt_client_id

            mqtt_username = self._get_text_value("mqtt_username_edit")
            if mqtt_username:
                mqtt_config["username"] = mqtt_username

            mqtt_password = self._get_text_value("mqtt_password_edit")
            if mqtt_password:
                mqtt_config["password"] = mqtt_password

            mqtt_publish_topic = self._get_text_value("mqtt_publish_topic_edit")
            if mqtt_publish_topic:
                mqtt_config["publish_topic"] = mqtt_publish_topic

            mqtt_subscribe_topic = self._get_text_value("mqtt_subscribe_topic_edit")
            if mqtt_subscribe_topic:
                mqtt_config["subscribe_topic"] = mqtt_subscribe_topic

            if mqtt_config:
                # 获取现有的MQTT配置并更新
                existing_mqtt = self.config_manager.get_config(
                    "SYSTEM_OPTIONS.NETWORK.MQTT_INFO", {}
                )
                existing_mqtt.update(mqtt_config)
                self.config_manager.update_config(
                    "SYSTEM_OPTIONS.NETWORK.MQTT_INFO", existing_mqtt
                )

            # 唤醒词配置
            if self.ui_controls["use_wake_word_check"]:
                use_wake_word = self.ui_controls["use_wake_word_check"].isChecked()
                self.config_manager.update_config(
                    "WAKE_WORD_OPTIONS.USE_WAKE_WORD", use_wake_word
                )

            model_path = self._get_text_value("model_path_edit")
            if model_path:
                self.config_manager.update_config(
                    "WAKE_WORD_OPTIONS.MODEL_PATH", model_path
                )

            # 保存唤醒词到 keywords.txt 文件
            if self.ui_controls["wake_words_edit"]:
                wake_words_text = (
                    self.ui_controls["wake_words_edit"].toPlainText().strip()
                )
                self._save_keywords_to_file(wake_words_text)

            # 摄像头配置
            camera_config = {}
            camera_config["camera_index"] = self._get_spin_value("camera_index_spin")
            camera_config["frame_width"] = self._get_spin_value("frame_width_spin")
            camera_config["frame_height"] = self._get_spin_value("frame_height_spin")
            camera_config["fps"] = self._get_spin_value("fps_spin")

            local_vl_url = self._get_text_value("local_vl_url_edit")
            if local_vl_url:
                camera_config["Local_VL_url"] = local_vl_url

            vl_api_key = self._get_text_value("vl_api_key_edit")
            if vl_api_key:
                camera_config["VLapi_key"] = vl_api_key

            models = self._get_text_value("models_edit")
            if models:
                camera_config["models"] = models

            # 获取现有的摄像头配置并更新
            existing_camera = self.config_manager.get_config("CAMERA", {})
            existing_camera.update(camera_config)
            self.config_manager.update_config("CAMERA", existing_camera)

            self.logger.info("Configuration enregistrée avec succès")
            return True

        except Exception as e:
            self.logger.error(
                f"Erreur lors de l'enregistrement de la configuration : {e}", exc_info=True
            )
            return False

    def _on_reset_clicked(self):
        """
        Événement clic sur le bouton Réinitialiser.
        """
        reply = QMessageBox.question(
            self,
            "Confirmer la réinitialisation",
            "Voulez-vous vraiment réinitialiser tous les paramètres par défaut ?\nCela effacera toutes les configurations actuelles.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self._reset_to_defaults()

    def _reset_to_defaults(self):
        """
        Rétablit les valeurs par défaut.
        """
        try:
            # 获取默认配置
            default_config = ConfigManager.DEFAULT_CONFIG

            # 系统选项
            self._set_text_value(
                "ota_url_edit",
                default_config["SYSTEM_OPTIONS"]["NETWORK"]["OTA_VERSION_URL"],
            )
            self._set_text_value("websocket_url_edit", "")
            self._set_text_value("websocket_token_edit", "")
            self._set_text_value(
                "authorization_url_edit",
                default_config["SYSTEM_OPTIONS"]["NETWORK"]["AUTHORIZATION_URL"],
            )

            if self.ui_controls["activation_version_combo"]:
                self.ui_controls["activation_version_combo"].setCurrentText(
                    default_config["SYSTEM_OPTIONS"]["NETWORK"]["ACTIVATION_VERSION"]
                )

            # 清空MQTT配置
            self._set_text_value("mqtt_endpoint_edit", "")
            self._set_text_value("mqtt_client_id_edit", "")
            self._set_text_value("mqtt_username_edit", "")
            self._set_text_value("mqtt_password_edit", "")
            self._set_text_value("mqtt_publish_topic_edit", "")
            self._set_text_value("mqtt_subscribe_topic_edit", "")

            # 唤醒词配置
            wake_word_config = default_config["WAKE_WORD_OPTIONS"]
            if self.ui_controls["use_wake_word_check"]:
                self.ui_controls["use_wake_word_check"].setChecked(
                    wake_word_config["USE_WAKE_WORD"]
                )

            self._set_text_value("model_path_edit", wake_word_config["MODEL_PATH"])

            if self.ui_controls["wake_words_edit"]:
                # 使用默认的关键词重置
                default_keywords = self._get_default_keywords()
                self.ui_controls["wake_words_edit"].setPlainText(default_keywords)

            # 摄像头配置
            camera_config = default_config["CAMERA"]
            self._set_spin_value("camera_index_spin", camera_config["camera_index"])
            self._set_spin_value("frame_width_spin", camera_config["frame_width"])
            self._set_spin_value("frame_height_spin", camera_config["frame_height"])
            self._set_spin_value("fps_spin", camera_config["fps"])
            self._set_text_value("local_vl_url_edit", camera_config["Local_VL_url"])
            self._set_text_value("vl_api_key_edit", camera_config["VLapi_key"])
            self._set_text_value("models_edit", camera_config["models"])

            self.logger.info("Configuration réinitialisée aux valeurs par défaut")

        except Exception as e:
            self.logger.error(f"Échec de la réinitialisation de la configuration : {e}", exc_info=True)
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de la réinitialisation : {str(e)}")

    def _on_model_path_browse(self):
        """
        Parcourt le chemin du modèle.
        """
        try:
            current_path = self._get_text_value("model_path_edit")
            if not current_path:
                # 使用resource_finder查找默认models目录
                models_dir = resource_finder.find_models_dir()
                if models_dir:
                    current_path = str(models_dir)
                else:
                    # 如果找不到，使用项目根目录下的models
                    project_root = resource_finder.get_project_root()
                    current_path = str(project_root / "models")

            selected_path = QFileDialog.getExistingDirectory(
                self, "Choisir le répertoire du modèle", current_path
            )

            if selected_path:
                self._set_text_value("model_path_edit", selected_path)
                self.logger.info(f"Chemin du modèle sélectionné : {selected_path}")

        except Exception as e:
            self.logger.error(f"Échec lors de la sélection du chemin du modèle : {e}", exc_info=True)
            QMessageBox.warning(self, "Erreur", f"Une erreur est survenue lors de la sélection du chemin du modèle : {str(e)}")

    def _restart_application(self):
        """
        Redémarre l'application.
        """
        try:
            self.logger.info("L'utilisateur a choisi de redémarrer l'application")

            # 关闭设置窗口
            self.accept()

            # 直接重启程序
            self._direct_restart()

        except Exception as e:
            self.logger.error(f"Échec du redémarrage de l'application : {e}", exc_info=True)
            QMessageBox.warning(
                self,
                "Échec du redémarrage",
                "Le redémarrage automatique a échoué, veuillez redémarrer le logiciel manuellement pour appliquer la configuration.",
            )

    def _direct_restart(self):
        """
        Redémarre le programme directement.
        """
        try:
            import os
            import sys

            # 获取当前执行的程序路径和参数
            python = sys.executable
            script = sys.argv[0]
            args = sys.argv[1:]

            self.logger.info(f"Commande de redémarrage : {python} {script} {' '.join(args)}")

            # 关闭当前应用
            from PyQt5.QtWidgets import QApplication

            QApplication.quit()

            # 启动新实例
            if getattr(sys, "frozen", False):
                # 打包环境
                os.execv(sys.executable, [sys.executable] + args)
            else:
                # 开发环境
                os.execv(python, [python, script] + args)

        except Exception as e:
            self.logger.error(f"Échec du redémarrage direct : {e}", exc_info=True)

    def _load_keywords_from_file(self) -> str:
        """
        Charge les mots de réveil depuis keywords.txt en conservant le format complet.
        """
        try:
            keywords_file = get_project_root() / "models" / "keywords.txt"
            if not keywords_file.exists():
                self.logger.warning(f"Fichier de mots-clés introuvable: {keywords_file}")
                return ""

            keywords = []
            with open(keywords_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and "@" in line and not line.startswith("#"):
                        # 保持完整格式: 拼音 @中文
                        keywords.append(line)

            return "\n".join(keywords)

        except Exception as e:
            self.logger.error(f"Échec de la lecture du fichier de mots-clés: {e}")
            return ""

    def _save_keywords_to_file(self, keywords_text: str):
        """
        Enregistre les mots de réveil dans keywords.txt en conservant le format complet.
        """
        try:
            keywords_file = get_project_root() / "models" / "keywords.txt"

            # 处理输入的关键词文本
            lines = [line.strip() for line in keywords_text.split("\n") if line.strip()]

            processed_lines = []
            has_invalid_lines = False

            for line in lines:
                if "@" in line:
                    # 完整格式：拼音 @中文
                    processed_lines.append(line)
                else:
                    # 只有中文，没有拼音 - 标记为无效
                    processed_lines.append(f"# Invalide : format pinyin manquant - {line}")
                    has_invalid_lines = True
                    self.logger.warning(
                        f"mot-clé '{line}' manque le pinyin, format requis : pinyin @chinois"
                    )

            # 写入文件
            with open(keywords_file, "w", encoding="utf-8") as f:
                f.write("\n".join(processed_lines) + "\n")

            self.logger.info(f"Mots-clés enregistrés dans {keywords_file}")

            # Si des formats invalides sont détectés, avertir l'utilisateur
            if has_invalid_lines:
                QMessageBox.warning(
                    self,
                    "Format incorrect",
                    "Format de mot-clé invalide détecté !\n\n"
                    "Format correct : pinyin @chinois\n"
                    "Exemple : x iǎo ài t óng x ué @小爱同学\n\n"
                    "Les lignes invalides ont été commentées, veuillez corriger manuellement puis sauvegarder à nouveau.",
                )

        except Exception as e:
            self.logger.error(f"Échec de l'enregistrement du fichier de mots-clés : {e}")
            QMessageBox.warning(self, "Erreur", f"Échec de l'enregistrement des mots-clés : {str(e)}")

    def _get_default_keywords(self) -> str:
        """
        Obtient la liste par défaut des mots de réveil, format complet.
        """
        default_keywords = [
            "x iǎo ài t óng x ué @小爱同学",
            "n ǐ h ǎo w èn w èn @你好问问",
            "x iǎo y ì x iǎo y ì @小艺小艺",
            "x iǎo m ǐ x iǎo m ǐ @小米小米",
            "n ǐ h ǎo x iǎo zh ì @你好小智",
            "j iā w éi s ī @贾维斯",
        ]
        return "\n".join(default_keywords)

    def closeEvent(self, event):
        """
        Événement de fermeture de la fenêtre.
        """
        self.logger.debug("Fenêtre de paramètres fermée")
        super().closeEvent(event)
