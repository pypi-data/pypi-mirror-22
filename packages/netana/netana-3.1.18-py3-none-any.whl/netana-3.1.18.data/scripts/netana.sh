#! /bin/sh

echo "You must be in a virt-dir!"
pkgloc="lib/python3.5/site-packages/netana"

echo "Starting Netana."
echo "Package location is: $(pkgloc)"
python $(pkgloc)/startnetana.py

echo "Good Bye - Exiting Netana!"
exit 0
