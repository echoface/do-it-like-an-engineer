# Crack StarUML 2.7



[各平台版本均适用，本文更改的为Mac版本](http://bbs.chinapyg.com/thread-79022-1-1.html)

1，打开对应 mac版本的安装包位置，在对应目录/Applications/StarUML.app/Contents/www/license/node/LicenseManagerDomain.js文件。

2，找到文件23行，修改对应下面函数。更改为如下代码：  
```javascript
1.    function validate(PK, name, product, licenseKey) {
2.         var pk, decrypted;
3.         // edit by 0xcb
4.         return {
5.             name: "0xcb",
6.             product: "StarUML",
7.             licenseType: "vip",
8.             quantity: "mergades.com",
9.             licenseKey: "later equals never!"
10.        };
11. 
12.        try {
13.            pk = new NodeRSA(PK);
14.            decrypted = pk.decrypt(licenseKey, 'utf8');
15.        } catch (err) {
16.            return false;
17.        }
18.        var terms = decrypted.trim().split("\n");
19.        if (terms[0] === name && terms[1] === product) {
20.            return { 
21.                name: name, 
22.                product: product, 
23.                licenseType: terms[2],
24.                quantity: terms[3],
25.                licenseKey: licenseKey
26.            };
27.        } else {
28.            return false;
29.        }
30.    }
```
我的做法是注释掉原有代码，再增加，防止出现问题。

3，打开starUML。help>enter license

    Name:0xcb
    licenseKey:later equals never!

然后提示你注册成功！
