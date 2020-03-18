#!/bin/bash

echo "minrate=1" >> /etc/yum.conf
echo "timeout=300" >> /etc/yum.conf
yum -y install net-tools epel-release less bind bind-utils
