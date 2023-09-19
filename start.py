import subprocess



subprocess.run(['sudo', 'apt', 'update'])
subprocess.run(['sudo', 'apt', 'upgrade', '-y'])
subprocess.run(['sudo', 'apt', 'install', '-y', 'wireguard'])

subprocess.run(['sudo', 'wg', 'genkey', '|', 'tee', '/etc/wireguard/privatekey'])
subprocess.run(['sudo', 'wg', 'pubkey', '|', 'tee', '/etc/wireguard/privatekey', '|', 'wg', 'pubkey', '|', 'tee', 'etc/wireguard/publickey'])


subprocess.run(['echo', 'net.ipv4.ip_forward=1', '>>', '/etc/sysctl.conf'])

subprocess.run(['sysctl', '-p'])
subprocess.run(['sudo', 'wg', 'genkey', '|', 'tee', '/etc/wireguard/qwe', '|', 'wg', 'pubkey', '|', 'tee', '/etc/wireguard/qwe'])








with open('/etc/wireguard/qwe', 'r')as f:
    pub_key = f.read().strip()

with open('/etc/wireguard/publickey', 'r') as files:
    private_key = files.read().strip()

server_config = f"""[Interface]
PrivateKey = {private_key}
Address = 10.0.0.2/32
DNS = 8.8.8.8

[Peer]
PublicKey = {pub_key}
Endpoint = server:51830
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 20
"""






subprocess.run(['sudo', 'systemctl', 'enable', 'wg-quick@wg0'])
subprocess.run(['sudo', 'systemctl', 'start', 'wg-quick@wg0'])



subprocess.run(['sudo', 'systemctl', 'status', 'wg-quick@wg0'])