import random
import sys
try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
        QHBoxLayout, QFrame, QScrollArea, QFileDialog, QGraphicsDropShadowEffect
    )
    from PyQt5.QtGui import QFont, QGuiApplication, QColor
    from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer, QSequentialAnimationGroup, QObject, pyqtProperty
    from PyQt5.QtGui import QPainter, QLinearGradient, QPalette, QBrush, QPen
except ImportError:
    print("Ошибка: PyQt5 не установлен. Установите его командой:")
    print("pip install PyQt5")
    sys.exit(1)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import os


races = {
    "Human": {"traits": ["Versatility"], "weapon": "Longsword"},
    "Elf": {"traits": ["Keen Senses", "Fey Ancestry"], "weapon": "Longbow"},
    "Dwarf": {"traits": ["Darkvision", "Dwarven Resilience"], "weapon": "Warhammer"},

}

classes = {
    "Barbarian": {"abilities": ["Rage", "Unarmored Defense"]},
    "Bard": {"abilities": ["Bardic Inspiration", "Spellcasting"]},
    "Cleric": {"abilities": ["Divine Domain", "Turn Undead"]},

}

backgrounds = ["Acolyte", "Criminal", "Folk Hero", "Noble", "Sage", "Soldier"]

alignments = ["Lawful Good", "Neutral Good", "Chaotic Good", "Lawful Neutral", "True Neutral", "Chaotic Neutral", "Lawful Evil", "Neutral Evil", "Chaotic Evil"]

names_male = ["Arin", "Thorin", "Balin", "Elric", "Gorin", "Vladimir", "Ragnar", "Leoric", "Boris", "Felix"]
names_female = ["Aria", "Lyra", "Mira", "Elara", "Nora", "Sasha", "Anya", "Yara", "Freya", "Kira"]

spells = {
    "Bard": {
        "Cantrips": ["Злая насмешка", "Свет", "Фокусы", "Пляшущие огоньки"],
        "Level 1": ["Лечащее слово", "Очарование личности", "Гром", "Сон"]
    },
    "Cleric": {
        "Cantrips": ["Свет", "Священное пламя", "Указание", "Сопротивление"],
        "Level 1": ["Лечащее слово", "Благословение", "Щит веры", "Нанесение ран"]
    },
    "Druid": {
        "Cantrips": ["Искусство друдов", "Сотворение пламени", "Шипы"],
        "Level 1": ["Разговор с животными", "Опутывание", "Лечащее слово"]
    },
    "Sorcerer": {
        "Cantrips": ["Огненный снаряд", "Свет", "Малая иллюзия"],
        "Level 1": ["Щит", "Магическая стрела", "Обнаружение магии"]
    },
    "Warlock": {
        "Cantrips": ["Мистический заряд", "Малая иллюзия", "Ядовитые брызги"],
        "Level 1": ["Ведьмин снаряд", "Доспехи Агатиса", "Очарование личности"]
    },
    "Wizard": {
        "Cantrips": ["Огненный снаряд", "Волшебная рука", "Свет"],
        "Level 1": ["Щит", "Магическая стрела", "Обнаружение магии"]
    }
}

spellcasting_classes = ["Bard", "Cleric", "Druid", "Sorcerer", "Warlock", "Wizard"]

def generate_spells(character_class):
    """Генерирует случайный набор заклинаний для класса"""
    if character_class not in spells:
        return None
    
    available_spells = spells[character_class]
    return {
        "Cantrips": random.sample(available_spells["Cantrips"], min(2, len(available_spells["Cantrips"]))),
        "Level 1": random.sample(available_spells["Level 1"], min(2, len(available_spells["Level 1"])))
    }


def generate_attributes():
    attributes = {}
    for attr in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
        rolls = sorted([random.randint(1, 6) for _ in range(4)], reverse=True)
        attributes[attr] = sum(rolls[:3])
    return attributes


def generate_name_and_gender():
    gender = random.choice(["Male", "Female"])
    name = random.choice(names_male if gender == "Male" else names_female)
    return name, gender


def generate_character():
    name, gender = generate_name_and_gender()
    race = random.choice(list(races.keys()))
    char_class = random.choice(list(classes.keys()))

    character = {
        "Name": name,
        "Gender": gender,
        "Race": race,
        "Class": char_class,
        "Background": random.choice(backgrounds),
        "Alignment": random.choice(alignments),
        "Traits": ", ".join(races[race]["traits"]),
        "Weapon": races[race]["weapon"],
        "Abilities": ", ".join(classes[char_class]["abilities"]),
        "Attributes": generate_attributes()
    }
    if char_class in spellcasting_classes:
        spells_list = generate_spells(char_class)
        if spells_list:
            character['spells'] = spells_list

    return character

def get_font_path():
    """Ищет шрифт в разных возможных местах"""
    possible_paths = [
        os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf'),
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Arial.ttf"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

font_path = get_font_path()
if font_path:
    try:
        pdfmetrics.registerFont(TTFont('MainFont', font_path))
    except Exception as e:
        print(f"Ошибка при регистрации шрифта: {str(e)}")


class AnimatedButton(QPushButton):
    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.base_color = color
        self.animation = QPropertyAnimation(self, b"pos")
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                border-radius: 10px;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                transition: all 0.3s;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }}
        """)

    def enterEvent(self, event):
        animation = QPropertyAnimation(self, b"pos")
        animation.setDuration(100)
        animation.setEndValue(QPoint(self.x(), self.y() - 5))
        animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        animation = QPropertyAnimation(self, b"pos")
        animation.setDuration(100)
        animation.setEndValue(QPoint(self.x(), self.y() + 5))
        animation.start()
        super().leaveEvent(event)

    @staticmethod
    def darken_color(hex_color, factor=120):
        color = QColor(hex_color)
        darker = color.darker(factor)
        return darker.name()

class GlowingLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._glow = 0.0

    @pyqtProperty(float)
    def glow(self):
        return self._glow

    @glow.setter
    def glow(self, value):
        self._glow = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#2C3E50"))
        gradient.setColorAt(1, QColor("#3498DB"))
        painter.fillRect(self.rect(), gradient)

        if self._glow > 0:
            painter.setPen(QPen(QColor(52, 152, 219, 50), self._glow))
            painter.drawText(self.rect(), Qt.AlignCenter, self.text())
        
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

class OpacityEffect(QObject):
    def __init__(self, widget):
        super().__init__(widget)
        self._opacity = 1.0
        self.widget = widget

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.widget.setStyleSheet(f"background-color: rgba(52, 73, 94, {value})")

class GlitchEffect(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.text = text
        self.glitch_offset = 0
        self.glitch_alpha = 0
        self.glitch_timer = QTimer(self)
        self.glitch_timer.timeout.connect(self.update_glitch)
        self.glitch_timer.start(100)
        self.setStyleSheet("""
            QLabel {
                color: #00ff9f;
                font-family: 'Segoe UI';
                font-weight: 800;
                letter-spacing: 4px;
                text-transform: uppercase;
            }
        """)

    def update_glitch(self):
        if random.random() < 0.05:
            self.glitch_offset = random.randint(-1, 1)
            self.glitch_alpha = random.randint(50, 100)
        else:
            self.glitch_offset = 0
            self.glitch_alpha = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#00ff9f"))
        gradient.setColorAt(0.5, QColor("#00ffff"))
        gradient.setColorAt(1, QColor("#00ff9f"))
        
        painter.setPen(QPen(QColor(0, 255, 159, 30), 8))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text)
        
        painter.setPen(QPen(QColor(0, 255, 159, 50), 4))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text)
        
        painter.setPen(QColor(0, 255, 159))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text)

        if self.glitch_offset:
            painter.setPen(QColor(255, 50, 50, self.glitch_alpha))
            rect = self.rect()
            rect.translate(self.glitch_offset, 0)
            painter.drawText(rect, Qt.AlignCenter, self.text)
            painter.setPen(QColor(50, 50, 255, self.glitch_alpha))
            rect = self.rect()
            rect.translate(-self.glitch_offset, 0)
            painter.drawText(rect, Qt.AlignCenter, self.text)

class ModernButton(QPushButton):
    def __init__(self, text, color_start, color_end, parent=None):
        super().__init__(text, parent)
        self.color_start = color_start
        self.color_end = color_end
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {color_start}, stop:1 {color_end});
                border: none;
                border-radius: 25px;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {color_end}, stop:1 {color_start});
            }}
        """)

    def enterEvent(self, event):
        animation = QPropertyAnimation(self.shadow, b"blurRadius")
        animation.setDuration(200)
        animation.setStartValue(15)
        animation.setEndValue(25)
        animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        animation = QPropertyAnimation(self.shadow, b"blurRadius")
        animation.setDuration(200)
        animation.setStartValue(25)
        animation.setEndValue(15)
        animation.start()
        super().leaveEvent(event)

class CharacterGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.character_info = None
        self.initUI()
        self.start_background_animation()

    def initUI(self):
        self.setWindowTitle("D&D - Генератор Персонажей")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("""
            QMainWindow {
                background: #0a0a0a;
            }
            QWidget {
                color: #ffffff;
            }
            QScrollArea {
                background: transparent;
                border: 2px solid rgba(0, 255, 159, 0.1);
                border-radius: 15px;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollArea > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(0, 255, 159, 0.05);
                width: 10px;
                margin: 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ff9f, stop:1 #00ffcc);
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                border: none;
                background: none;
                height: 0px;
            }
        """)

        # Главный виджет и layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setSpacing(30)
        self.layout.setContentsMargins(40, 40, 40, 40)

        self.title_label = GlitchEffect("ГЕНЕРАТОР ПЕРСОНАЖЕЙ D&D")
        self.title_label.setFont(QFont("Segoe UI", 32, QFont.Bold))
        self.title_label.setFixedHeight(100)
        self.layout.addWidget(self.title_label)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.character_widget = QWidget()
        self.character_layout = QVBoxLayout(self.character_widget)
        
        self.character_label = QLabel("", self)
        self.character_label.setFont(QFont("Segoe UI", 12))
        self.character_label.setWordWrap(True)
        self.character_label.setStyleSheet("""
            QLabel {
                background: rgba(0, 255, 159, 0.05);
                border: 1px solid rgba(0, 255, 159, 0.1);
                border-radius: 15px;
                padding: 25px;
                line-height: 1.6;
                color: #e0e0e0;
                font-family: 'Segoe UI';
                letter-spacing: 1px;
            }
        """)
        
        self.character_layout.addWidget(self.character_label)
        self.scroll_area.setWidget(self.character_widget)
        self.layout.addWidget(self.scroll_area)

        self.button_container = QWidget()
        self.button_layout = QHBoxLayout(self.button_container)
        self.button_layout.setSpacing(20)
        
        buttons_data = [
            ("СОЗДАТЬ ПЕРСОНАЖА", "#00ff9f", "#00ffcc", self.display_character),
            ("КОПИРОВАТЬ", "#00ffcc", "#00ff9f", self.copy_to_clipboard),
            ("СОХРАНИТЬ PDF", "#00ff9f", "#00ffdd", self.save_to_pdf)
        ]
        
        for text, color_start, color_end, func in buttons_data:
            btn = ModernButton(text, color_start, color_end)
            btn.clicked.connect(func)
            self.button_layout.addWidget(btn)

        self.layout.addWidget(self.button_container)

    def start_background_animation(self):
        self.background_timer = QTimer(self)
        self.background_timer.timeout.connect(self.update_background)
        self.background_timer.start(50)
        self.background_offset = 0

    def update_background(self):
        self.background_offset = (self.background_offset + 1) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(10, 12, 16))
        gradient.setColorAt(0.5, QColor(15, 18, 24))
        gradient.setColorAt(1, QColor(10, 12, 16))
        painter.fillRect(self.rect(), gradient)

        pen = QPen(QColor(0, 255, 159, 10))
        pen.setWidth(1)
        painter.setPen(pen)
        
        step = 30
        offset = self.background_offset
        for x in range(0, self.width() + step, step):
            painter.drawLine(x + offset, 0, x + offset - step*2, self.height())
        for y in range(0, self.height() + step, step):
            painter.drawLine(0, y + offset, self.width(), y + offset - step*2)

    def format_character_info(self, character):
        html = f"""
        <div style='color: #e0e0e0; font-family: "Segoe UI"; letter-spacing: 1px;'>
            <h2 style='color: #00ff9f; margin-bottom: 25px; font-size: 24px; 
                      text-transform: uppercase; letter-spacing: 3px;'>
                ⚔️ {character['Name']} ⚔️
            </h2>
            
            <div style='background: rgba(0, 255, 159, 0.03); 
                       border: 1px solid rgba(0, 255, 159, 0.1);
                       padding: 20px; border-radius: 10px; 
                       margin-bottom: 20px;
                       backdrop-filter: blur(5px);'>
                <p><span style='color: #00ff9f;'>РАСА:</span> {character['Race']}</p>
                <p><span style='color: #00ff9f;'>КЛАСС:</span> {character['Class']}</p>
                <p><span style='color: #00ff9f;'>ПРЕДЫСТОРИЯ:</span> {character['Background']}</p>
                <p><span style='color: #00ff9f;'>МИРОВОЗЗРЕНИЕ:</span> {character['Alignment']}</p>
            </div>

            <h3 style='color: #00ff9f; margin-top: 20px; 
                      text-transform: uppercase; letter-spacing: 2px;'>
                📊 Характеристики
            </h3>
            <div style='background: rgba(0, 255, 159, 0.03);
                       border: 1px solid rgba(0, 255, 159, 0.1);
                       padding: 20px; border-radius: 10px;
                       backdrop-filter: blur(5px);'>
        """
        
        for attr, value in character['Attributes'].items():
            modifier = (value - 10) // 2
            sign = "+" if modifier >= 0 else ""
            html += f"<p><b>{attr}:</b> {value} ({sign}{modifier})</p>"
        
        html += "</div>"
        
        if 'spells' in character and character['spells']:
            html += f"""
                <h3 style='color: #00ff9f; margin-top: 20px;
                          text-transform: uppercase; letter-spacing: 2px;'>
                    ✨ Заклинания
                </h3>
                <div style='background: rgba(0, 255, 159, 0.03);
                           border: 1px solid rgba(0, 255, 159, 0.1);
                           padding: 20px; border-radius: 10px;
                           backdrop-filter: blur(5px);'>
                    <p><b style='color: #00ff9f;'>Заговоры:</b></p>
                    <ul style='color: #e0e0e0;'>
                        {''.join(f'<li>{spell}</li>' for spell in character['spells']['Cantrips'])}
                    </ul>
                    <p><b style='color: #00ff9f;'>1 уровень:</b></p>
                    <ul style='color: #e0e0e0;'>
                        {''.join(f'<li>{spell}</li>' for spell in character['spells']['Level 1'])}
                    </ul>
                </div>
            """
        
        html += "</div>"
        return html

    def display_character(self):
        try:
            character = generate_character()
            if character['Class'] in spells:
                character['spells'] = generate_spells(character['Class'])
            
            self.character_label.setText(self.format_character_info(character))
            self.character_info = character
            
            self.character_label.setStyleSheet("""
                QLabel {
                    background: rgba(20, 20, 20, 0.8);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    padding: 25px;
                    line-height: 1.6;
                }
            """)
            
            self.statusBar().showMessage("Персонаж успешно создан!", 3000)
            
        except Exception as e:
            self.statusBar().showMessage(f"Ошибка: {str(e)}", 3000)

    def copy_to_clipboard(self):
        if self.character_info:
            clipboard = QGuiApplication.clipboard()
            text = f"""
Имя: {self.character_info['Name']}
Пол: {self.character_info['Gender']}
Раса: {self.character_info['Race']}
Клас: {self.character_info['Class']}
Предыстория: {self.character_info['Background']}
Мировоззрение: {self.character_info['Alignment']}
Особенности: {self.character_info['Traits']}
Оружие: {self.character_info['Weapon']}
Способности: {self.character_info['Abilities']}

Характеристики:
"""
            for attr, value in self.character_info['Attributes'].items():
                modifier = (value - 10) // 2
                sign = "+" if modifier >= 0 else ""
                text += f"{attr}: {value} ({sign}{modifier})\n"
            
            clipboard.setText(text)
            self.statusBar().showMessage("Информация скопирована в буфер обмена!", 3000)
        else:
            self.statusBar().showMessage("Сначала создайте персонажа!", 3000)

    def save_to_pdf(self):
        """Сохраняет информацию о персонаже в PDF файл"""
        if not self.character_info:
            self.statusBar().showMessage("Сначала создайте персонажа!", 3000)
            return

        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить PDF",
                f"{self.character_info['Name']}.pdf",
                "PDF Files (*.pdf)"
            )

            if not file_path:
                return

            c = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4

            font_name = 'MainFont' if font_path else 'Helvetica'

            c.setTitle(f"D&D Character - {self.character_info['Name']}")
            c.setFont(font_name, 24)
            c.drawString(50, height - 50, f"Персонаж D&D: {self.character_info['Name']}")
            
            c.setFont(font_name, 16)
            c.drawString(50, height - 100, "Основная информация")
            
            c.setFont(font_name, 12)
            y = height - 120
            info_list = [
                f"Пол: {self.character_info['Gender']}",
                f"Раса: {self.character_info['Race']}",
                f"Класс: {self.character_info['Class']}",
                f"Предыстория: {self.character_info['Background']}",
                f"Мировоззрение: {self.character_info['Alignment']}",
                f"Особенности: {self.character_info['Traits']}",
                f"Оружие: {self.character_info['Weapon']}",
                f"Способности: {self.character_info['Abilities']}"
            ]
            
            for info in info_list:
                y -= 20
                c.drawString(50, y, info)
            
            y -= 40
            c.setFont(font_name, 16)
            c.drawString(50, y, "Характеристики")
            
            c.setFont(font_name, 12)
            for attr, value in self.character_info['Attributes'].items():
                y -= 20
                modifier = (value - 10) // 2
                sign = "+" if modifier >= 0 else ""
                c.drawString(50, y, f"{attr}: {value} ({sign}{modifier})")
            
            if 'spells' in self.character_info and self.character_info['spells']:
                y -= 40
                c.setFont(font_name, 16)
                c.drawString(50, y, "Заклинания")
                
                c.setFont(font_name, 12)
                y -= 20
                c.drawString(50, y, "Заговоры:")
                for spell in self.character_info['spells']['Cantrips']:
                    y -= 20
                    c.drawString(70, y, f"• {spell}")
                
                y -= 20
                c.drawString(50, y, "Заклинания 1 уровня:")
                for spell in self.character_info['spells']['Level 1']:
                    y -= 20
                    c.drawString(70, y, f"• {spell}")
            
            c.save()
            self.statusBar().showMessage(f"PDF успешно сохранен: {file_path}", 3000)
            
        except Exception as e:
            print(f"Подробная ошибка при сохранении PDF: {str(e)}")
            self.statusBar().showMessage(f"Ошибка при сохранении PDF: {str(e)}", 3000)


def main():
    try:
        app = QApplication(sys.argv)
        ex = CharacterGenerator()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
