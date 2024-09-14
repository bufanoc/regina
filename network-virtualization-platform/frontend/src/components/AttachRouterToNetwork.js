import React, { useState } from 'react';
import axios from 'axios';

function AttachRouterToNetwork({ routerId, networkId }) {
  const [gatewayIp, setGatewayIp] = useState('');

  const handleAttach = () => {
    axios.post(`/attach_network_to_router`, {
      network_name: networkId,
      router_name: routerId,
      gateway_ip: gatewayIp
    }).then(response => {
      alert('Network attached to Router');
    });
  };

  return (
    <div>
      <h3>Attach Network to Router</h3>
      <input
        type="text"
        value={gatewayIp}
        onChange={(e) => setGatewayIp(e.target.value)}
        placeholder="Gateway IP (Optional)"
      />
      <button onClick={handleAttach}>Attach Network</button>
    </div>
  );
}

export default AttachRouterToNetwork;
