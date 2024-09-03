import random
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont, QGuiApplication, QColor
from PyQt5.QtCore import Qt


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
    return character


class CharacterGenerator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setWindowTitle("D&D Character Generator")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: #f0f0f0; border-radius: 10px;")


        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)


        title_font = QFont("Arial", 18, QFont.Bold)
        text_font = QFont("Arial", 12)


        self.title_label = QLabel("Generate Your D&D Character", self)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #0078d7;")
        self.layout.addWidget(self.title_label)


        self.character_label = QLabel("", self)
        self.character_label.setFont(text_font)
        self.character_label.setWordWrap(True)
        self.character_label.setStyleSheet("color: #333333; background-color: #ffffff; border-radius: 10px; padding: 10px;")
        self.layout.addWidget(self.character_label)


        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)


        self.generate_button = QPushButton("Generate Character", self)
        self.generate_button.setFont(text_font)
        self.generate_button.setStyleSheet(self.button_style("#0078d7", "#ffffff"))
        self.generate_button.clicked.connect(self.display_character)
        self.button_layout.addWidget(self.generate_button)


        self.copy_button = QPushButton("Copy to Clipboard", self)
        self.copy_button.setFont(text_font)
        self.copy_button.setStyleSheet(self.button_style("#28a745", "#ffffff"))
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.button_layout.addWidget(self.copy_button)


    def button_style(self, bg_color, text_color):
        return f"""
        QPushButton {{
            background-color: {bg_color};
            color: {text_color};
            border-radius: 10px;
            padding: 10px;
        }}
        QPushButton:pressed {{
            background-color: {self.darken_color(bg_color)};
        }}
        """


    def darken_color(self, hex_color):
        color = QColor(hex_color)
        darker_color = color.darker(120)
        return darker_color.name()


    def display_character(self):
        character = generate_character()
        self.character_info = (
            f"Name: {character['Name']}\n"
            f"Gender: {character['Gender']}\n"
            f"Race: {character['Race']}\n"
            f"Class: {character['Class']}\n"
            f"Background: {character['Background']}\n"
            f"Alignment: {character['Alignment']}\n"
            f"Traits: {character['Traits']}\n"
            f"Weapon: {character['Weapon']}\n"
            f"Abilities: {character['Abilities']}\n"
            f"Attributes:\n"
            f"  Strength: {character['Attributes']['Strength']}\n"
            f"  Dexterity: {character['Attributes']['Dexterity']}\n"
            f"  Constitution: {character['Attributes']['Constitution']}\n"
            f"  Intelligence: {character['Attributes']['Intelligence']}\n"
            f"  Wisdom: {character['Attributes']['Wisdom']}\n"
            f"  Charisma: {character['Attributes']['Charisma']}\n"
        )
        self.character_label.setText(self.character_info)


    def copy_to_clipboard(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.character_info)


def main():
    app = QApplication(sys.argv)
    ex = CharacterGenerator()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
