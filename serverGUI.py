import socket
from _thread import start_new_thread
import threading
import platform
from PySide6.QtWidgets import (
    QApplication
, QMessageBox
, QWidget
, QLabel
, QPushButton
, QVBoxLayout
, QPlainTextEdit
)

list_of_clients = []

def clientthread(conn, addr):
    # sends a message to the client whose user object is conn
    conn.send(bytes("Welcome to this chatroom!\n", "utf-8"))

    while True:
        try:
            message = str(conn.recv(2048), "utf-8")
            print("<" + str(addr[0]) + "> " + str(message))
            # Calls broadcast function to send message to all
            message_to_send = "<" + str(addr[0]) + "> " + str(message)
            broadcast(message_to_send, conn)
        except:
            continue


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(bytes(message, "utf-8"))
            except:
                print("closing Client", clients)
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

app = QApplication([])
app.setStyle(platform.system().lower())
window = QWidget()
v_layout = QVBoxLayout()

connect = QPushButton('connect')

IP = QPlainTextEdit("localhost")
IP.setMaximumSize(100, 25)
IP.setMinimumSize(100, 25)

port = QPlainTextEdit("port")
port.setMaximumSize(100, 25)
port.setMinimumSize(100, 25)

v_layout.addWidget(QLabel('IP and Port'))
v_layout.addWidget(IP)
v_layout.addWidget(port)

v_layout.addWidget(connect)

#button "connect" connects AND disconnects the server
disconn = False


def on_btn1_clicked():
    global disconn
    if disconn:
        # conn.close()
        server.close()
        return
    server.bind((IP.toPlainText(), int(port.toPlainText())))
    server.listen(100)

    connect.setText('disconnect')
    disconn = True
    alert = QMessageBox()
    alert.setText('Connected')
    alert.exec()
    def whileLoop():
        global list_of_clients
        while True:
            conn, addr = server.accept()
            list_of_clients.append(conn)
            print(addr[0] + " connected")
            start_new_thread(clientthread, (conn, addr))
    t1 = threading.Thread(target=whileLoop)
    t1.start()


connect.clicked.connect(on_btn1_clicked)

window.setLayout(v_layout)
window.show()
app.exec()
