### idea from https://github.com/chenminghua/torrent-cli.git
#### 源码安装
```
 $ git clone https://github.com/chenminghua/sso-cli.git
 $ cd tvsso-cli
 $ pip install -r requirements.txt
 $ python setup.py install
 ```


### 用法
```
$tvsso-cli
usage: tvsso-cli [-h] [-a -e email -n name]  [-r username] [-d username]

Magnets-Getter CLI Tools.

optional arguments:
  -h, --help            show this help message and exit
  -a                    add new user
  -e                    email
  -n                    name
  -r                    resetpassword
  -d                    delete user
```


#### 简单示范
```
$tvsso-cli -r -e zhangsan@qq.com
Done...

```
