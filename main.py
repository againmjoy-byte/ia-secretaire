from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class SecretaireIAApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Secrétaire IA Multilingue'))
        layout.add_widget(Button(text='Parler'))
        return layout

if __name__ == '__main__':
    SecretaireIAApp().run()
