#!/usr/bin/env python3

from ftplib import FTP, error_perm
import argparse
import os
import sys
import getpass


def connect(host, user, password, port=21):
    ftp = FTP()
    ftp.connect(host, port)
    ftp.login(user, password)
    return ftp


def list_files(ftp, path="."):
    ftp.cwd(path)
    files = []
    ftp.retrlines("LIST", files.append)
    return files


def download(ftp, remote_path, local_path=None):
    if local_path is None:
        local_path = os.path.basename(remote_path)
    
    with open(local_path, "wb") as f:
        ftp.retrbinary(f"RETR {remote_path}", f.write)
    
    return local_path


def upload(ftp, local_path, remote_path=None):
    if remote_path is None:
        remote_path = os.path.basename(local_path)
    
    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {remote_path}", f)
    
    return remote_path


def delete(ftp, remote_path):
    ftp.delete(remote_path)


def mkdir(ftp, path):
    ftp.mkd(path)


def main():
    parser = argparse.ArgumentParser(
        description="FTP client for file transfers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ftp -H ftp.example.com -u user ls
  ftp -H ftp.example.com -u user get remote.txt
  ftp -H ftp.example.com -u user put local.txt
  ftp -H ftp.example.com -u user put local.txt /path/remote.txt
  ftp -H ftp.example.com -u user rm old.txt
  ftp -H ftp.example.com -u user mkdir newdir
        """
    )
    
    parser.add_argument("-H", "--host", required=True, help="FTP server hostname")
    parser.add_argument("-u", "--user", required=True, help="Username")
    parser.add_argument("-p", "--password", help="Password (prompts if not provided)")
    parser.add_argument("-P", "--port", type=int, default=21, help="Port (default: 21)")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    ls_parser = subparsers.add_parser("ls", help="List files")
    ls_parser.add_argument("path", nargs="?", default=".", help="Remote path")
    
    get_parser = subparsers.add_parser("get", help="Download file")
    get_parser.add_argument("remote", help="Remote file path")
    get_parser.add_argument("local", nargs="?", help="Local file path")
    
    put_parser = subparsers.add_parser("put", help="Upload file")
    put_parser.add_argument("local", help="Local file path")
    put_parser.add_argument("remote", nargs="?", help="Remote file path")
    
    rm_parser = subparsers.add_parser("rm", help="Delete file")
    rm_parser.add_argument("path", help="Remote file path")
    
    mkdir_parser = subparsers.add_parser("mkdir", help="Create directory")
    mkdir_parser.add_argument("path", help="Directory path")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    password = args.password
    if not password:
        password = getpass.getpass(f"Password for {args.user}@{args.host}: ")
    
    try:
        ftp = connect(args.host, args.user, password, args.port)
    except Exception as e:
        print(f"Connection failed: {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.command == "ls":
            for line in list_files(ftp, args.path):
                print(line)
        
        elif args.command == "get":
            local = download(ftp, args.remote, args.local)
            print(f"Downloaded: {args.remote} -> {local}")
        
        elif args.command == "put":
            if not os.path.exists(args.local):
                print(f"File not found: {args.local}", file=sys.stderr)
                sys.exit(1)
            remote = upload(ftp, args.local, args.remote)
            print(f"Uploaded: {args.local} -> {remote}")
        
        elif args.command == "rm":
            delete(ftp, args.path)
            print(f"Deleted: {args.path}")
        
        elif args.command == "mkdir":
            mkdir(ftp, args.path)
            print(f"Created: {args.path}")
    
    except error_perm as e:
        print(f"FTP error: {e}", file=sys.stderr)
        sys.exit(1)
    
    finally:
        ftp.quit()


if __name__ == "__main__":
    main()
