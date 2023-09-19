import subprocess



subprocess.run(['sudo', 'apt', 'update'])
subprocess.run(['sudo', 'apt', 'upgrade', '-y'])
subprocess.run(['sudo', 'apt', 'install', '-y', 'wireguard-tools'])

subprocess.run(['sudo', 'modprobe', 'wireguard'])





private_key = subprocess.check_output(['wg', 'getkey']).decode().strip()
public_key = subprocess.check_output(['echo', '-n', private_key, '|', 'wg', 'pubkey']).decode().strip()








server_config = f"""
[Interface]
Address = 10.0.0.1/24
SaveConfig = true
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
ListenPort = 51820
PrivateKey = {private_key}

[Peer]
PublicKey = {public_key}
AllowedIPs = 10.0.0.2/32

"""
with open('/etc/wireguard/wg0.conf', 'w') as f:
    f.write(server_config)





subprocess.run(['sudo', 'systemctl', 'enable', 'wg-quick@wg0'])
subprocess.run(['sudo', 'systemctl', 'start', 'wg-quick@wg0'])



subprocess.run(['sudo', 'systemctl', 'status', 'wg-quick@wg0'])
