# No Time

## Created by Toon Swyzen

## Description
I asked my cousin to go bowling, but he keeps telling me he has no time!

I think he's working on this secret website, can you try to log in and see what he's up to?


## Solution
A timing attack can be used against the login field to figure out the correct pincode. First, figure out the length of the pin by increasing the size until the backend no longer indicates that the pin is too short.

Next, the pin can be brute-forced by enumerating the first digit from 0 to 9 and evaluating the response times. For one of the digits, the response time will be higher than the other ones. This indicates that that number is the correct first position. Once you know the first digit, enumerate the second digit, etc.

An example can be seen in solution.py.