package main

import (
	"fmt"
	"math/rand"
	"os"
	"regexp"
)

// This challenge is based around either research or decoding, the fact that we're using Whirl is
// mostly an excuse to confuse people into thinking the file is binary.
// Here is an explaination of the logic (roughly)
/*
For all chars in the passed string
  Clear the MathWheel's register
  Write 1 into the MathWheel's register
  Write the MathWheel's register into the currently selected memory address
  Add 1 to the MathWheel's register as many times as the ascii value of the character
  Store the result into the currently targetted memory address
  Output the letter
*/

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: " + os.Args[0] + " source")
		return
	}

	output := ""

	for i := 0; i < len(os.Args[1]); i++ {
		// Load Zero into the MathWheel's register
		output = output + "00" + randomNoop() + "1111" + randomNoop() + "110000"
		// Turn the zero into a one
		output = output + "11" + randomNoop() + "110000"
		// Store the one into the memory slot
		output = output + "1111" + randomNoop() + "0000"
		// Select the "add" instruction
		output = output + "1"
		for j := 0; j < int(os.Args[1][i])-1; j++ {
			// Add one to the MathWheel's register
			output = output + "00" + randomNoop() + "00" + randomNoop()
		}
		// Go back to a neutral position
		output = output + "1111" + randomNoop() + "1111" + randomNoop() + "100"

		// Store the result of the addition to the first memory slot
		output = output + "00110000" + randomNoop() + "11111" + randomNoop() + "1111100"
		// Write one to the OpWheel's register to make AscIO output the character
		output = output + "1100" + randomNoop() + "00"
		// Output the character in the first memory slot
		output = output + "1111" + randomNoop() + "1111100001"
	}
	// Quit program
	output = output + "10000"

	// Align to nearest nybble to mask as binary
	output = output + "010110111101"[0:8-(len(output)%8)]

	// Format as a binary viewer would do, in groups of 8, 4 groups per line
	split := regexp.MustCompile("(........)")
	output = split.ReplaceAllString(output, "$1 ")
	align := regexp.MustCompile("(.*? .*? .*? .*?) ")
	output = align.ReplaceAllString(output, "$1\n")

	fmt.Print(output)
}

func randomNoop() string {
	noops := []string{
		"111010110111111011",
		"11010110111101",
		"101101",
		"",
		"",
	}
	// If you want to turn this challenge into a decoding challenge,
	// instead of a research challenge, uncomment this line
	// return ""
	return noops[rand.Intn(len(noops))]
}
