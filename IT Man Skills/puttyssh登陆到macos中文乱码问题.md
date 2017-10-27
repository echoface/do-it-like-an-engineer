# SSH登陆到MacOS中文乱码

## 前提：

* 你知道ssh是什么
* 你知道putty是何物
* 你打开了MACOS上的远程登陆
* 你是一个知道你在干什么的人

如果你买来一个国行的mac，出于各种各样的目的你需要通过ssh登陆mac；  
有很大可能性， 你可能会遇到你运行 `ls` 或者其他命令， 你会发现中文会显示成乱码，在mac上， 系统使用的不是linux上类似的`LANGUAGE OR LANG`环境变量， 而是使用的另外一个环境变量 `LC_CTYPE ` 所以只要我们在`$HOME/.bash_profile` 或者 `$HOME/.bashrc `下 使用命令`export LC_CTYPE=zh_CN.utf-8`就可以指定使用以UTF8编码方式的中文环境了， 之后在putty中的`Change Settings->Window -> Translation ` 中的 `remote machine character` 选项中使用utf8编码即可正常的显示中文了