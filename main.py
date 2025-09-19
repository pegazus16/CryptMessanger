# main.py
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
import ciphers

class CryptoApp(MDApp):
    def build(self):
        # ✅ Thème par défaut clair
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        # ✅ Support portrait/paysage
        Window.softinput_mode = "pan"

        self.layout = MDBoxLayout(orientation="vertical", padding=20, spacing=12)

        # Champ message
        self.input_message = MDTextField(hint_text="Entrez le message", multiline=True, size_hint_y=None, height=150)
        self.layout.add_widget(self.input_message)

        # Menu algorithme
        self.selected_algo = "César"
        algos = ["César", "Vigenère", "Atbash", "Playfair", "Hill"]
        self.menu_items = [
            {"text": algo, "viewclass": "OneLineListItem", "on_release": lambda x=algo: self.set_algorithm(x)}
            for algo in algos
        ]
        self.menu = MDDropdownMenu(items=self.menu_items, width_mult=4)
        self.algo_button = MDRaisedButton(text="Choisir : César", on_release=self.open_menu)
        self.layout.add_widget(self.algo_button)

        # Champ clé
        self.key_input = MDTextField(hint_text="Entrez la clé (ex: 3 | KEY | 3 3;2 5)", mode="rectangle")
        self.layout.add_widget(self.key_input)

        # Boutons action
        self.layout.add_widget(MDRaisedButton(text="Crypter", md_bg_color=(0,0.6,0,1), on_release=self.encrypt_message))
        self.layout.add_widget(MDRaisedButton(text="Décrypter", md_bg_color=(0.7,0,0,1), on_release=self.decrypt_message))
        self.layout.add_widget(MDRaisedButton(text="Copier le résultat", on_release=self.copy_to_clipboard))

        # Résultat
        self.result_label = MDLabel(text="Résultat affiché ici", halign="center", theme_text_color="Primary")
        self.layout.add_widget(self.result_label)

        # ✅ Ligne bascule thème
        theme_row = MDGridLayout(cols=2, adaptive_height=True, spacing=10, padding=(0,10))
        theme_row.add_widget(MDLabel(text="🌞 / 🌙 Thème", halign="left"))
        self.theme_switch = MDSwitch(active=False)  # False = Light, True = Dark
        self.theme_switch.bind(active=self.toggle_theme)
        theme_row.add_widget(self.theme_switch)
        self.layout.add_widget(theme_row)

        return self.layout

    def open_menu(self, instance):
        self.menu.caller = instance
        self.menu.open()

    def set_algorithm(self, algo):
        self.selected_algo = algo
        self.algo_button.text = f"Choisir : {algo}"
        self.menu.dismiss()

    def encrypt_message(self, instance):
        text = self.input_message.text or ""
        key = self.key_input.text or ""
        algo = self.selected_algo
        try:
            if algo == "César":
                result = ciphers.caesar_encrypt(text, int(key))
            elif algo == "Vigenère":
                result = ciphers.vigenere_encrypt(text, key)
            elif algo == "Atbash":
                result = ciphers.atbash_encrypt(text)
            elif algo == "Playfair":
                result = ciphers.playfair_encrypt(text, key)
            elif algo == "Hill":
                matrix = [list(map(int, row.split())) for row in key.split(";")]
                result = ciphers.hill_encrypt(text, matrix)
            else:
                result = "Algorithme non supporté"
        except Exception as e:
            result = f"Erreur : {e}"
        self.result_label.text = result

    def decrypt_message(self, instance):
        text = self.input_message.text or ""
        key = self.key_input.text or ""
        algo = self.selected_algo
        try:
            if algo == "César":
                result = ciphers.caesar_decrypt(text, int(key))
            elif algo == "Vigenère":
                result = ciphers.vigenere_decrypt(text, key)
            elif algo == "Atbash":
                result = ciphers.atbash_decrypt(text)
            elif algo == "Playfair":
                result = ciphers.playfair_decrypt(text, key)
            elif algo == "Hill":
                matrix = [list(map(int, row.split())) for row in key.split(";")]
                result = ciphers.hill_decrypt(text, matrix)
            else:
                result = "Algorithme non supporté"
        except Exception as e:
            result = f"Erreur : {e}"
        self.result_label.text = result

    def copy_to_clipboard(self, instance):
        text = self.result_label.text
        if text and text != "Résultat affiché ici":
            Clipboard.copy(text)
            Snackbar(text="✅ Résultat copié !").open()
        else:
            Snackbar(text="⚠️ Aucun résultat à copier").open()

    def toggle_theme(self, switch, value):
        # ✅ Bascule thème clair/sombre
        self.theme_cls.theme_style = "Dark" if value else "Light"

if __name__ == "__main__":
    CryptoApp().run()
