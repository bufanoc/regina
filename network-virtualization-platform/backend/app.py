from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import subprocess

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models for User, Network, Router (see models.py)
from models import User, Network, Router

# Load user for login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Admin creates user accounts
@app.route('/admin/create_user', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        return jsonify({'error': 'Not authorized'}), 403
    
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': f'User {data["username"]} created'}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

# Create Network with Subnet and DHCP options
@app.route('/create_network', methods=['POST'])
@login_required
def create_network():
    data = request.json
    network_name = data['network_name']
    subnet = data['subnet']
    enable_dhcp = data.get('enable_dhcp', False)
    dhcp_start_ip = data.get('dhcp_start_ip')
    dhcp_end_ip = data.get('dhcp_end_ip')

    # Create the network in OVN
    ovn_controller = OVNController()
    network_id = ovn_controller.create_network(current_user.id, network_name, subnet, enable_dhcp, dhcp_start_ip, dhcp_end_ip)

    # Save to database
    network = Network(tenant_id=current_user.id, name=network_name, subnet=subnet, dhcp_enabled=enable_dhcp, dhcp_start_ip=dhcp_start_ip, dhcp_end_ip=dhcp_end_ip)
    db.session.add(network)
    db.session.commit()

    return jsonify({"network_id": network_id}), 201

# Attach Network to Router
@app.route('/attach_network_to_router', methods=['POST'])
@login_required
def attach_network_to_router():
    data = request.json
    network_name = data['network_name']
    router_name = data['router_name']
    gateway_ip = data.get('gateway_ip')

    ovn_controller = OVNController()
    ovn_controller.attach_network_to_router(router_name, network_name, gateway_ip)

    return jsonify({'message': f'Network {network_name} attached to router {router_name}'}), 200

# API to receive VM events (from KVM or XCP-NG)
@app.route('/vm_event', methods=['POST'])
def vm_event():
    data = request.json
    vm_name = data['vm_name']
    mac_address = data['mac_address']

    # Find user's network configuration (placeholder)
    network_name = find_user_network_for_vm(vm_name)

    # Bind the VM's NIC to the correct network
    attach_nic_to_ovs_switch(vm_name, mac_address, network_name)

    return jsonify({"message": "NIC attached to network"}), 200

def attach_nic_to_ovs_switch(vm_name, mac_address, network_name):
    command = f"ovn-nbctl lsp-add {network_name} {vm_name}-port -- lsp-set-addresses {vm_name}-port {mac_address}"
    subprocess.run(command, shell=True)

if __name__ == '__main__':
    app.run(debug=True)

