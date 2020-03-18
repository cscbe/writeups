# Invisible Ink

## Description
Your friend sent you this message, but the letters make no sense and are all over the place!

## Solution
Spaces are before or after characters
If there's a space before, remove one from the ascii value, if there's a space after, add one to the ascii value

The spaces to the left of the letter are negative numbers
The spaces to the right of the letter are positive numbers
Add them together, then add the result to the ascii value of the letter.

The output is the flag.

The solution.py script automates this, or you can do it by hand.

