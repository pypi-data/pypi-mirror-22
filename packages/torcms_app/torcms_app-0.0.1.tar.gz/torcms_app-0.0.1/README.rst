# yunsuan

## 安装

源代码部署。

## 外部库的安装

外部库都放在 static/alien 下面。 这个文件夹内容是不在 git 代码管理中的。

### CodeMirror

编辑器： codemirror

使用cdn即可。

http://www.bootcdn.cn/codemirror/


##  首次安装


1. 运行


## Database

    \set dbname yunsuan
    CREATE USER :dbname WITH PASSWORD '131322' ; 
    CREATE DATABASE :dbname OWNER :dbname ;
    GRANT ALL PRIVILEGES ON DATABASE :dbname to :dbname ;
    \c :dbname ;
    create extension hstore;
    \q
