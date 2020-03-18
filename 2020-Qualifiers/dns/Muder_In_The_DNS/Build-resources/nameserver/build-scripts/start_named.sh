#!/bin/bash

exec nohup /usr/sbin/named -f -u named -c /etc/named.conf 
