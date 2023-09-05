# FTP Client

A simple command-line FTP client for file transfers.

## Installation

```bash
git clone https://github.com/elcruzo/ftp-client.git
cd ftp-client
chmod +x ftp.py
```

## Usage

```bash
./ftp.py -H <host> -u <user> <command> [args]
```

### Commands

| Command | Description |
|---------|-------------|
| `ls [path]` | List files in directory |
| `get <remote> [local]` | Download file |
| `put <local> [remote]` | Upload file |
| `rm <path>` | Delete file |
| `mkdir <path>` | Create directory |

### Options

| Flag | Description |
|------|-------------|
| `-H, --host` | FTP server hostname (required) |
| `-u, --user` | Username (required) |
| `-p, --password` | Password (prompts if not provided) |
| `-P, --port` | Port (default: 21) |

## Examples

```bash
./ftp.py -H ftp.example.com -u myuser ls

./ftp.py -H ftp.example.com -u myuser ls /public

./ftp.py -H ftp.example.com -u myuser get report.pdf

./ftp.py -H ftp.example.com -u myuser get report.pdf ./downloads/report.pdf

./ftp.py -H ftp.example.com -u myuser put data.csv

./ftp.py -H ftp.example.com -u myuser put data.csv /uploads/data.csv

./ftp.py -H ftp.example.com -u myuser rm old_file.txt

./ftp.py -H ftp.example.com -u myuser mkdir backups
```

## License

MIT License - see [LICENSE](LICENSE) for details.
