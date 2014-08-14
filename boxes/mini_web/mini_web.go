package main

import (
	"encoding/json"
	"fmt"
	"github.com/hoisie/web"
	"time"
)

func hello(val string) string {
	type Message struct {
		Name string
		Time string
	}

	m := Message{
		"Hello 中文 Success " + val,
		time.Now().Format("2006-01-02 03:04:05"),
	}

	byteArray, _ := json.Marshal(m)

	return string(byteArray[:]) // bytes to string
}

func main() {
	y := 1.5
	fmt.Println(int(y))

	web.Get("/hello/(.*)/", hello)
	web.Run("0.0.0.0:9998")

}
