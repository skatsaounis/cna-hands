package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
)

type stack []int

func (s stack) Push(v int) stack {
	return append(s, v)
}

func (s stack) Pop() (stack, int) {
	// FIXME: What do we do if the stack is empty, though?

	l := len(s)
	return s[:l-1], s[l-1]
}

// Probe data structure
type Probe struct {
	Rate         float64
	CurrentValue int
	PrevValue    int
}

func (probe *Probe) getRate(w http.ResponseWriter, r *http.Request) {
	if _, err := w.Write([]byte(fmt.Sprintf("%f\n", probe.Rate))); err != nil {
		panic("Can't write rate")
	}
}

func (probe *Probe) getCurrent(w http.ResponseWriter, r *http.Request) {
	if _, err := w.Write([]byte(fmt.Sprintf("%d\n", probe.CurrentValue))); err != nil {
		panic("Can't write current value")
	}
}

func main() {
	ipAddress := os.Args[1]
	// Run the sequence of rates
	// 1.25, 10, 2, 10, 5, 20
	s := make(stack, 0)
	s = s.Push(50)
	s = s.Push(200)
	s = s.Push(100)
	s = s.Push(500)
	s = s.Push(100)
	s = s.Push(800)
	s = s.Push(800) // This needs to be pushed twice
	s, TIMEOUT := s.Pop()
	requestProbe := &Probe{
		Rate:         1000.0 / float64(TIMEOUT),
		CurrentValue: 0,
		PrevValue:    0,
	}
	responseProbe := &Probe{
		// Assume server can handle line rate when starting
		Rate:         1000.0 / float64(TIMEOUT),
		CurrentValue: 0,
		PrevValue:    0,
	}
	ticker := time.NewTicker(5 * time.Second)
	ticker2 := time.NewTicker(1 * time.Second)

	go func() {
		http.HandleFunc("/requestRate", requestProbe.getRate)
		http.HandleFunc("/responseRate", responseProbe.getRate)
		http.HandleFunc("/numRequests", requestProbe.getCurrent)
		http.HandleFunc("/numResponses", responseProbe.getCurrent)
		log.Fatal(http.ListenAndServe(":5555", nil))
	}()

	fmt.Println("Waiting for client to start...")
	time.Sleep(time.Duration(5) * time.Second)
	fmt.Println("Client started")

	for {
		select {
		case <-ticker.C:
			if len(s) == 0 {
				ticker.Stop()
				ticker2.Stop()
				fmt.Println("Reqs - Resps = ", requestProbe.CurrentValue-responseProbe.CurrentValue)
				os.Exit(0)
			} else {
				s, TIMEOUT = s.Pop()
				fmt.Println("stack: ", s)
				fmt.Println("timeout: ", TIMEOUT)
				requestProbe.Rate = 1000.0 / float64(TIMEOUT)
				fmt.Println("rate: ", requestProbe.Rate)
			}
		case <-ticker2.C:
			responseProbe.Rate = float64(responseProbe.CurrentValue - responseProbe.PrevValue)
			responseProbe.PrevValue = responseProbe.CurrentValue
		case <-time.After(time.Duration(TIMEOUT) * time.Millisecond):
			go func() {
				requestProbe.CurrentValue++
				fmt.Println(" REQUESTS = ", requestProbe.CurrentValue)
				resp, err := http.Get(fmt.Sprintf("http://%s:4444/doWork", ipAddress))
				if err == nil {
                                        respBody, _ := ioutil.ReadAll(resp.Body)
				        fmt.Println("Response came after", string(respBody), "seconds")
                                }
				responseProbe.CurrentValue++
				fmt.Println(" RESPONSES = ", responseProbe.CurrentValue)
			}()
		}
	}
}
