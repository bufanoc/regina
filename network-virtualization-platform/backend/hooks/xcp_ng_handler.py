from XenAPI import Session
import requests

# XCP-NG/XenServer API connection
session = Session('http://xcp-ng-ip')
session.xenapi.login_with_password('username', 'password')

# Fetch VM details and send to web interface
def on_vm_event(event):
    if event['operation'] == 'add' or event['operation'] == 'mod':
        vm_uuid = event['ref']
        mac_address = session.xenapi.VM.get_MAC(vm_uuid)
        vm_name = session.xenapi.VM.get_name_label(vm_uuid)

        # Send VM details to web interface
        requests.post("http://<web-interface-ip>:<web-interface-port>/vm_event", json={
            "vm_name": vm_name,
            "mac_address": mac_address
        })

