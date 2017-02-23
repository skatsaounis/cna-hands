package main

import (
	"fmt"
	"golang.org/x/net/netutil"
	"log"
	"net"
	"net/http"
	"os"
	"runtime"
	"time"
)

// Sync -> make responses synchronous to have steady rate
var Sync = make(chan bool, 1)

func serverDoWork(w http.ResponseWriter, r *http.Request) {
	log.Println("Processing request")
	val := <-Sync
	sleepTime := 500
	time.Sleep(time.Duration(sleepTime) * time.Millisecond)
	fmt.Fprintf(w, "Response sent after %d ms\n", sleepTime)
	fmt.Println("Response sent")
	Sync <- val
}

func serverStop(w http.ResponseWriter, r *http.Request) {
	fmt.Println("server exiting...")
	os.Exit(0)
}

func serverHeartbeat(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "tick\n")
}

func main() {
	runtime.GOMAXPROCS(runtime.NumCPU())
	connectionCount := 1
	log.Println("Serving on port 4444")
	Sync <- true

	http.HandleFunc("/doWork", serverDoWork)
	http.HandleFunc("/stop", serverStop)
	http.HandleFunc("/heartbeat", serverHeartbeat)

	l, _ := net.Listen("tcp", ":4444")
	defer l.Close()
	l = netutil.LimitListener(l, connectionCount)
	log.Fatal(http.Serve(l, nil))
}
