#!/bin/bash
GUEST_NAME=$1
EVENT=$2

if [ "$EVENT" == "start" ]; then
    # Fetch VM MAC address using virsh
    MAC_ADDR=$(virsh dumpxml "$GUEST_NAME" | grep "mac address" | sed "s/.*'\(.*\)'.*/\1/")
    
    # Send details to web interface for network binding
    curl -X POST http://<web-interface-ip>:<web-interface-port>/vm_event \
         -H "Content-Type: application/json" \
         -d "{\"vm_name\":\"$GUEST_NAME\", \"mac_address\":\"$MAC_ADDR\"}"
fi

