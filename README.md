# bypass_wechat_qrcode_scanning
绕过微信公众号、小程序的强制摄像头扫码登陆



## 产生缘由

微信公众号（小程序）的扫码登陆机制是在过于讨厌。一方面自作主张强制进行“二维码登陆保护”，且不能关闭这种“保护”。另一方面，不允许长按扫码或者从相册中选择图片扫码登陆，强制要求通过摄像头扫码登陆。

当你试图构造正确的url，想直接从微信打开，绕过摄像头时，微信的内置浏览器还会修改url，使得无法通过构造url来绕过。

当你试图在Chrome模拟该过程，会发现，即使自己伪造了微信内置浏览器的User-Agent，也会因为缺少必要的cookies而无法完成。

一般人还是不会被这个困扰，所以我找遍全网都没找到这个解决方案。个人是因为弄一些自动化，比如selenium，每次都要人工操作就很麻烦，所以就花时间去研究了下。

### 我要的是一个不用通过手机扫码，单纯在电脑中就能自己伪造扫码过程进行登录的脚本。

## 使用方法
使用方法就是，将脚本中这几行的数据填写为你自己的数据：

```python
    appmsg_token = 'xxxxxxxxx'
    pass_ticket = 'xxxxxxxx'
    wap_sid2 = 'xxxxxxxx'
    user_agent = 'xxxxxxxxx'
    wxuin = 'xxxxxxxx'
    ua_id = 'xxxxxxxxx'
    pgv_pvi = 'xxxxxxxxx'
    pgv_si = 'xxxxxxxxxx'
    uuid = 'xxxxxxxxxx'
```

其中user_agent指的是微信内置浏览器的UA，你可以用微信的内置浏览器去访问一些能显示自己UA的在线工具，然后就能得到。

其他的几个，除了appmsg_token之外，都是cookies。可以在登录微信公众号或者小程序后，按f12在开发者工具中找到这几个cookies对应的值（只要填一次就好，一劳永逸）。

#### 最后剩下一个appmsg_token的获取方式，就比较复杂，需要对微信进行抓包得到。
本来抓包也不难，可是微信自带了对证书的检验，所以微信看到抓包的自签名证书就直接断开连接了，正常情况下无法解密https的流量。

但是我们可以通过hook的方式来使得微信对证书的检验失效。这个时候就需要借助[VitualXposed](https://github.com/android-hacker/VirtualXposed)（免root） + [JustTrustMe](https://github.com/Fuzion24/JustTrustMe)来使得抓包需要的自签名证书被信任。

之后就可以抓包了，关于抓包，你可以使用fiddler，参考[这篇文章](https://github.com/wnma3mz/wechat_articles_spider/blob/master/docs/get_appmsg_token.md)，我使用的是burp，详细说一下过程。

首先你要安装VirtualXposed，然后去微信的官网，下载一个微信的最新版本的apk，最好选择32位的，我安装64位一直失败。然后再VirtualXposed中安装apk。之后再去安装JustTrustMe就可以了。

然后你需要把burp的证书导入到手机里面，在burp里面选择导入证书(export certificate)，然后修改后缀为.cer，传给手机后安装即可，网上可以找到大量教程。

之后，打开手机的wifi，开启代理，填你电脑的内网ip和burp的监听端口就可以了。记得先开启burp的监听再开启VitualXposed中的微信。之后你用微信正常扫码、确认登录，然后要拦截最后确认登录时候的数据包，在POST的内容里面就可以找到**appmsg_token**了。每次扫码登陆，**appmsg_token**都会变化，但是没事，你随便弄一个填写到脚本中，都是可以通过检验的。



现在准备工作做好了，你只要把二维码的图片覆盖qrcode.png就可以了，或者直接用二维码的url，看源码就知道了。启动后就可以直接在电脑中，不再需要手机的扫码，就能成功登陆了。配合selenium食用更佳。