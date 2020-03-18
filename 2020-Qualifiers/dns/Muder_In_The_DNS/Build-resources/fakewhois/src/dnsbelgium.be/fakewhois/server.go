package main

import (
	"fmt"
	"math/rand"
	"net"
	"os"
)

const (
	CONN_HOST = ""
	CONN_PORT = "4343"
	CONN_TYPE = "tcp"
)

var unhelpfullResponses = []string{
	"This not what we're looking for.\n",
	"Maybe you should try something different.\n",
	"Are you really going to keep trying this?.\n",
	"Close but no cigar.\n",
	"It wasn't me! Someone else did it...\n",
	"This is not the murderer you're looking for.\n"}

var flag = `
▓█████▄  ███▄    █   ██████     ▄▄▄▄   ▓█████  ██▓      ▄████  ██▓ █    ██  ███▄ ▄███▓
▒██▀ ██▌ ██ ▀█   █ ▒██    ▒    ▓█████▄ ▓█   ▀ ▓██▒     ██▒ ▀█▒▓██▒ ██  ▓██▒▓██▒▀█▀ ██▒
░██   █▌▓██  ▀█ ██▒░ ▓██▄      ▒██▒ ▄██▒███   ▒██░    ▒██░▄▄▄░▒██▒▓██  ▒██░▓██    ▓██░
░▓█▄   ▌▓██▒  ▐▌██▒  ▒   ██▒   ▒██░█▀  ▒▓█  ▄ ▒██░    ░▓█  ██▓░██░▓▓█  ░██░▒██    ▒██ 
░▒████▓ ▒██░   ▓██░▒██████▒▒   ░▓█  ▀█▓░▒████▒░██████▒░▒▓███▀▒░██░▒▒█████▓ ▒██▒   ░██▒
 ▒▒▓  ▒ ░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░   ░▒▓███▀▒░░ ▒░ ░░ ▒░▓  ░ ░▒   ▒ ░▓  ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░
 ░ ▒  ▒ ░ ░░   ░ ▒░░ ░▒  ░ ░   ▒░▒   ░  ░ ░  ░░ ░ ▒  ░  ░   ░  ▒ ░░░▒░ ░ ░ ░  ░      ░
 ░ ░  ░    ░   ░ ░ ░  ░  ░      ░    ░    ░     ░ ░   ░ ░   ░  ▒ ░ ░░░ ░ ░ ░      ░   
   ░             ░       ░      ░         ░  ░    ░  ░      ░  ░     ░            ░   
 ░                                   ░                                                


>>>>>>   CSC{It was Colonel Mustard, in the living room, with a candle stick}   <<<<<<

`

func main() {
	// Listen for incoming connections.
	l, err := net.Listen(CONN_TYPE, ":"+CONN_PORT)
	if err != nil {
		fmt.Println("Error listening:", err.Error())
		os.Exit(1)
	}
	// Close the listener when the application closes.
	defer l.Close()
	fmt.Println("Listening on " + CONN_HOST + ":" + CONN_PORT)
	for {
		// Listen for an incoming connection.
		conn, err := l.Accept()
		if err != nil {
			fmt.Println("Error accepting: ", err.Error())
			os.Exit(1)
		}

		//logs an incoming message
		fmt.Printf("Received message %s -> %s \n", conn.RemoteAddr(), conn.LocalAddr())

		// Handle connections in a new goroutine.
		go handleRequest(conn)
	}
}

// Handles incoming requests.
func handleRequest(conn net.Conn) {
	// Make a buffer to hold incoming data.
	buf := make([]byte, 1024)
	// Read the incoming connection into the buffer.
	length, err := conn.Read(buf)
	if err != nil {
		fmt.Println("Error reading:", err.Error())
	}

	// Builds the message.
	message := string(buf[:length-2])
	fmt.Printf("  %s -> %s \n", conn.RemoteAddr(), message)

	if message == "with-a-candlestick.i-killed-black.be" {
		conn.Write([]byte(flag))
	} else if message == "murderer.i-killed-black.be" {
		conn.Write([]byte(`
You found me! I, Colonel Musterd did it...

How did i do it? 
Was it with-a-knive or maybe with-a-rope?

`))
	} else {
		// Write the message in the connection channel.
		conn.Write([]byte(unhelpfullResponses[rand.Intn(len(unhelpfullResponses))]))
	}
	// Close the connection when you're done with it.
	conn.Close()
}
