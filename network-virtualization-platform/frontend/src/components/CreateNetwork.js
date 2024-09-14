import React, { useState } from 'react';
import axios from 'axios';

function CreateNetwork() {
  const [networkName, setNetworkName] = useState('');
  const [subnet, setSubnet] = useState('');
  const [enableDHCP, setEnableDHCP] = useState(false);
  const [dhcpStartIp, setDhcpStartIp] = useState('');
  const [dhcpEndIp, setDhcpEndIp] = useState('');

  const handleSubmit = () => {
    axios.post('/create_network', {
      network_name: networkName,
      subnet: subnet,
      enable_dhcp: enableDHCP,
      dhcp_start_ip: dhcpStartIp,
      dhcp_end_ip: dhcpEndIp
    }).then(response => {
      alert('Network Created: ' + response.data.network_id);
    });
  };

  return (
    <div>
      <h3>Create New Network</h3>
      <input
        type="text"
        value={networkName}
        onChange={(e) => setNetworkName(e.target.value)}
        placeholder="Network Name"
      />
      <input
        type="text"
        value={subnet}
        onChange={(e) => setSubnet(e.target.value)}
        placeholder="Subnet (e.g., 192.168.1.0/24)"
      />
      <label>
        <input
          type="checkbox"
          checked={enableDHCP}
          onChange={(e) => setEnableDHCP(e.target.checked)}
        />
        Enable DHCP
      </label>
      {enableDHCP && (
        <>
          <input
            type="text"
            value={dhcpStartIp}
            onChange={(e) => setDhcpStartIp(e.target.value)}
            placeholder="DHCP Start IP"
          />
          <input
            type="text"
            value={dhcpEndIp}
            onChange={(e) => setDhcpEndIp(e.target.value)}
            placeholder="DHCP End IP"
          />
        </>
      )}
      <button onClick={handleSubmit}>Create Network</button>
    </div>
  );
}

export default CreateNetwork;
