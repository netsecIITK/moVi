package main

import (
    "net"
    "os"
    "strconv"
)

type ConnectionHandler func(net.Conn)

type Server struct {
    hostName       string
    portNumber     int
    connectionType string
}

func (s Server) Listen(handler ConnectionHandler) {
    socket, err :=
        net.Listen(s.connectionType, s.hostName+":"+strconv.Itoa(s.portNumber))
    if err != nil {
        Error.Println("Error listening: ", err.Error())
        os.Exit(1)
    }

    defer socket.Close()

    Info.Println("Listening on " + s.hostName + ":" + strconv.Itoa(s.portNumber))
    for {
        // Listen for an incoming connection.
        conn, err := socket.Accept()
        if err != nil {
            Error.Println("Error accepting: ", err.Error())
            os.Exit(1)
        }
        // Handle connections in a new goroutine.
        go handler(conn)
    }
}
