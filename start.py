import subprocess









with open('/root/privatekey', 'r')as f:
    private_key = f.read().strip()


with open('root/pub_key', 'r')as f_:
    s = f_.read()








server_config = f"""[Interface]
PrivateKey = {private_key}
Address = 10.0.0.1/32
ListenPort = 51830





PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

PublicKey = {s}
AllowedIPs = 10.0.0.2/32

"""



with open('/etc/wireguard/wg5.conf', 'w') as files_:
    files_.write(server_config)


subprocess.run(['sudo', 'systemctl', 'enable', 'wg-quick@wg5.service'])
subprocess.run(['sudo', 'systemctl', 'start', 'wg-quick@wg5.service'])



subprocess.run(['sudo', 'systemctl', 'status', 'wg-quick@wg5.service'])



