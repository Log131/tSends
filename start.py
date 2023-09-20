import subprocess



subprocess.run('wg', 'genkey', '|', 'tee', 'privatekey', '|', 'wg', 'pubkey' '>', 'publickey')






with open('/root/privatekey', 'r')as f:
    private_key = f.read().strip()

with open('/root/publickey', 'r') as files:
    public_key = files.read().strip()

server_config = f"""[Interface]
PrivateKey = {private_key}
Address = 10.0.0.2/32
DNS = 8.8.8.8

[Peer]
PublicKey = {public_key}
Endpoint = 45.129.3.8:51830
AllowedIPs = 0.0.0.0/0
"""



with open('/etc/wireguard/wg5.conf', 'w') as files_:
    files_.write(server_config)


subprocess.run(['sudo', 'systemctl', 'enable', 'wg-quick@wg5'])
subprocess.run(['sudo', 'systemctl', 'start', 'wg-quick@wg5'])



subprocess.run(['sudo', 'systemctl', 'status', 'wg-quick@wg5'])