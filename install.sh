#!/bin/bash
mkdir /etc/assisht
cp ht.py /usr/local/bin
chmod +x /usr/local/bin/ht.py
mv /usr/local/bin/ht.py /usr/local/bin/ht
echo 'assisht: config files ready'
