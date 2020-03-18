package main

import (
	"fmt"
	"math/rand"
	"os"
	"time"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Printf("Usage: %v 'flag{abcd}'", os.Args[0])
		return
	}

	runes := []rune(os.Args[1])

	zws := rune(' ')

	output := []rune{}

	rand.Seed(time.Now().UnixNano())

	for _, v := range runes {
		before := rand.Int() % 16
		after := rand.Int() % 16

		for i := 0; i < before; i++ {
			output = append(output, zws)
		}
		output = append(output, rune((int(v)+before)-after))
		for i := 0; i < after; i++ {
			output = append(output, zws)
		}
		output = append(output, '\n')
	}
	fmt.Println(string(output))

}
