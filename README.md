# Regina Web based network virtualization platform 
# Network Virtualization Platform

## Overview

This platform allows users to create and manage virtual networks, logical routers, and bind virtual machines (VMs) to networks. It integrates with **KVM** and **XCP-NG/Xen Orchestra** to provide fine-grained network control, including **DHCP** configuration, **floating IPs**, and advanced networking features.

## Features

- **Create Virtual Networks**: Users can create isolated virtual networks with custom subnets and DHCP configuration.
- **Attach Networks to Routers**: Route traffic between networks using logical routers.
- **VM Network Binding**: Automatically bind VM NICs to networks upon creation.
- **Future Features**: Load Balancers as a Service (LBaaS), VPN as a Service (VPNaaS), Floating IPs, and SNAT support.

## Installation Instructions

### Backend Setup (Flask)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/network-virtualization-platform.git
   cd network-virtualization-platform/backend

