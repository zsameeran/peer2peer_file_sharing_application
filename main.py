import socket
import threading
import os
import tkinter as tk
from tkinter import simpledialog , filedialog , messagebox

SERVER = socket.gethostbyname(socket.gethostname())
isServerCreatedFlag = False
peersList = {}
peerServerList = []
global currentPeer

KEY = b"M23CSE019"
NONCE = b"M23CSE019NONCE"

def handle_client(connection, addr, port):
    # it handle clients. whenever any client is connected this function runs in a thread and always listens for files.
    print(f"[NEW CONNECTION] {addr} connected on {port}")
    connected = True
    while connected:
        name = connection.recv(1024).decode()
        fileSize = connection.recv(1024).decode()
        fileR = connection.recv(1024)
        while len(fileR) < int(fileSize):
            fileR += connection.recv(1024)
        writefile = open(f"recv_{name}", "wb")
        writefile.write(fileR)
        writefile.flush()
        os.fsync(writefile.fileno())
        writefile.close()
        if(len(fileR) == int(fileSize)):
            messagebox.showinfo("Message", " File Transferred Successfully!")
            print("File transferred")
        else:
            messagebox.showerror("Message", " File Transferred Failed!")


# this function runs in a new thread and continuosly listens for incomming connections and accept them
def startNewListening(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, port))
    server.listen()
    print(f"SERVER IS LISTENING ON {SERVER}{port}")
    serverAdd = []
    serverAdd.append(SERVER)
    serverAdd.append(port)
    peerServerList.append(serverAdd)
    global isServerCreatedFlag
    isServerCreatedFlag = True
    while True:
        connection_object, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection_object, addr, port))
        thread.start()


def createPeerClients():
    # client code and connect to every port in the list except the arg 'port'
    if len(peerServerList) == 1:
        return
    for i in range(len(peerServerList)):
        newPort = peerServerList[len(peerServerList) - 1][1]
        if peerServerList[i][1] != newPort:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER, newPort))
            peerConnection = []
            peerConnection.append(newPort)
            peerConnection.append(client)
            if peerServerList[i][1] in peersList:
                peersList[peerServerList[i][1]].append(peerConnection)
            else:
                peersList[peerServerList[i][1]] = [peerConnection]

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER, peerServerList[i][1]))
            peerConnection = []
            peerConnection.append(peerServerList[i][1])
            peerConnection.append(client)

            if newPort in peersList:
                peersList[newPort].append(peerConnection)
            else:
                peersList[newPort] = [peerConnection]
        else: continue

def startPeer(peerPort):
    global isServerCreatedFlag
    isServerCreatedFlag = False
    listenThread = threading.Thread(target=startNewListening, args=(peerPort,))
    listenThread.start()
    # wait untill server is created for the peer and then create client connections
    while not isServerCreatedFlag:
        continue
    createPeerClients()

def sendMsg(peer1, peer2 ,filePath , data ):
    for con in range(len(peersList[peer1])):
        if peersList[peer1][con][0] == peer2[0]:
            fileName = filePath.split('/')[-1]
            peersList[peer1][con][1].send(fileName.encode())
            peersList[peer1][con][1].send(str(len(data)).encode())
            peersList[peer1][con][1].send(data)
            return


def addNewPeer():
    port = simpledialog.askinteger("Input", "Enter Port of the PEER:")
    if port:
        startPeer(port)
        peerlistbox.delete(0,tk.END)
        populatePeerListBox(peerlistbox, peerServerList)


# GUI CODE FOR THE APPLICATION

def populatePeerListBox(listbox, peers):
    for item in peers:
        listbox.insert(tk.END, item)


def updatePeerConnectins(event):

    selectedPeer = peerlistbox.curselection()

    if selectedPeer:
        selectedPeerName = peerlistbox.get(selectedPeer[0])
        peerConnectionlistbox.delete(0, tk.END)

        if selectedPeerName[1] in peersList:
            print(peersList[selectedPeerName[1]])
            global currentPeer
            currentPeer = selectedPeerName[1]
            print("$%%")
            print(peersList[selectedPeerName[1]])
            populatePeerListBox(peerConnectionlistbox, peersList[selectedPeerName[1]])

    updateFileBtnState()


def updateFileBtnState():
    selection = peerConnectionlistbox.curselection()
    if selection:
        print_button.config(state=tk.NORMAL)
    else:
        print_button.config(state=tk.DISABLED)


def transferFile():
    selectedPeerCon = peerConnectionlistbox.curselection()
    if selectedPeerCon:
        filePath = filedialog.askopenfilename()
        file = open(filePath, "rb")
        data = file.read()
        print(currentPeer)
        receiverPeer = peersList[currentPeer][selectedPeerCon[0]]
        print(receiverPeer)
        sendMsg(currentPeer,receiverPeer,filePath , data)



root = tk.Tk()
root.geometry("500x500")
root.title("Peer To Peer Network Application")


left_frame = tk.Frame(root, width=200, height=400, bg="darkgray")
right_frame = tk.Frame(root, width=200, height=400, bg="darkgray")


left_label = tk.Label(left_frame, text="PEERS" , font=("Arial", 12), bg="darkgray", fg="black")
right_label = tk.Label(right_frame, text="CONNECTIONS OF PEERS" ,font=("Arial", 12),  bg="darkgray", fg="black")

peerlistbox = tk.Listbox(left_frame, selectmode=tk.SINGLE , bg="darkgray")
peerConnectionlistbox = tk.Listbox(right_frame, selectmode=tk.SINGLE , bg="darkgray")
addPeerBtn = tk.Button(root, text="Add New Peer", font=("Arial", 12), bg="#283E64", fg="white" , padx=5 ,pady=5 ,
                       command=addNewPeer)


peerlistbox.bind("<<ListboxSelect>>", updatePeerConnectins)

addPeerBtn.pack( fill=tk.BOTH , pady=10 , padx=10)
left_label.pack(pady=5)
peerlistbox.pack(fill=tk.BOTH, expand=True)


right_label.pack(pady=5)
peerConnectionlistbox.pack(fill=tk.BOTH, expand=True)

print_button = tk.Button(root, text="Send File to selected User", command=transferFile, state=tk.DISABLED, bg="#283E64",
                         fg="#FFFFFF" , font=("Arial", 12, "bold"))

print_button.pack(side=tk.BOTTOM, fill=tk.BOTH, pady=5 , padx= 10 )

left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

root.mainloop()

