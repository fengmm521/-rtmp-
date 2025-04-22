# douyinRTMP_addr
 获取抖音rtmp推流地址

安装的npcap版本是1.81,这是网络硬件的驱动程序,这个是一定要安装的

下载地址:
https://npcap.com/#download


使用的Wireshark是4.4.6,这个工具可以用来抓区网络数据包

下载地址:
https://www.wireshark.org/download.html

安装后需要将tshark.exe放到和main.py同一个目录下,并且需要将tshark.exe的路径添加到环境变量中

安装完成后,运行main.py即可获取抖音rtmp推流地址(我的代码可能有问题,我没有用main.py获取地址成功,谁弄好了告诉我一下)

##### 下边的方法我成功了:

使用wireshark抓取抖音直播rtmp推流地址方法:

1.打开wireshark,选择好对应网卡

2.在过滤器中选择tcp.port == 1935

3.然后打开直播伴侣开启直播,就可以看到抓取到的数据流

4.然后在提到的数据流中Ctrl+F开妈搜索,数据类型选择字符串

5.先搜"connect",会找到rtmp的推流服务器如下边这样:

![1.jpg](https://github.com/fengmm521/douyinRTMP_addr/blob/main/img/1.jpg?raw=true)

6.然后搜索"publish()",在下边的内容中就可以找到流串密钥

![2.jpg](https://github.com/fengmm521/douyinRTMP_addr/blob/main/img/2.jpg?raw=true)

拿到流串地址和流串密钥后,就可以使用obs进行推流了.

进入设置
![3.jpg](https://github.com/fengmm521/douyinRTMP_addr/blob/main/img/3.jpg?raw=true)
填好推流地址,之后就可以开始用obs推流了

![4.jpg](https://github.com/fengmm521/douyinRTMP_addr/blob/main/img/4.jpg?raw=true)
