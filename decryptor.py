q#! /usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import sqlite3
import argparse
import json
import chainbreaker

# Change this lol
COOKIE_DB_PATH = "~/Library/Application Support/Google/Chrome/Default/Cookies"

# Get this from chainbreaker:
# python3 -m chainbreaker --dump-all --password-prompt --export-all -o ../lol.memes ./login.keychain-db | grep 'Chrome Safe Storage' -A 1 | grep Password | awk -F ':' '{print $NF}'| tr -d "[:space:]"
CHROME_SAFE_STORAGE_PASS = "hV+dy7aMTuteJAqyNDiGuA==" # See above comment
CHROME_SAFE_STORAGE_PASS = CHROME_SAFE_STORAGE_PASS.encode('utf8')
COOKIE_DB_QUERY = "SELECT name, hex(encrypted_value), host_key, path, expires_utc, is_httponly, is_secure, samesite, source_scheme, source_port FROM cookies;"

# function to get rid of padding
def clean(s):
    if s:
        s = s[:-s[-1]].decode('utf8').strip()
    return s

def getPass(kcDB,pwd):
    #print(keychain)
    kc = chainbreaker.Chainbreaker(kcDB, unlock_password=pwd)
    words=kc.dump_generic_passwords()
    global CHROME_SAFE_STORAGE_PASS
    for word in words:
        if "Chrome Safe Storage" in str(word):
            CHROME_SAFE_STORAGE_PASS = word.password
            #print(word.password)
            return

def decrypt(encrypted_value_hex):
    # replace with your encrypted_value from sqlite3
    encrypted_value = bytes.fromhex(encrypted_value_hex)

    # Trim off the 'v10' that Chrome/ium prepends
    encrypted_value = encrypted_value[3:]

    # Default values used by both Chrome and Chromium in OSX and Linux
    salt = b'saltysalt'
    iv = b' ' * 16
    length = 16

    iterations = 1003

    key = PBKDF2(CHROME_SAFE_STORAGE_PASS, salt, length, iterations)
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)

    decrypted = cipher.decrypt(encrypted_value)
    return clean(decrypted)

def main():
    result=[]
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', help='output as cookie as cvs format[Default output as json format]')
    parser.add_argument('--cookieDB', help='specify the cookieDB file location')
    parser.add_argument('--keychainDB',help='specify the keychainDB file location')
    parser.add_argument('--userpass',help='specify user password')
    args = parser.parse_args()
    cookiedb = sqlite3.connect(args.cookieDB)
    getPass(args.keychainDB,args.userpass)
    cursor = cookiedb.cursor()
    cursor.execute(COOKIE_DB_QUERY)
    records = cursor.fetchall()
    cursor.close()
    cookiedb.close()
    
    if args.csv:
        print("name,value,domain,path,expirationDate,httpOnly,secure,sameSite,SOURCE_SCHEME,SOURCE_PORT")
        for record in records:
            decrypted_value = decrypt(record[1])
            print(f"{record[0]},{decrypted_value},{record[2]},{record[3]},{record[4]},{record[5]},{record[6]},{record[7]},{record[8]},{record[9]}")

    else:
        header = "name,value,domain,path".split(",")
        for record in records:
            decrypted_value = decrypt(record[1])
            domain = str(record[2]).lstrip('.')
            value = [str(record[0]),str(decrypted_value),domain,str(record[3])]
            item = dict(zip(header, value))
            result.append(item)

        json_cookie=json.dumps(result)
        print(json_cookie)

if __name__ == "__main__":
    main()
