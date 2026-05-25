#!/bin/sh

set -e

if [ $# -lt 3 ]; then
	    echo "Usage: $0 <username> \"summary\" \"message\""
	        exit 1
fi

_user="$1"
_summary="$2"
_message="$3"

# Get latest session file (most recent one)
DBUS_FILE=$(ls -t /home/"$_user"/.dbus/session-bus/ 2>/dev/null | head -n1)

if [ -z "$DBUS_FILE" ]; then
    echo "No DBus session file found for $_user"
    echo "Is the user logged into XFCE?"
    exit 1
fi

# Source the file to get DBUS_SESSION_BUS_ADDRESS (remove surrounding single quotes)
DBUS_ADDR=$(grep -m1 '^DBUS_SESSION_BUS_ADDRESS=' "/home/$_user/.dbus/session-bus/$DBUS_FILE" \
	| cut -d= -f2- \
	| sed "s/^'//;s/'$//")

if [ -z "$DBUS_ADDR" ]; then
    echo "Could not read DBUS_SESSION_BUS_ADDRESS from session file"
    exit 1
fi

DISPLAY=:0

echo "Sending notification to $_user..."
echo "Using DBUS: $DBUS_ADDR"

env -i \
    DISPLAY="$DISPLAY" \
    DBUS_SESSION_BUS_ADDRESS="$DBUS_ADDR" \
    HOME="/home/$_user" \
    USER="$_user" \
    su -m "$_user" -c "notify-send -u normal -i dialog-information \"$_summary\" \"$_message\""
