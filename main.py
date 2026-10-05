import json, os
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

Window.clearcolor = (0.08, 0.08, 0.12, 1)
LULUS = 0.7


class CeritaApp(App):
    def build(self):
        base = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base, "chapters.json"), encoding="utf-8") as f:
            self.bab = json.load(f)
        self.simpan_file = os.path.join(self.user_data_dir, "progres.json")
        self.idx = self.muat()
        self.root_box = BoxLayout(orientation="vertical", padding=20, spacing=12)
        self.baca()
        return self.root_box

    def muat(self):
        try:
            with open(self.simpan_file) as f:
                return min(json.load(f)["bab"], len(self.bab) - 1)
        except Exception:
            return 0

    def simpan(self):
        with open(self.simpan_file, "w") as f:
            json.dump({"bab": self.idx}, f)

    def label(self, teks, ukuran="18sp"):
        lb = Label(text=teks, font_size=ukuran, halign="left", valign="top",
                   size_hint_y=None, text_size=(Window.width - 40, None))
        lb.bind(texture_size=lambda i, v: setattr(i, "height", v[1]))
        return lb

    def tombol(self, teks, aksi):
        b = Button(text=teks, size_hint_y=None, height=60, font_size="17sp")
        b.bind(on_release=lambda x: aksi())
        return b

    def baca(self):
        self.root_box.clear_widgets()
        b = self.bab[self.idx]
        self.root_box.add_widget(self.label(b["judul"], "24sp"))
        sv = ScrollView()
        sv.add_widget(self.label(b["teks"]))
        self.root_box.add_widget(sv)
        self.root_box.add_widget(self.tombol("Mulai Kuis", self.mulai_kuis))

    def mulai_kuis(self):
        self.q = 0
        self.benar = 0
        self.tanya()

    def tanya(self):
        self.root_box.clear_widgets()
        kuis = self.bab[self.idx]["kuis"]
        s = kuis[self.q]
        self.root_box.add_widget(
            self.label("Soal %d dari %d" % (self.q + 1, len(kuis)), "14sp"))
        self.root_box.add_widget(self.label(s["tanya"], "22sp"))
        for i, p in enumerate(s["pilihan"]):
            self.root_box.add_widget(self.tombol(p, lambda i=i: self.jawab(i)))
        self.root_box.add_widget(Label())

    def jawab(self, i):
        kuis = self.bab[self.idx]["kuis"]
        if i == kuis[self.q]["jawab"]:
            self.benar += 1
        self.q += 1
        if self.q < len(kuis):
            self.tanya()
        else:
            self.hasil()

    def hasil(self):
        self.root_box.clear_widgets()
        total = len(self.bab[self.idx]["kuis"])
        lulus = self.benar / total >= LULUS
        self.root_box.add_widget(
            self.label("Skor: %d dari %d" % (self.benar, total), "26sp"))
        if lulus and self.idx + 1 < len(self.bab):
            self.root_box.add_widget(self.label("Lulus! Lanjut ya."))
            self.root_box.add_widget(self.tombol("Chapter berikutnya", self.lanjut))
        elif lulus:
            self.root_box.add_widget(self.label("Tamat! Terima kasih sudah membaca."))
        else:
            self.root_box.add_widget(self.label("Belum lulus. Baca lagi, lalu coba lagi."))
            self.root_box.add_widget(self.tombol("Baca ulang", self.baca))
        self.root_box.add_widget(Label())

    def lanjut(self):
        self.idx += 1
        self.simpan()
        self.baca()


CeritaApp().run()
