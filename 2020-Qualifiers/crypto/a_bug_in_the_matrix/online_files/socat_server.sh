#!/bin/sh

socat TCP4-LISTEN:5555,reuseaddr,fork EXEC:"./Challenge",pty,ctty,stderr,echo=0

