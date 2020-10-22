from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window

KV = '''
BoxLayout:
    orientation: "vertical"

    MDToolbar:
        id: layout
        title: "MDToolbar"
        canvas:
            Rectangle:
                source: 'images/logo.png'
                pos: (((self.parent.size[0])/2)-30,self.pos[1])
                size: self.parent.width, 60

    MDLabel:
        text: "Content"
        halign: "center"
'''


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)


Window.show_cursor = True

Test().run()