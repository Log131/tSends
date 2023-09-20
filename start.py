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


[Peer]
PublicKey = {s}
AllowedIPs = 10.0.0.2/3


"""



with open('/etc/wireguard/wg5.conf', 'w') as files_:
    files_.write(server_config)


subprocess.run(['sudo', 'systemctl', 'enable', 'wg-quick@wg5.service'])
subprocess.run(['sudo', 'systemctl', 'start', 'wg-quick@wg5.service'])



subprocess.run(['sudo', 'systemctl', 'status', 'wg-quick@wg5.service'])


with open('/root/publickey', 'r') as files:
    s_ = files.read()




with open('/root/private_key', 'r') as files_:
    s_5 = files.read()

pub_config = f""""[Interface]
PrivateKey = {s_5}
Address = 10.0.0.2/32
DNS = 8.8.8.8

[Peer]
PublicKey = {s_}
Endpoint = 45.129.3.8:51830
AllowedIPs = 0.0.0.0/0
"""

with open('/root/tsends/qwe.conf', 'w') as files_5:
    files_5.write(pub_config)