package main

import (
    "fmt"
    "net"
    "strconv"
)

func main() {
    server := Server{"127.0.0.1", 3456, "tcp"}
    server.Listen(handleRequest)
}

// Handles incoming requests.
func handleRequest(conn net.Conn) {
    // Make a buffer to hold incoming data.
    buf := make([]byte, 1024)
    // Read the incoming connection into the buffer.
    reqLen, err := conn.Read(buf)
    if err != nil {
        fmt.Println("Error reading:", err.Error())
    }
    // Send a response back to person contacting us.
    conn.Write([]byte("Message received of length: " + strconv.Itoa(reqLen)))
    // Close the connection when you're done with it.
    conn.Close()
}
