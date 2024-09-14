import subprocess

class OVNController:
    def create_network(self, tenant_id, network_name, subnet, enable_dhcp=False, dhcp_start_ip=None, dhcp_end_ip=None):
        # Create logical switch in OVN
        command = f"ovn-nbctl ls-add {tenant_id}-{network_name}"
        subprocess.run(command, shell=True)

        # Set subnet
        command_subnet = f"ovn-nbctl set Logical_Switch {tenant_id}-{network_name} other_config:subnet={subnet}"
        subprocess.run(command_subnet, shell=True)

        # Configure DHCP if enabled
        if enable_dhcp and dhcp_start_ip and dhcp_end_ip:
            dhcp_command = f"ovn-nbctl set DHCP_Options {tenant_id}-{network_name}-dhcp options:range={dhcp_start_ip}-{dhcp_end_ip} options:subnet={subnet}"
            subprocess.run(dhcp_command, shell=True)

        return f"{tenant_id}-{network_name}"

    def attach_network_to_router(self, router_name, network_name, gateway_ip=None):
        # Use the first IP in the subnet if gateway IP is not specified
        if not gateway_ip:
            subnet_info = subprocess.run(f"ovn-nbctl get Logical_Switch {network_name} other_config:subnet",
                                         shell=True, capture_output=True, text=True)
            subnet = subnet_info.stdout.strip().split('=')[1]
            gateway_ip = subnet.split('/')[0]  # First IP from subnet

        # Command to attach the network to the router
        command = f"ovn-nbctl lrp-add {router_name} {network_name}-port {gateway_ip}"
        subprocess.run(command, shell=True)

