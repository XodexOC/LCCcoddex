# [07] Packages
> **Track:** Linux · **Level:** 07 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

Installing software on Linux isn't like Windows or Mac where you download an `.exe` from a website. Linux has **package managers** — centralized tools that handle installing, updating, configuring, and removing software, along with all its dependencies. Without a package manager, you'd need to manually find, download, and compile every program and its libraries.

## 2. Core concept (absolute zero)

### What is a package manager?

A **package manager** is a tool that automates:
- Installing software from repositories
- Resolving dependencies (libraries that software needs)
- Updating all installed software
- Removing software cleanly

### What is a package?

A **package** is a compressed archive containing a program, its configuration, metadata, and installation scripts. On Debian/Ubuntu systems, packages have the `.deb` extension.

### APT (Advanced Package Tool)

APT is the package manager used on Debian, Ubuntu, and their derivatives. It works with `.deb` packages and pulls them from **repositories**.

### Repositories

A **repository** is a server containing thousands of packages. APT downloads package lists from repositories and lets you search, install, and update.

Repository sources are listed in:

```
/etc/apt/sources.list
/etc/apt/sources.list.d/*.list
```

Example entry:

```
deb http://deb.debian.org/debian bookworm main contrib non-free
```

### Key commands

| Task | Command |
|------|---------|
| Update package list | `apt update` |
| Upgrade all packages | `apt upgrade` |
| Install a package | `apt install package` |
| Remove a package | `apt remove package` |
| Remove package + config | `apt purge package` |
| Search for a package | `apt search keyword` |
| Show package info | `apt show package` |
| List installed packages | `apt list --installed` |
| Fix broken dependencies | `apt --fix-broken install` |

## 3. Step-by-step breakdown (examples)

### `apt update` — refresh package index

Always run this before installing anything. It downloads the latest package list from repositories:

```
alice@xodex:~$ sudo apt update
Hit:1 http://deb.debian.org/debian bookworm InRelease
Get:2 http://security.debian.org bookworm-security InRelease [48.4 kB]
Get:3 http://deb.debian.org/debian bookworm-updates InRelease [52.0 kB]
...
Reading package lists... Done
```

### `apt upgrade` — upgrade all packages

Upgrades all installed packages to their latest versions:

```
alice@xodex:~$ sudo apt upgrade
Reading package lists... Done
Building dependency tree... Done
Calculating upgrade... Done
The following packages will be upgraded:
  curl libcurl4 openssl
3 upgraded, 0 newly installed, 0 to remove, 0 not upgraded.
Need to get 1,245 kB of archives.
After this operation, 16.4 kB disk space will be freed.
Do you want to continue? [Y/n] y
```

### `apt install` — install a package

```
alice@xodex:~$ sudo apt install htop
Reading package lists... Done
Building dependency tree... Done
The following NEW packages will be installed:
  htop libnl-3-200 libnl-genl-3-200
0 upgraded, 3 newly installed, 0 to remove, 0 not upgraded.
Need to get 189 kB of archives.
After this operation, 567 kB of additional disk space will be used.
Do you want to continue? [Y/n] y
```

APT automatically installs all dependencies (like `libnl-3-200`).

Install multiple packages at once:

```
alice@xodex:~$ sudo apt install git curl vim tree
```

### `apt remove` and `apt purge`

Remove a package (leaves config files):

```
alice@xodex:~$ sudo apt remove htop
```

Remove package and its configuration files:

```
alice@xodex:~$ sudo apt purge htop
```

### `apt search` — find packages

```
alice@xodex:~$ apt search "text editor"
Sorting... Done
Full Text Search... Done
vim/focal 2:8.1.2269-1ubuntu5 amd64
  Vi IMproved - enhanced vi editor

nano/focal 4.8-1ubuntu1 amd64
  small, friendly text editor inspired by Pico

gedit/focal 3.36.2-0ubuntu1 amd64
  official text editor of the GNOME desktop environment
```

### `apt show` — package details

```
alice@xodex:~$ apt show htop
Package: htop
Version: 3.0.5-6
Priority: optional
Section: utils
Maintainer: Jonathan Carter <jcc@debian.org>
Installed-Size: 276 kB
Depends: libc6 (>= 2.29), libncursesw6 (>= 6), libnl-3-200 (>= 3.2.7), ...
Homepage: https://htop.dev/
Description: interactive process viewer
 htop is an interactive process viewer for Linux that aims to be a
 better alternative to top.
```

### `apt list` — list packages

All installed packages:

```
alice@xodex:~$ apt list --installed | head -10
Listing... Done
adduser/stable 3.118 all
apt/stable 2.2.4 amd64
base-files/stable 12.4 amd64
base-passwd/stable 3.5.52 amd64
bash/stable 5.1-2 amd64
```

Upgradable packages:

```
alice@xodex:~$ apt list --upgradable
```

### `dpkg` — low-level package tool

APT uses `dpkg` underneath. You can use `dpkg` directly for specific tasks:

List installed packages:

```
alice@xodex:~$ dpkg -l | head -10
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name           Version      Architecture Description
+++-==============-============-============-=================================
ii  adduser        3.118        all          add and remove users and groups
ii  apt            2.2.4        amd64        commandline package manager
```

Check if a package is installed:

```
alice@xodex:~$ dpkg -l | grep htop
```

Install a `.deb` file:

```
alice@xodex:~$ sudo dpkg -i some-package.deb
```

Remove a package:

```
alice@xodex:~$ sudo dpkg -r htop
```

Show files owned by a package:

```
alice@xodex:~$ dpkg -L htop
/.
/usr
/usr/bin
/usr/bin/htop
/usr/share
/usr/share/doc
/usr/share/doc/htop
...
```

Find which package owns a file:

```
alice@xodex:~$ dpkg -S /bin/ls
coreutils: /bin/ls
```

### What is a `.deb` file?

A `.deb` is a Debian software package. It's an archive (ar format) containing:

```
control.tar.gz   — metadata (name, version, dependencies)
data.tar.gz      — the actual files to install
debian-binary    — version number
```

### Installing a `.deb` manually

Sometimes software isn't in the repository. You download a `.deb` and install:

```
alice@xodex:~$ wget https://example.com/package.deb
alice@xodex:~$ sudo dpkg -i package.deb
```

If there are missing dependencies, fix them with:

```
alice@xodex:~$ sudo apt --fix-broken install
```

### Adding repositories

To add a third-party repository (e.g., for Docker):

```
alice@xodex:~$ echo "deb [arch=amd64] https://download.docker.com/linux/debian bookworm stable" | sudo tee /etc/apt/sources.list.d/docker.list
alice@xodex:~$ sudo apt update
alice@xodex:~$ sudo apt install docker-ce
```

Many third-party repos require a GPG key:

```
alice@xodex:~$ curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

### `apt-get` vs `apt`

`apt-get` is the older command. `apt` is newer and more user-friendly (color output, progress bar). Both work; `apt` is recommended for interactive use.

| apt command | apt-get equivalent |
|-------------|-------------------|
| `apt install` | `apt-get install` |
| `apt remove` | `apt-get remove` |
| `apt update` | `apt-get update` |
| `apt upgrade` | `apt-get upgrade` |
| `apt search` | `apt-cache search` |
| `apt show` | `apt-cache show` |

### Full update workflow

```
alice@xodex:~$ sudo apt update          # refresh package lists
alice@xodex:~$ sudo apt upgrade         # upgrade all packages
alice@xodex:~$ sudo apt autoremove      # remove orphaned dependencies
alice@xodex:~$ sudo apt autoclean       # clean up downloaded .deb cache
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| Forgetting `sudo` with `apt install` | Only root can install system-wide packages | `sudo apt install package` |
| Running `apt upgrade` without `apt update` | Upgrades from stale package list | `sudo apt update && sudo apt upgrade` |
| `apt install package.deb` | `apt` doesn't install local `.deb` files | `sudo dpkg -i package.deb` |
| `sudo apt remove` thinking it removes config | `remove` keeps config files; use `purge` | `sudo apt purge package` |
| Adding random PPAs/repos | Security risk, can break your system | Only add repos you trust from official sources |
| `apt autoremove` without checking what it will remove | May remove packages you actually want | Review the list before confirming (`-s` to simulate) |

## 5. Exercises

1. Run `sudo apt update`. What happens?
2. Search for a package with `apt search "web server"`.
3. Show details of the `curl` package: `apt show curl`.
4. Install the `tree` package: `sudo apt install tree`.
5. Run `tree` on your home directory to see the directory tree.
6. List all installed packages: `apt list --installed | wc -l`. How many do you have?
7. Find which package owns the `/bin/cp` file using `dpkg -S`.
8. List all files owned by the `tree` package: `dpkg -L tree`.
9. Remove the `tree` package: `sudo apt remove tree`.
10. Check `dpkg -l | grep tree` to confirm removal.
11. If you have a `.deb` file, practice installing with `dpkg -i`.
12. Add the `buster-backports` repository to your sources.list and update.

## 6. Self-check questions

1. What is the difference between `apt update` and `apt upgrade`?
2. What does `sudo apt install` do that `dpkg -i` doesn't?
3. How do you remove a package AND its configuration files?
4. Where does APT find its list of available packages?
5. What is the `.deb` file format?
6. How do you search for a package by keyword?
7. What command shows all files installed by a specific package?
8. How do you fix broken dependencies after a failed installation?
9. What is the difference between `apt` and `apt-get`?
10. How do you add a new repository to your system?

## 7. What's next

You can install, update, and remove software like a pro. In **Level 08**, you'll get connected — **networking** commands like `ip`, `ping`, `ssh`, `curl`, and basic troubleshooting.
