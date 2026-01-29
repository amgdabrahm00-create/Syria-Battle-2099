from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        # تصميم أزرار اختيار الشخصية
        self.btn_m = Button(text="إختيار رجل (Warrior)", size_hint=(.4, .1), pos_hint={'x': .05, 'y': .5})
        self.btn_f = Button(text="إختيار امرأة (Agent)", size_hint=(.4, .1), pos_hint={'x': .55, 'y': .5})
        
        self.btn_m.bind(on_release=self.select_male)
        self.btn_f.bind(on_release=self.select_female)
        
        layout.add_widget(self.btn_m)
        layout.add_widget(self.btn_f)
        self.add_widget(layout)

    def select_male(self, instance):
        App.get_running_app().player_gender = "male"
        self.manager.current = 'game'

    def select_female(self, instance):
        App.get_running_app().player_gender = "female"
        self.manager.current = 'game'

class GameScreen(Screen):
    def on_enter(self):
        self.game = SyriaBattleEngine()
        self.add_widget(self.game)

class SyriaBattleEngine(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_pos = [Window.width/2, Window.height/2]
        self.zone_r = 1500
        Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, dt):
        self.canvas.clear()
        with self.canvas:
            Color(0.1, 0.2, 0.1) # الأرضية
            Rectangle(pos=(0,0), size=(Window.width*2, Window.height*2))
            
            Color(0, 0, 1, 0.3) # الزون الأزرق
            Ellipse(pos=(Window.width/2 - self.zone_r/2, Window.height/2 - self.zone_r/2), size=(self.zone_r, self.zone_r))
            
            # تغيير لون اللاعب حسب الجنس المختار
            if App.get_running_app().player_gender == "male":
                Color(0.2, 0.6, 1) # أزرق للرجل
            else:
                Color(1, 0.4, 0.7) # وردي للمرأة
                
            Rectangle(pos=self.player_pos, size=(60, 60))
        
        if self.zone_r > 200: self.zone_r -= 0.5

    def on_touch_move(self, touch):
        self.player_pos = [touch.x - 30, touch.y - 30]

class SyriaBattleApp(App):
    player_gender = "male"
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == "__main__":
    SyriaBattleApp().run()
      
