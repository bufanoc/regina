# Network Virtualization Platform – Future Features

## 1. Load Balancers as a Service (LBaaS)
- Implement load balancing services for virtual machines connected to tenant networks.
- User-defined load balancer configurations (round-robin, least connections, etc.)

## 2. VPN as a Service (VPNaaS)
- Provide VPN services to users for connecting external resources securely to their virtual networks.
- Support IPsec, SSL VPN, and OpenVPN.

## 3. Virtual Tunnel Endpoints (VTEPs)
- Enable cross-hypervisor or cross-datacenter communication using VTEPs to tunnel traffic between OVN instances.

## 4. Floating IPs and SNAT
- Implement support for floating IPs, allowing public IPs to be mapped to private VM addresses using SNAT.
- Dynamic IP allocation from a shared IP pool for external access.

