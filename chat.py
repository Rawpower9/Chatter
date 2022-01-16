import platform
import socket
import select
import threading
from PySide6.QtWidgets import (
    QApplication
    ,QWidget
    ,QLabel
    ,QPushButton
    ,QVBoxLayout
    ,QPlainTextEdit
    ,QLineEdit
)



connected = False
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

app = QApplication([])
app.setStyle(platform.system().lower())
window = QWidget()
v_layout = QVBoxLayout()

btn1 = QPushButton('Send')
btn1.setShortcut("return")

chatInput = QLineEdit("Type here to chat!")
chatInput.setMaximumSize(window.width(), 50)

chatb = QPlainTextEdit("---This is the start of the chat---")
chatb.setReadOnly(True)
chatb.setMinimumSize(window.width(), window.height())

v_layout.addWidget(QLabel('CHATBOX!'))
v_layout.addWidget(chatb)
v_layout.addWidget(chatInput)
v_layout.addWidget(btn1)

def on_btn1_clicked():
    global connected, server
    if not connected:
        connected = True
        text = chatInput.text()
        chatInput.setText("")
        text = text.replace(" ","",text.count(" "))
        text = text.split(":")
        ip = text[0]
        port = int(text[1])
        server.connect((ip,port))

        def whileLoop():
            while True:

                sockets_list = [server]

                read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

                for socks in read_sockets:
                    receive_message(str(socks.recv(2048), "utf-8"))
            server.close()

        t1 = threading.Thread(target=whileLoop)
        t1.start()
    else:
        message = chatInput.text()
        server.send(bytes(message, "utf-8"))
        chatb.appendPlainText("<YOU> " + message)
        chatInput.setText("")

def receive_message(message):
    chatb.appendPlainText(message)


btn1.clicked.connect(on_btn1_clicked)

window.setLayout(v_layout)
window.show()
app.exec()