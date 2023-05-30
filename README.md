## Cookie Handler
This project can help you to decrypt the Chrome cookie using the MacOS keychaindb & Cookiedb file

## How to build
```
// Install Chainbreaker
git clone https://github.com/n0fate/chainbreaker.git
cd ./chainbreaker
python3 setup.py bdist_wheel -d dist
pip3 install -e .

//Install other dependency
pip3 install -r ./requirements.txt 

```

## How to use
/opt/homebrew/bin/python3 ./decryptor.py --cookieDB <Cookie FileLocation> --keychainDB <keychainDB FileLocation> --userpass <PASSWORD>

## Maybe a better way to import cookie & manage
**Can use this plugin to import the cookies(JSON Format)**
https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg

**Can use this plugin to verify the cookies are imported correctly**
https://chrome.google.com/webstore/detail/cookie-editor/iphcomljdfghbkdcfndaijbokpgddeno

**Contributor**
Shout out to @Jordan Sinclair
Shout out to @Stark Li