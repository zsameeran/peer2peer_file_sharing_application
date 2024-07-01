# peer2peer_file_sharing_application
peer to peer application that allows us to share files between Peers without relying on any Central server. To achieve this We have used the sockets libraries from Python which are generally used for client and server models but we have modified it a little bit and used it to achieve peer-to-peer communication.


This peer-to-peer system is designed for peers who are all across the globe with different IP
addresses and ports. To implement this on the local machine we have only a single IP address
hence we use different ports for different peers. Also as we have to run various peers on a
single machine and each Peer has its own server listening and clients connected to various
servers of the different Peer we have to use threads that run parallelly with the main thread and
represent a different Peer.
I have used a thread for each Peer and then again a separate sub-thread for the server of that
Peer which listens for the client for connection. I have also created a user interface for easy
interaction. In this UI user first has to add a peer by entering the port number for the peer. As we
have to implement this on a single local machine each peer is represented or identified by the
port number which it runs on



![Capture](https://github.com/zsameeran/peer2peer_file_sharing_application/assets/53044906/c3a97b13-977d-4e36-a04d-d738e94fb297)


The port number for the pear and add a new Peer. After adding several peers they get
automatically connected to each other in the background. Hence we create a peer-to-peer
network on a local machine.
We can check the connections of each beer by clicking on the port number of the Peer on the
left list box. The connections of the peer will be displayed on the right list box. As shown in the
image
Here, in the image we can see the connections of the Peer named 6000 have connections to
the rest of the Peers that is to 7000 and to 8000.
We can select the connections and then click on the send files button to browse the file that we
have to send. Then it will send the file to the selected peer



![image](https://github.com/zsameeran/peer2peer_file_sharing_application/assets/53044906/8a172121-2eeb-495e-b949-02ebc9d5b771)
