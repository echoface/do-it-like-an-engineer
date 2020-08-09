# gitbook editor同时推送到github与gitbook

step 1：
 在gitbook的个人主页上选择需要export到github上的书籍，go to settings page, and click the button `export to github`; done!

step 2:
 go to your github; open the respository you export on step one; then get git url, for example `https://github.com/HuanGong/art_as_programer.git`; copy it;

step 3:
 find out the gitbook editor library path in your computer, go to the folder of your book, edit file
 .git/config; add it "url = https://xxxxxxxxx.xxxxx.xxxx.git"