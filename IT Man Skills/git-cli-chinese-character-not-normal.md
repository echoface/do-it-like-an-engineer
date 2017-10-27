# git 相关命令不显示中文的问题

如果只用命令行， 也没有太多高的要求的话， 完全没有必要按照百度出来的文章那么多乱七八糟的设置， 下面一条足以

> git config --global core.quotepath false

这样，当在命令行下输入git commit， git log, git status.... etc; 这些命令的时候中文就不会显示成/xxx/xxx了...

good luck;