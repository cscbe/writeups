package main

import (
	"fmt"
	"math/rand"
	"os"
	"text/scanner"
	"time"
)

var oracle = map[rune]string{
	'A': "NBVCXZAQWERTYD",
	'B': "NBVCXZAWDRTH",
	'C': "THBVCXAW",
	'D': "NBVCXZAWERTH",
	'E': "QAZXCDVBNHY",
	'F': "QAZXCDVBN",
	'G': "QAZXCVBNHYTR",
	'H': "QWERTYDZXCVBN",
	'I': "QAZSDFGNHY",
	'J': "ZXCVBHTR",
	'K': "ZXCVBNGYR",
	'L': "ZXCVBNHY",
	'M': "123456WSZXCVBN",
	'N': "123456ESZXCVBN",
	'O': "WERTHBVCXA",
	'P': "QWEAFZXCVBN",
	'Q': "WERYAGXCV",
	'R': "QWETYAFZXCVBN",
	'S': "QAZXCDERTYHNB",
	'T': "QAZSDFGH",
	'U': "ZXCVBHTREWQ",
	'V': "ZXCVGHREWQ",
	'W': "ZXCVBNGQWERTY",
	'X': "ZXDFBNQWTY",
	'Y': "QWZXDFGH",
	'Z': "ZAQWDFBNHY",
	'{': "QXCVBH",
	'}': "WSDFGN",
	'_': "NHY",
}

func main() {

	rand.Seed(time.Now().UTC().UnixNano())
	fullstring := ""
	for _, chr := range os.Args[1] {
		if pattern, ok := oracle[chr]; ok {
			fullstring = fullstring + shuffle(pattern) + "\n"
		} else {
			fmt.Println("Did not receive a valid string as input. Only ABCDEFGHIJKLMNOPQRSTUVWXYZ{}_ are allowed.")
		}
	}
	fmt.Println(fullstring)
}

func shuffle(str string) string {
	tokens := []rune(str)

	var result []string

	for _, char := range tokens {
		result = append(result, scanner.TokenString(char))
	}
	final := make([]rune, len(tokens))
	perm := rand.Perm(len(tokens))

	for i, v := range perm {
		final[v] = tokens[i]
	}
	return string(final)
}
