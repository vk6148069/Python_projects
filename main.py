import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://duckduckgo.com/'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        history_btn = QAction('History', self)
        history_btn.triggered.connect(self.show_history)
        navbar.addAction(history_btn)

        self.browser.urlChanged.connect(self.update_url)

        self.history = []
        self.history_window = None
        self.load_history()

    def navigate_home(self):
        self.browser.setUrl(QUrl('https://www.google.com/search?q=all+search+engines&rlz=1C1ONGR_enIN1113IN1114&oq=all+search+engines&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORiABDIHCAEQABiABDIHCAIQABiABDIHCAMQABiABDIHCAQQABiABDIICAUQABgWGB4yCAgGEAAYFhgeMgYIBxBFGDzSAQg1MjA4ajBqN6gCCLACAQ&sourceid=chrome&ie=UTF-8'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))
        self.history.append(url)
        self.save_history()

    def update_url(self, q):
        self.url_bar.setText(q.toString())
        self.history.append(q.toString())
        self.save_history()

    def show_history(self):
        if self.history_window is None:
            self.history_window = QWidget()
            self.history_window.setWindowTitle('History')
            layout = QVBoxLayout()
            self.history_window.setLayout(layout)

            for i, url in enumerate(self.history):
                btn = QPushButton(url)
                btn.clicked.connect(lambda url=url: self.navigate_to_url_from_history(url))
                layout.addWidget(btn)

            clear_history_btn = QPushButton('Clear History')
            clear_history_btn.clicked.connect(self.clear_history)
            layout.addWidget(clear_history_btn)

            self.history_window.show()
        else:
            self.history_window.show()

    def navigate_to_url_from_history(self, url):
        self.browser.setUrl(QUrl(url))

    def clear_history(self):
        self.history = []
        self.save_history()
        self.history_window.close()
        self.show_history()

    def load_history(self):
        try:
            with open('history.txt', 'r') as f:
                self.history = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            pass

    def save_history(self):
        with open('history.txt', 'w') as f:
            for url in self.history:
                f.write(url + '\n')


app = QApplication(sys.argv)
QApplication.setApplicationName('Browseprivately')
window = MainWindow()
app.exec_()
input()