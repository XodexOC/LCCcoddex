# [08] Networking
> **Track:** Linux · **Level:** 08 · **Difficulty:** ★★☆☆☆

## 1. Problem we're running

Linux systems are rarely isolated. They connect to the internet, to each other, to databases, APIs, and services. You need to know: what's my IP address? Is a remote server reachable? How do I download a file? How do I SSH into another machine? How do I check which ports are listening?

## 2. Core concept (absolute zero)

### Network interfaces

A **network interface** is how the system connects to a network. Common types:

- `eth0`, `enp0s3` — wired Ethernet
- `wlan0`, `wlp2s0` — wireless Wi-Fi
- `lo` — loopback (127.0.0.1, the machine talking to itself)

### IP addresses

- **IPv4**: `192.168.1.10` (32-bit, most common)
- **IPv6**: `fe80::1` (128-bit, newer)
- **Private IPs**: `10.x.x.x`, `172.16-31.x.x`, `192.168.x.x`
- **Public IP**: globally routable, unique on the internet
- **127.0.0.1**: localhost — the machine itself

### Ports

A port is like a door on a computer. Services listen on specific ports:

| Port | Protocol | Service |
|------|----------|---------|
| 22 | TCP | SSH |
| 80 | TCP | HTTP |
| 443 | TCP | HTTPS |
| 53 | TCP/UDP | DNS |
| 3306 | TCP | MySQL |
| 5432 | TCP | PostgreSQL |

### DNS

DNS (Domain Name System) translates hostnames like `google.com` to IP addresses like `142.250.185.78`.

## 3. Step-by-step breakdown (examples)

### `ip addr` — show IP addresses

Modern tool for network configuration:

```
alice@xodex:~$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default
    link/ether 08:00:27:ab:cd:ef brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic enp0s3
       valid_lft 85782sec preferred_lft 85782sec
    inet6 fe80::a00:27ff:feab:cdef/64 scope link
       valid_lft forever preferred_lft forever
```

- `lo` is loopback (127.0.0.1)
- `enp0s3` has IP `192.168.1.100/24`

### `ip link` — show/handle network interfaces

```
alice@xodex:~$ ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 ...
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ...
```

### `ip route` — show routing table

```
alice@xodex:~$ ip route
default via 192.168.1.1 dev enp0s3
192.168.1.0/24 dev enp0s3 proto kernel scope link src 192.168.1.100
```

- **default via 192.168.1.1** — the gateway (your router)
- **192.168.1.0/24** — directly connected network

### Legacy tools: `ifconfig`, `route`, `netstat`

These are older but still widely used. Install with `sudo apt install net-tools`.

```
alice@xodex:~$ ifconfig
enp0s3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
        ...

alice@xodex:~$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    enp0s3
192.168.1.0     0.0.0.0         255.255.255.0   U     enp0s3
```

### `ping` — test reachability

`ping` sends ICMP echo requests and measures response time:

```
alice@xodex:~$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=12.3 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=11.8 ms
^C
--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 11.8/12.05/12.3/0.250 ms
```

Ping by hostname:

```
alice@xodex:~$ ping google.com
```

Press `Ctrl+C` to stop. Use `-c count` for a fixed number:

```
alice@xodex:~$ ping -c 4 google.com
```

### DNS resolution: `/etc/resolv.conf`

```
alice@xodex:~$ cat /etc/resolv.conf
nameserver 192.168.1.1
nameserver 8.8.8.8
```

This file tells the system which DNS servers to use.

### `curl` — transfer data from/to URLs

`curl` is the Swiss Army knife of HTTP (and many other protocols):

```
alice@xodex:~$ curl https://example.com
<!doctype html>
<html>
<head>
    <title>Example Domain</title>
...
```

Save output to a file:

```
alice@xodex:~$ curl -o page.html https://example.com
```

Show response headers with `-v` (verbose) or `-I` (headers only):

```
alice@xodex:~$ curl -I https://google.com
HTTP/2 200
content-type: text/html; charset=ISO-8859-1
...

alice@xodex:~$ curl -v https://google.com
*   Trying 142.250.185.78:443...
* Connected to google.com (142.250.185.78) port 443 (#0)
* TLS 1.3 connection using TLS_AES_256_GCM_SHA384
...
```

Post data:

```
alice@xodex:~$ curl -X POST -d "name=alice&age=25" https://httpbin.org/post
```

Download a file:

```
alice@xodex:~$ curl -O https://example.com/file.zip
```

### `wget` — download files

`wget` is simpler than `curl` for basic downloads:

```
alice@xodex:~$ wget https://example.com/file.zip
--2026-01-15 10:00:01--  https://example.com/file.zip
Resolving example.com... 93.184.216.34
Connecting to example.com|93.184.216.34|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1234567 (1.2M) [application/zip]
Saving to: 'file.zip'
100%[======================================>] 1,234,567  1.2MB/s  in 0.1s

2026-01-15 10:00:02 (12.3 MB/s) - 'file.zip' saved [1234567/1234567]
```

Recursive download (mirror a website):

```
alice@xodex:~$ wget -r -l 2 https://example.com
```

### `ssh` — secure shell

SSH lets you log into a remote machine:

```
alice@xodex:~$ ssh alice@192.168.1.50
The authenticity of host '192.168.1.50 (192.168.1.50)' can't be established.
ED25519 key fingerprint is SHA256:...
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
alice@192.168.1.50's password:
```

Once authenticated, you get a shell on the remote machine.

#### SSH key authentication (passwordless login)

Generate a key pair:

```
alice@xodex:~$ ssh-keygen -t ed25519
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/alice/.ssh/id_ed25519):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/alice/.ssh/id_ed25519
Your public key has been saved in /home/alice/.ssh/id_ed25519.pub
```

Copy the public key to the remote server:

```
alice@xodex:~$ ssh-copy-id alice@192.168.1.50
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s)
alice@192.168.1.50's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'alice@192.168.1.50'"
```

Now you can SSH without a password:

```
alice@xodex:~$ ssh alice@192.168.1.50
```

### `scp` — secure copy

Copy files over SSH:

```
alice@xodex:~$ scp file.txt alice@192.168.1.50:/home/alice/
```

Copy from remote to local:

```
alice@xodex:~$ scp alice@192.168.1.50:/home/alice/remote-file.txt .
```

Copy entire directories with `-r`:

```
alice@xodex:~$ scp -r project/ alice@192.168.1.50:/home/alice/
```

### Network troubleshooting: `ss` and `netstat`

List listening sockets (services waiting for connections):

```
alice@xodex:~$ ss -tuln
Netid  State   Recv-Q  Send-Q  Local Address:Port   Peer Address:Port
tcp    LISTEN  0       128     0.0.0.0:22            0.0.0.0:*
tcp    LISTEN  0       128     127.0.0.1:3306        0.0.0.0:*
udp    LISTEN  0       10      0.0.0.0:53            0.0.0.0:*
```

- `-t` TCP, `-u` UDP
- `-l` listening only
- `-n` numeric (don't resolve service names)
- `-p` show process (needs `sudo`)

Old tool `netstat` (same info, different command):

```
alice@xodex:~$ netstat -tuln
```

### Checking connectivity

A typical troubleshooting workflow:

```
# 1. Check IP config
alice@xodex:~$ ip addr

# 2. Can I reach the gateway?
alice@xodex:~$ ping -c 1 192.168.1.1

# 3. Can I reach the internet?
alice@xodex:~$ ping -c 1 8.8.8.8

# 4. Does DNS work?
alice@xodex:~$ nslookup google.com

# 5. Can I connect to a specific port?
alice@xodex:~$ curl -v http://192.168.1.50:8080

# 6. Is my web server listening?
alice@xodex:~$ ss -tuln | grep 80
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| `ping google.com` without checking DNS first | If DNS fails, ping may show "unknown host" | Check `/etc/resolv.conf` and try `ping 8.8.8.8` first |
| Using `ifconfig` on modern systems | Not installed by default, deprecated | Use `ip addr` |
| `curl` without `-O` | Output goes to terminal, doesn't save file | `curl -O URL` or `curl -o filename URL` |
| SSH with password instead of key | Less secure, can be brute-forced | Use `ssh-keygen` + `ssh-copy-id` |
| `ss` without `sudo` | May not show process names | `sudo ss -tulnp` |
| Forgetting `scp -r` for directories | `scp` skips directories without `-r` | `scp -r mydir/ user@host:/path/` |
| Opening ports without a firewall | Exposes services to the internet | Use `ufw` or `iptables` to restrict access |

## 5. Exercises

1. Run `ip addr`. What is your IP address? What interface is it on?
2. Check your routing table: `ip route`. What is your default gateway?
3. Ping your gateway: `ping -c 4 192.168.1.1` (use your gateway IP). What's the average latency?
4. Ping `8.8.8.8`. Then ping `google.com`. If one fails, why?
5. Use `curl -I https://example.com`. What web server is it running?
6. Download a file with `wget`.
7. Generate an SSH key pair with `ssh-keygen -t ed25519`.
8. List listening ports on your system: `sudo ss -tuln`. What services are listening?
9. Check DNS resolution: `cat /etc/resolv.conf`.
10. Use `curl -v` to see the full HTTP conversation with a website.
11. Use `scp` to copy a file to `/tmp` on localhost: `scp test.txt localhost:/tmp/`.
12. Trace the route to `google.com`: `traceroute google.com` (install with `sudo apt install traceroute`).

## 6. Self-check questions

1. What is the difference between `ip addr` and `ip link`?
2. What does `ping 127.0.0.1` test?
3. How do you download a file from the internet using the terminal?
4. What is the purpose of SSH keys?
5. How do you check which ports are listening on your system?
6. What's the difference between `curl` and `wget`?
7. How do you copy a file from a remote server to your local machine?
8. What does `/etc/resolv.conf` contain?
9. How do you find your default gateway?
10. What is the loopback interface and what IP does it use?

## 7. What's next

You can connect, transfer files, and troubleshoot networking. In **Level 09**, you'll level up to **shell scripting** — writing reusable bash scripts with variables, conditionals, loops, functions, and exit codes.
