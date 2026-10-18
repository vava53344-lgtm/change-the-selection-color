import sys
import os
import ctypes
import winreg
import subprocess

from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QColorDialog,
    QLabel,
    QFrame,
)

from qfluentwidgets import (
    MSFluentWindow,
    FluentIcon,
    setTheme,
    Theme,
    PushButton,
    PrimaryPushButton,
    ComboBox,
    LineEdit,
    SubtitleLabel,
    BodyLabel,
    CardWidget,
    InfoBar,
    InfoBarPosition,
    MessageBox,
    ColorDialog,
)


REG_PATH = r"Control Panel\Colors"

SYSTEM_IDS = {
    "Highlight": 13,
    "HighlightText": 14,
    "HotTrackingColor": 26,
}

FACTORY_COLORS = {
    "Highlight": "0 120 215",
    "HighlightText": "255 255 255",
    "HotTrackingColor": "0 102 204",
}

# ---------------------------------------------------------------------------
# Локализация
# ---------------------------------------------------------------------------

TRANSLATIONS = {
    "ru": {
        "Highlight_title": "Цвет барьера",
        "Highlight_desc": "Цвет под выделенным текстом и барьер выделения",
        "HighlightText_title": "Текст выделения",
        "HighlightText_desc": "Цвет букв внутри выделения",
        "HotTrackingColor_title": "Цвет фона выделения",
        "HotTrackingColor_desc": "Цвет ссылок и элементов при наведении",
        "rgb_placeholder": "Например: 0 120 215",
        "pick_button": "Выбрать",
        "choose_color_title": "Выберите цвет",
        "colors_heading": "Системные цвета",
        "colors_description": "Настрой цвета выделения текста и наведения курсора.",
        "preview_title": "Предпросмотр",
        "preview_text": "Пример выделенного текста",
        "status_ready": "Готово к настройке.",
        "apply_button": "Применить",
        "reset_button": "Сбросить до заводских",
        "reload_button": "Загрузить из Windows",
        "restart_button": "Перезапустить Explorer",
        "status_loaded": "Цвета загружены из реестра Windows.",
        "status_applied": "Цвета сохранены и переданы Windows.",
        "status_reset": "Цвета сброшены к заданным значениям.",
        "status_restart_sent": "Команда перезапуска Explorer отправлена.",
        "done_title": "Готово",
        "done_content": (
            "Цвета сохранены. Некоторые приложения "
            "могут потребовать перезапуска."
        ),
        "reset_done_title": "Сброс выполнен",
        "reset_done_content": "Стандартные цвета сохранены и переданы Windows.",
        "reset_dialog_title": "Сброс цветов",
        "reset_dialog_content": (
            "Вернуть стандартные значения цветов?\n\n"
            "Фон выделения: 0 120 215\n"
            "Текст выделения: 255 255 255\n"
            "Цвет наведения: 0 102 204\n\n"
            "Текущие значения будут заменены."
        ),
        "restart_dialog_title": "Перезапуск Explorer",
        "restart_dialog_content": (
            "Перезапустить проводник Windows? Панель задач "
            "может на короткое время исчезнуть."
        ),
        "error_load_title": "Ошибка загрузки",
        "error_apply_title": "Ошибка применения",
        "error_reset_title": "Ошибка сброса",
        "error_restart_title": "Ошибка перезапуска",
        "settings_title": "Настройки",
        "settings_theme_desc": "Выбери тему оформления приложения.",
        "settings_theme_label": "Тема приложения",
        "theme_system": "Системная",
        "theme_light": "Светлая",
        "theme_dark": "Тёмная",
        "settings_lang_label": "Язык приложения",
        "lang_system": "Системный",
        "lang_ru": "Русский",
        "lang_en": "English",
        "about_title": "О программе",
        "about_line1": "Настройка системных цветов Windows.",
        "about_line2": (
            "Изменения зависят от версии Windows и приложения. "
            "Некоторые современные элементы интерфейса могут "
            "не использовать системные цвета."
        ),
        "nav_colors": "Цвета",
        "nav_settings": "Настройки",
        "nav_about": "О прог...",
        "window_title": "Настройка системных цветов",
        "err_three_numbers": "Введите три числа RGB через пробел.",
        "err_integers": "RGB должен содержать только целые числа.",
        "err_range": "Значения RGB должны быть от 0 до 255.",
    },
    "en": {
        "Highlight_title": "Highlight color",
        "Highlight_desc": "Color behind selected text and selection highlight",
        "HighlightText_title": "Highlight text",
        "HighlightText_desc": "Color of letters inside selection",
        "HotTrackingColor_title": "Hot tracking color",
        "HotTrackingColor_desc": "Color of links and hovered items",
        "rgb_placeholder": "e.g. 0 120 215",
        "pick_button": "Pick",
        "choose_color_title": "Choose color",
        "colors_heading": "System colors",
        "colors_description": "Configure text selection and hover colors.",
        "preview_title": "Preview",
        "preview_text": "Sample selected text",
        "status_ready": "Ready to configure.",
        "apply_button": "Apply",
        "reset_button": "Reset to defaults",
        "reload_button": "Load from Windows",
        "restart_button": "Restart Explorer",
        "status_loaded": "Colors loaded from Windows registry.",
        "status_applied": "Colors saved and sent to Windows.",
        "status_reset": "Colors reset to defaults.",
        "status_restart_sent": "Explorer restart command sent.",
        "done_title": "Done",
        "done_content": "Colors saved. Some applications may need a restart.",
        "reset_done_title": "Reset complete",
        "reset_done_content": "Default colors saved and sent to Windows.",
        "reset_dialog_title": "Reset colors",
        "reset_dialog_content": (
            "Restore default color values?\n\n"
            "Highlight background: 0 120 215\n"
            "Highlight text: 255 255 255\n"
            "Hot tracking: 0 102 204\n\n"
            "Current values will be replaced."
        ),
        "restart_dialog_title": "Restart Explorer",
        "restart_dialog_content": (
            "Restart Windows Explorer? The taskbar "
            "may disappear briefly."
        ),
        "error_load_title": "Load error",
        "error_apply_title": "Apply error",
        "error_reset_title": "Reset error",
        "error_restart_title": "Restart error",
        "settings_title": "Settings",
        "settings_theme_desc": "Choose the application theme.",
        "settings_theme_label": "Application theme",
        "theme_system": "System",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "settings_lang_label": "Application language",
        "lang_system": "System",
        "lang_ru": "Русский",
        "lang_en": "English",
        "about_title": "About",
        "about_line1": "Configure Windows system colors.",
        "about_line2": (
            "Changes depend on Windows version and application. "
            "Some modern UI elements may ignore system colors."
        ),
        "nav_colors": "Colors",
        "nav_settings": "Settings",
        "nav_about": "About",
        "window_title": "System color settings",
        "err_three_numbers": "Enter three RGB numbers separated by spaces.",
        "err_integers": "RGB must contain integers only.",
        "err_range": "RGB values must be between 0 and 255.",
    },
}


def system_language():
    """Возвращает 'ru' если системный язык русский, иначе 'en'."""
    name = QLocale.system().name()  # например "ru_RU" или "en_US"
    if name.lower().startswith("ru"):
        return "ru"
    return "en"


class Locale:
    def __init__(self):
        self.lang = system_language()
        self.manual_lang = None  # None = системный

    def set_language(self, lang):
        self.lang = lang

    def __call__(self, key):
        table = TRANSLATIONS.get(self.lang, TRANSLATIONS["en"])
        return table.get(key, TRANSLATIONS["en"].get(key, key))


tr = Locale()


# ---------------------------------------------------------------------------
# Работа с реестром и WinAPI
# ---------------------------------------------------------------------------

def parse_rgb(value):
    parts = value.strip().split()

    if len(parts) != 3:
        raise ValueError(tr("err_three_numbers"))

    try:
        rgb = tuple(int(part) for part in parts)
    except ValueError:
        raise ValueError(tr("err_integers"))

    if any(component < 0 or component > 255 for component in rgb):
        raise ValueError(tr("err_range"))

    return rgb


def rgb_hex(value):
    r, g, b = parse_rgb(value)
    return QColor(r, g, b).name()


def read_colors():
    colors = {}

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        REG_PATH,
        0,
        winreg.KEY_READ,
    ) as key:
        for name, default in (
            ("Highlight", FACTORY_COLORS["Highlight"]),
            ("HighlightText", FACTORY_COLORS["HighlightText"]),
            ("HotTrackingColor", FACTORY_COLORS["HotTrackingColor"]),
        ):
            try:
                value, _ = winreg.QueryValueEx(key, name)
                parse_rgb(value)
                colors[name] = value
            except (OSError, ValueError):
                colors[name] = default

    return colors


def save_colors(colors):
    with winreg.CreateKeyEx(
        winreg.HKEY_CURRENT_USER,
        REG_PATH,
        0,
        winreg.KEY_SET_VALUE,
    ) as key:
        for name in colors:
            value = colors[name]
            parse_rgb(value)

            winreg.SetValueEx(
                key,
                name,
                0,
                winreg.REG_SZ,
                value,
            )


def apply_system_colors(colors):
    names = list(colors.keys())
    count = len(names)

    indices = (ctypes.c_int * count)(
        *(SYSTEM_IDS[name] for name in names)
    )

    colorrefs = []

    for name in names:
        r, g, b = parse_rgb(colors[name])
        colorrefs.append(r | (g << 8) | (b << 16))

    values = (ctypes.c_uint * count)(*colorrefs)

    user32 = ctypes.WinDLL("user32", use_last_error=True)

    user32.SetSysColors.argtypes = [
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_uint),
    ]
    user32.SetSysColors.restype = ctypes.c_bool

    if not user32.SetSysColors(count, indices, values):
        raise ctypes.WinError(ctypes.get_last_error())

    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002

    result = ctypes.c_size_t()

    user32.SendMessageTimeoutW(
        HWND_BROADCAST,
        WM_SETTINGCHANGE,
        0,
        "Colors",
        SMTO_ABORTIFHUNG,
        2000,
        ctypes.byref(result),
    )


def restart_explorer():
    subprocess.run(
        ["taskkill", "/f", "/im", "explorer.exe"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )

    subprocess.Popen(["explorer.exe"])


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

class ColorCard(CardWidget):
    def __init__(self, key, parent=None):
        super().__init__(parent)

        self.key = key
        self.default = FACTORY_COLORS[key]

        self.setBorderRadius(12)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        self.title_label = SubtitleLabel("", self)
        self.description_label = BodyLabel("", self)
        self.description_label.setWordWrap(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)

        self.rgb_input = LineEdit(self)
        self.rgb_input.setPlaceholderText(tr("rgb_placeholder"))

        self.color_preview = QFrame(self)
        self.color_preview.setFixedSize(38, 38)
        self.color_preview.setStyleSheet(
            "border-radius: 8px; border: 1px solid #888;"
        )

        self.pick_button = PushButton(
            tr("pick_button"),
            self,
            FluentIcon.PALETTE,
        )
        self.pick_button.clicked.connect(self.choose_color)

        input_layout.addWidget(self.rgb_input, 1)
        input_layout.addWidget(self.color_preview)
        input_layout.addWidget(self.pick_button)

        layout.addLayout(input_layout)

        self.rgb_input.textChanged.connect(self.update_preview)
        self.set_color_text(self.default)

        self.retranslate()

    def retranslate(self):
        self.title_label.setText(tr(f"{self.key}_title"))
        self.description_label.setText(tr(f"{self.key}_desc"))
        self.rgb_input.setPlaceholderText(tr("rgb_placeholder"))
        self.pick_button.setText(tr("pick_button"))

    def set_color_text(self, value):
        self.rgb_input.setText(value)
        self.update_preview()

    def get_color_text(self):
        value = self.rgb_input.text().strip()
        parse_rgb(value)
        return value

    def update_preview(self):
        try:
            color = rgb_hex(self.rgb_input.text())
            self.color_preview.setStyleSheet(
                f"background-color: {color};"
                "border-radius: 8px;"
                "border: 1px solid #888;"
            )
        except ValueError:
            self.color_preview.setStyleSheet(
                "background-color: transparent;"
                "border-radius: 8px;"
                "border: 1px solid #888;"
            )

    def choose_color(self):
        try:
            current = parse_rgb(self.rgb_input.text())
            initial = QColor(*current)
        except ValueError:
            initial = QColor(*parse_rgb(self.default))

        try:
            dialog = ColorDialog(
                initial,
                tr("choose_color_title"),
                self.window(),
            )

            if dialog.exec():
                color = None

                if hasattr(dialog, "color"):
                    candidate = dialog.color
                    color = candidate() if callable(candidate) else candidate
                elif hasattr(dialog, "getColor"):
                    candidate = dialog.getColor
                    color = candidate() if callable(candidate) else candidate

                if isinstance(color, QColor) and color.isValid():
                    self.set_color(color)
                else:
                    self.fallback_color_dialog(initial)

        except (AttributeError, TypeError):
            self.fallback_color_dialog(initial)

    def fallback_color_dialog(self, initial):
        color = QColorDialog.getColor(
            initial,
            self.window(),
            tr("choose_color_title"),
        )

        if color.isValid():
            self.set_color(color)

    def set_color(self, color):
        self.set_color_text(
            f"{color.red()} {color.green()} {color.blue()}"
        )


class ColorsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("ColorsPage")

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(18)

        self.heading = SubtitleLabel("", self)
        self.description = BodyLabel("", self)
        self.description.setWordWrap(True)

        root.addWidget(self.heading)
        root.addWidget(self.description)

        self.cards_layout = QGridLayout()
        self.cards_layout.setSpacing(14)

        self.cards = {}

        for index, key in enumerate(SYSTEM_IDS):
            card = ColorCard(key, self)
            self.cards[key] = card
            self.cards_layout.addWidget(card, index, 0)

        root.addLayout(self.cards_layout)

        self.preview_card = CardWidget(self)
        self.preview_card.setBorderRadius(12)

        preview_layout = QVBoxLayout(self.preview_card)
        preview_layout.setContentsMargins(18, 16, 18, 16)
        preview_layout.setSpacing(10)

        self.preview_title = SubtitleLabel("", self.preview_card)
        preview_layout.addWidget(self.preview_title)

        self.preview_label = QLabel("", self.preview_card)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(60)

        preview_layout.addWidget(self.preview_label)
        root.addWidget(self.preview_card)

        self.status = BodyLabel("", self)
        root.addWidget(self.status)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)

        self.apply_button = PrimaryPushButton(
            tr("apply_button"),
            self,
            FluentIcon.ACCEPT,
        )
        self.apply_button.clicked.connect(self.apply_colors)

        reset_icon = getattr(FluentIcon, "BROOM", FluentIcon.UPDATE)
        self.reset_button = PushButton(
            tr("reset_button"),
            self,
            reset_icon,
        )
        self.reset_button.clicked.connect(self.reset_factory)

        self.reload_button = PushButton(
            tr("reload_button"),
            self,
            FluentIcon.SYNC,
        )
        self.reload_button.clicked.connect(self.load)

        self.restart_button = PushButton(
            tr("restart_button"),
            self,
            FluentIcon.POWER_BUTTON,
        )
        self.restart_button.clicked.connect(self.restart_shell)

        buttons.addWidget(self.apply_button)
        buttons.addWidget(self.reset_button)
        buttons.addWidget(self.reload_button)
        buttons.addWidget(self.restart_button)

        root.addLayout(buttons)
        root.addStretch(1)

        for card in self.cards.values():
            card.rgb_input.textChanged.connect(self.update_preview)

        self.retranslate()
        self.load()

    def retranslate(self):
        self.heading.setText(tr("colors_heading"))
        self.description.setText(tr("colors_description"))
        self.preview_title.setText(tr("preview_title"))
        self.preview_label.setText(tr("preview_text"))
        self.status.setText(tr("status_ready"))
        self.apply_button.setText(tr("apply_button"))
        self.reset_button.setText(tr("reset_button"))
        self.reload_button.setText(tr("reload_button"))
        self.restart_button.setText(tr("restart_button"))

        for card in self.cards.values():
            card.retranslate()

    def collect_colors(self):
        colors = {}

        for key, card in self.cards.items():
            colors[key] = card.get_color_text()

        return colors

    def update_preview(self):
        try:
            colors = self.collect_colors()
            background = rgb_hex(colors["Highlight"])
            foreground = rgb_hex(colors["HighlightText"])

            self.preview_label.setStyleSheet(
                f"background-color: {background};"
                f"color: {foreground};"
                "border-radius: 8px;"
                "padding: 12px;"
            )
        except ValueError:
            self.preview_label.setStyleSheet(
                "border-radius: 8px; padding: 12px;"
            )

    def load(self):
        try:
            colors = read_colors()

            for key, value in colors.items():
                self.cards[key].set_color_text(value)

            self.update_preview()
            self.status.setText(tr("status_loaded"))

        except OSError as error:
            self.show_error(tr("error_load_title"), str(error))

    def apply_colors(self):
        try:
            colors = self.collect_colors()
            save_colors(colors)
            apply_system_colors(colors)

            self.status.setText(tr("status_applied"))

            InfoBar.success(
                title=tr("done_title"),
                content=tr("done_content"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3500,
                parent=self.window(),
            )

        except (ValueError, OSError, RuntimeError) as error:
            self.show_error(tr("error_apply_title"), str(error))

    def reset_factory(self):
        dialog = MessageBox(
            tr("reset_dialog_title"),
            tr("reset_dialog_content"),
            self.window(),
        )

        if not dialog.exec():
            return

        try:
            save_colors(FACTORY_COLORS)
            apply_system_colors(FACTORY_COLORS)

            for key, value in FACTORY_COLORS.items():
                self.cards[key].set_color_text(value)

            self.update_preview()
            self.status.setText(tr("status_reset"))

            InfoBar.success(
                title=tr("reset_done_title"),
                content=tr("reset_done_content"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3500,
                parent=self.window(),
            )

        except (ValueError, OSError, RuntimeError) as error:
            self.show_error(tr("error_reset_title"), str(error))

    def restart_shell(self):
        dialog = MessageBox(
            tr("restart_dialog_title"),
            tr("restart_dialog_content"),
            self.window(),
        )

        if not dialog.exec():
            return

        try:
            restart_explorer()
            self.status.setText(tr("status_restart_sent"))
        except OSError as error:
            self.show_error(tr("error_restart_title"), str(error))

    def show_error(self, title, message):
        InfoBar.error(
            title=title,
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=6000,
            parent=self.window(),
        )


class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("SettingsPage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        self.title_label = SubtitleLabel("", self)
        self.theme_desc = BodyLabel("", self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.theme_desc)

        self.theme_combo = ComboBox(self)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)

        self.theme_label = BodyLabel("", self)
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combo)

        self.lang_label = BodyLabel("", self)
        layout.addWidget(self.lang_label)

        self.lang_combo = ComboBox(self)
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        layout.addWidget(self.lang_combo)

        layout.addStretch(1)

        self.retranslate()

    def retranslate(self):
        self.title_label.setText(tr("settings_title"))
        self.theme_desc.setText(tr("settings_theme_desc"))
        self.theme_label.setText(tr("settings_theme_label"))
        self.lang_label.setText(tr("settings_lang_label"))

        current_theme = self.theme_combo.currentIndex()
        self.theme_combo.blockSignals(True)
        self.theme_combo.clear()
        self.theme_combo.addItems([
            tr("theme_system"),
            tr("theme_light"),
            tr("theme_dark"),
        ])
        self.theme_combo.setCurrentIndex(max(0, current_theme))
        self.theme_combo.blockSignals(False)

        self.lang_combo.blockSignals(True)
        self.lang_combo.clear()
        self.lang_combo.addItems([
            tr("lang_system"),
            tr("lang_ru"),
            tr("lang_en"),
        ])
        if getattr(tr, "manual_lang", None) == "ru":
            self.lang_combo.setCurrentIndex(1)
        elif getattr(tr, "manual_lang", None) == "en":
            self.lang_combo.setCurrentIndex(2)
        else:
            self.lang_combo.setCurrentIndex(0)
        self.lang_combo.blockSignals(False)

    def change_theme(self, index):
        if index == 0:
            setTheme(Theme.AUTO)
        elif index == 1:
            setTheme(Theme.LIGHT)
        else:
            setTheme(Theme.DARK)

    def change_language(self, index):
        if index == 0:
            tr.manual_lang = None
            tr.set_language(system_language())
        elif index == 1:
            tr.manual_lang = "ru"
            tr.set_language("ru")
        else:
            tr.manual_lang = "en"
            tr.set_language("en")

        window = self.window()
        if hasattr(window, "retranslate_all"):
            window.retranslate_all()


class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("AboutPage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(12)

        self.title_label = SubtitleLabel("", self)
        self.line1 = BodyLabel("", self)
        self.line2 = BodyLabel("", self)
        self.line2.setWordWrap(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.line1)
        layout.addWidget(self.line2)
        layout.addStretch(1)

        self.retranslate()

    def retranslate(self):
        self.title_label.setText(tr("about_title"))
        self.line1.setText(tr("about_line1"))
        self.line2.setText(tr("about_line2"))


class AppWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()

        icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "icon.png",
        )

        if os.path.isfile(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setWindowTitle(tr("window_title"))
        self.resize(950, 800)

        self.colors_page = ColorsPage(self)
        self.settings_page = SettingsPage(self)
        self.about_page = AboutPage(self)

        self.nav_colors = self.addSubInterface(
            self.colors_page,
            FluentIcon.PALETTE,
            tr("nav_colors"),
        )
        self.nav_settings = self.addSubInterface(
            self.settings_page,
            FluentIcon.SETTING,
            tr("nav_settings"),
        )
        self.nav_about = self.addSubInterface(
            self.about_page,
            FluentIcon.INFO,
            tr("nav_about"),
        )

        # Пытаемся сохранить ссылки на элементы навигации для обновления текста
        self._nav_items = {}
        try:
            for item in self.navigationInterface.panel.items():
                obj_name = getattr(item, "objectName", lambda: "")()
                self._nav_items[obj_name] = item
        except Exception:
            pass

    def retranslate_all(self):
        self.setWindowTitle(tr("window_title"))

        self.colors_page.retranslate()
        self.settings_page.retranslate()
        self.about_page.retranslate()

        self._set_nav_text(self.nav_colors, tr("nav_colors"))
        self._set_nav_text(self.nav_settings, tr("nav_settings"))
        self._set_nav_text(self.nav_about, tr("nav_about"))

        mapping = {
            "ColorsPage": tr("nav_colors"),
            "SettingsPage": tr("nav_settings"),
            "AboutPage": tr("nav_about"),
        }
        for obj_name, text in mapping.items():
            item = self._nav_items.get(obj_name)
            if item is not None:
                self._set_nav_text(item, text)

    @staticmethod
    def _set_nav_text(item, text):
        if item is None:
            return
        for attr in ("setText",):
            if hasattr(item, attr):
                try:
                    getattr(item, attr)(text)
                    return
                except Exception:
                    pass
        if hasattr(item, "text"):
            try:
                if callable(item.text):
                    item.text = text
                else:
                    item.text = text
                return
            except Exception:
                pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Всегда стартуем с системным языком
    tr.manual_lang = None
    tr.set_language(system_language())

    setTheme(Theme.AUTO)

    window = AppWindow()
    window.show()

    sys.exit(app.exec_())
