# URL组成


范式
－－－

protocol :// hostname[:port] / path / [;parameters][?query]#fragment 协议://主机名[:端口]/ 路径/[:参数] [?查询]#Fragment

协议://主机名[:端口]/路径/[;参数][?查询]#Fragment



几点说明：
---

example: `https://www.baidu.com/s?ie=UTF-8&wd=URL%E7%BB%84%E6%88%90`

- 虚拟目录部分：从域名后的第一个“/”开始到最后一个“/”为止，是虚拟目录部分。虚拟目录也不是一个URL必须的部分。本例中的虚拟目录的路径是“/s”， 路径也可以是一个文件路径 比如说`/books/swift.html`;

- 有不少前后端的js组件可以提供 url 规范化的功能， 可以用来处理url