# nvm 在fish shell中的两种使用方式

#How to Make NVM working On Fish shell @ platform OSX

- ##方法一： 使用nvm-fish-wrapper
https://github.com/passcod/nvm-fish-wrapper

step 1: 安装nvm 
```
~> brew install nvm
~> mkdir ~/.nvm
~> ln -s (brew --prefix nvm)/nvm.sh ~/.nvm/nvm.sh
```
step 2： 设置NVM_DIR环境变量［fish的变量］
```
file: ~/.config/fish/config.fish
set -x NVM_DIR ~/.nvm
```

step 3: 安装nvm-fish-wrapper
```
~> cd ~/.config/fish
~/.c/fish> git clone git://github.com/passcod/nvm-fish-wrapper.git nvm-wrapper
```
step 4: 设置对wrapper的引用
```
#Finally edit your config.fish and add this line:
#file: ~/.config/fish/config.fish
source ~/.config/fish/nvm-wrapper/nvm.fish
```

###大功告成 !!!!


- ##方法二： 使用nvm-fish
https://github.com/Alex7Kom/nvm-fish
it is a port of nvm for fish shell. still beta;

