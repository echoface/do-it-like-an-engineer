# macmini display not clear


测试结果: 两种方法都测试过了， 结果还是一样的..... 糊 {PS: 说明一下， 我的是2k得显示器。直接开2k很清晰，可惜字实在是太太太太小了... 降级成2048*1152的。调整了一如既然的糊， 通过指令能开启720P的retina现实，可惜现显示的内容太少了，真™鱼与熊掌不可兼得呀....}

####方案一：
解决1080P屏幕模糊地问题， 一个是修改字体平滑等级
终端下执行:

    defaults -currentHost write -globalDomain AppleFontSmoothing -int 2
打开字体平滑, 最后一个数字可以尝试 1,2,3， 如果没有效果通过以下命令关闭字体平滑

    defaults -currentHost delete -globalDomain AppleFontSmoothing
    
    
    
####方案二：
第二个方案就是由一个脚本根据eeid生成一个外部显示器的描述文件，覆盖掉系统自己的配置；

```ruby
#!/usr/bin/ruby
# Create display override file to force Mac OS X to use RGB mode for Display
# see http://embdev.net/topic/284710
# 
# Update 2013-06-24: added -w0 option to prevent truncated lines

require 'base64'

data=`ioreg -l -w0 -d0 -r -c AppleDisplay`

edid_hex=data.match(/IODisplayEDID.*?<([a-z0-9]+)>/i)[1]
vendorid=data.match(/DisplayVendorID.*?([0-9]+)/i)[1].to_i
productid=data.match(/DisplayProductID.*?([0-9]+)/i)[1].to_i

puts "found display: vendorid #{vendorid}, productid #{productid}, EDID:\n#{edid_hex}"

bytes=edid_hex.scan(/../).map{|x|Integer("0x#{x}")}.flatten

puts "Setting color support to RGB 4:4:4 only"
bytes[24] &= ~(0b11000)

puts "Number of extension blocks: #{bytes[126]}"
puts "removing extension block"
bytes = bytes[0..127]
bytes[126] = 0

bytes[127] = (0x100-(bytes[0..126].reduce(:+) % 256)) % 256
puts 
puts "Recalculated checksum: 0x%x" % bytes[127]
puts "new EDID:\n#{bytes.map{|b|"%02X"%b}.join}"

Dir.mkdir("DisplayVendorID-%x" % vendorid) rescue nil
f = File.open("DisplayVendorID-%x/DisplayProductID-%x" % [vendorid, productid], 'w')
f.write '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">'
f.write "
<dict>
  <key>DisplayProductName</key>
  <string>Display with forced RGB mode (EDID override)</string>
  <key>IODisplayEDID</key>
  <data>#{Base64.encode64(bytes.pack('C*'))}</data>
  <key>DisplayVendorID</key>
  <integer>#{vendorid}</integer>
  <key>DisplayProductID</key>
  <integer>#{productid}</integer>
</dict>
</plist>"
f.close
```

#####step by step:
- Connect the external monitor and close the lid (only the external monitor must be connected).
- Run the command chmod +x patch-edid.rb
- Run the script ./patch-edid.rb
- A new folder will be created with the overrides for your monitor.
- Move it into the /System/Library/Displays/Overrides folder.
- Restart your computer.









