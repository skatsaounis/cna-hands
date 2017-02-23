package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os"
	"time"
)

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
	TIMEOUT := rand.Int() % 999
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
	quit := make(chan struct{})

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
			TIMEOUT = rand.Int() % 999
			requestProbe.Rate = 1000.0 / float64(TIMEOUT)
		case <-ticker2.C:
			responseProbe.Rate = float64(responseProbe.CurrentValue - responseProbe.PrevValue)
			responseProbe.PrevValue = responseProbe.CurrentValue
		case <-time.After(time.Duration(TIMEOUT) * time.Millisecond):
			go func() {
				requestProbe.CurrentValue++
				fmt.Println(" REQUESTS = ", requestProbe.CurrentValue)
				resp, _ := http.Get(fmt.Sprintf("http://%s:4444/doWork", ipAddress))
				respBody, _ := ioutil.ReadAll(resp.Body)
				fmt.Println("Response came after", string(respBody), "seconds")
				responseProbe.CurrentValue++
				fmt.Println(" RESPONSES = ", responseProbe.CurrentValue)
			}()
		case <-quit:
			ticker.Stop()
			return
		}
	}
}
