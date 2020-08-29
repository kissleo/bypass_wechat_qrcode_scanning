import requests
import os
import requests
from io import BytesIO
from pyzbar import pyzbar
from PIL import Image

def get_ewm(img_adds):
    """ 
    读取二维码的内容： img_adds：二维码地址（网址or本地路径） 
    从网上复制的，来源：https://blog.csdn.net/qq_30068487/article/details/96833002
    """
    if os.path.isfile(img_adds):
        # 从本地加载二维码图片
        img = Image.open(img_adds)
    else:
        # 从网络下载并加载二维码图片
        rq_img = requests.get(img_adds).content
        img = Image.open(BytesIO(rq_img))

    # img.show()  # 显示图片，测试用

    txt_list = pyzbar.decode(img)

    for txt in txt_list:
        barcodeData = txt.data.decode("utf-8")
        print(barcodeData)
        return barcodeData


def scan_qrcode():

    # 解析二维码，获取二维码的qrticket
    try:
        a = get_ewm(r'登陆扫的二维码的本地路径').split('&')[-1]
    except:
        return

    qrticket = a.split('#')[0].replace('qrticket=', '')
    print('qrticket=', qrticket)


    # 除了wap_sid2以外，其他的值永久适用
    pass_ticket = 'xxxxxxx'
    wap_sid2 = 'xxxxxx'
    user_agent = 'xxxxxx'
    wxuin = 'xxxxxx'
    ua_id = 'xxxxxx'
    pgv_pvi = 'xxxxxxx'
    pgv_si = 'xxxxxx'
    uuid = 'xxxxxxx'


    cookies = {
        'wxuin': wxuin,
        'devicetype': 'android-29',
        'version': '27001134',
        'lang': 'zh_CN',
        'ua_id': ua_id,
        'pgv_pvi': pgv_pvi,
        'pgv_si': pgv_si,
        'uuid': uuid,
        'pass_ticket': pass_ticket,
        'wap_sid2': wap_sid2
    }


    print('需要先请求一下这个“是否确定登录”的页面，否则后面会失败')
    a = requests.get(
        url='https://mp.weixin.qq.com/wap/loginauthqrcode?action=scan&qrticket=%s&lang=zh_CN&devicetype=android-29&version=27001134&pass_ticket=%s&wx_header=1' % (
            qrticket, pass_ticket),
        headers={
            'Host': 'mp.weixin.qq.com',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-User': '?1',
            'X-Requested-With': 'com.tencent.mm',
            'User-Agent': user_agent,
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en-US;q=0.7,en;q=0.6'
        },
        cookies=cookies,
    )

    # 从返回的内容中获取appmsg_token
    appmsg_token = ''
    for line in a.text.splitlines():
        print(line)
        if 'appmsg_token' in line:
            appmsg_token = line.split('=', 1)[1].replace(
                ' ', '').replace(';', '').replace('\'', '')
            print('appmsg_token=', appmsg_token)


    print('发送请求（相当于点击“确认登录”）')
    a = requests.post(
        url='https://mp.weixin.qq.com/wap/loginauthqrcode?action=confirm',
        headers={
            'Host': 'mp.weixin.qq.com',
            'Origin': 'https://mp.weixin.qq.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': user_agent,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://mp.weixin.qq.com/wap/loginauthqrcode?action=scan&qrticket=%s&lang=zh_CN&devicetype=android-29&version=27001134&pass_ticket=%s&wx_header=1' % (qrticket, pass_ticket),
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en-US;q=0.7,en;q=0.6'
        },
        cookies=cookies,
        data={
            'uin': '777',
            'key': '777',
            'pass_ticket': pass_ticket,
            'appmsg_token': appmsg_token,
            'f': 'json',
            'param': 'qrticket',
            'qrticket': qrticket
        },
    )
    print(a.text)
    try:
        if a.json['base_resp']['ret'] == 0:
            print('成功自动登录')
        else:
            print('自动登录失败，状态码是：', a.json['base_resp']['ret'])
    except:
        print('自动登录失败')   

if __name__ == "__main__":
    scan_qrcode()
