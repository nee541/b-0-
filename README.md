# b-0-
比较简单的小项目
网上冲浪时发现一个“无播放量”的视频，由于是在夜里，看到封面还被吓了一跳。。。
不过发现这类视频好像只能在同种视频的推荐中寻找，而且非登录用户好像不能查看
需要用到：
1.cookie池，项目保存在文件夹CookiesPool中，可通过http://localhost:5555/bilibili/random获取
2.代理池（可选），项目保存在ProxyPool中,可通过访问http://localhost:5000/random获取
还有抓取视频python文件
1.crawl_info.py
2.download_img.py
在下载封面时，发现封面是后来通过js代码加载的，因此耗费了很久，终于发现通过在up主主页搜索视频比较容易找到获取视频封面的api接口
终于大功告成

不过，实力不行，bilibili模拟登陆是用的是selenium加上人工验证验证码，bilibili的文字点击验证码没有破解
还有代码的异常处理太差，可读性也很差
由于异步aiohttp也不会，所以代理池的维护很慢，爬取速度也很慢
并且代理用的是比较便宜的，经常有异常出现，获取视频封面效率很差

还是有些成果
视频BV爬取结果：
![Image text](https://github.com/wenziqiang/b-0-/blob/master/img_folder/BV%E7%BB%93%E6%9E%9C.PNG)

部分视频封面：

