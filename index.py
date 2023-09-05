from ftplib import FTP

host = "elcruzo.bplaced.net"
user = "elcruzo"
password = "PutInYourLoginInfo"

with FTP(host) as ftp:
    
    ftp.login(user=user, passwd=password)
    print(ftp.getwelcome())
    
    #Download files with this block of code:
    with open('myupload.txt', "rb") as f:
        ftp.storbinary('STOR' + "upload.txt", f)
        
    ftp.cwd('mydir')
    
    #Upload files with this block of code:
    with open("myspecialfile.txt", "wb") as f:
        ftp.retrbinary("RETR " + "otherfile.txt", f.write, 1024)
    
    # with open("test.txt", "wb") as f:
    #     ftp.retrbinary("RETR " + "mytest.txt", f.write, 1024)
        
    ftp.quit()
    
