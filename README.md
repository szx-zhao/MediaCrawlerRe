<summary>🔗 <strong>使用 Python 原生 venv 管理环境（不推荐）</strong></summary>

#### 创建并激活 Python 虚拟环境

> 如果是爬取抖音和知乎，需要提前安装 nodejs 环境，版本大于等于：`16` 即可

```shell
# 进入项目根目录
cd MediaCrawler

# 创建虚拟环境
# 我的 python 版本是：3.9.6，requirements.txt 中的库是基于这个版本的
# 如果是其他 python 版本，可能 requirements.txt 中的库不兼容，需自行解决
python -m venv venv

# macOS & Linux 激活虚拟环境
source venv/bin/activate

# Windows 激活虚拟环境
venv\Scripts\activate
```

#### 安装依赖库

```shell
pip install -r requirements.txt
```

#### 安装 playwright 浏览器驱动

```shell
playwright install
```

#### 运行爬虫程序（原生环境）

```shell
# 项目默认是没有开启评论爬取模式，如需评论请在 config/base_config.py 中的 ENABLE_GET_COMMENTS 变量修改
# 一些其他支持项，也可以在 config/base_config.py 查看功能，写的有中文注释

# 从配置文件中读取关键词搜索相关的帖子并爬取帖子信息与评论
python main.py --platform xhs --lt qrcode --type search

# 从配置文件中读取指定的帖子ID列表获取指定帖子的信息与评论信息
python main.py --platform xhs --lt qrcode --type detail

# 打开对应APP扫二维码登录

# 其他平台爬虫使用示例，执行下面的命令查看
python main.py --help

python main.py --platform dy --lt qrcode --type search --keywords '曹操'
```



## 💾 数据保存

支持多种数据存储方式：
- **CSV 文件**：支持保存到 CSV 中（`data/` 目录下）
- **JSON 文件**：支持保存到 JSON 中（`data/` 目录下）
- **数据库存储**
  - 使用参数 `--init_db` 进行数据库初始化（使用`--init_db`时不需要携带其他optional）
  - **SQLite 数据库**：轻量级数据库，无需服务器，适合个人使用（推荐）
    1. 初始化：`--init_db sqlite`
    2. 数据存储：`--save_data_option sqlite`
  - **MySQL 数据库**：支持关系型数据库 MySQL 中保存（需要提前创建数据库）
    1. 初始化：`--init_db mysql`
    2. 数据存储：`--save_data_option db`（db 参数为兼容历史更新保留）


### 使用示例：
```shell
# 初始化 SQLite 数据库（使用'--init_db'时不需要携带其他optional）
uv run main.py --init_db sqlite
# 使用 SQLite 存储数据（推荐个人用户使用）
uv run main.py --platform xhs --lt qrcode --type search --save_data_option sqlite
```
```shell
# 初始化 MySQL 数据库
uv run main.py --init_db mysql
# 使用 MySQL 存储数据（为适配历史更新，db参数进行沿用）
uv run main.py --platform xhs --lt qrcode --type search --save_data_option db
```


[🚀 MediaCrawlerPro 重磅发布 🚀！更多的功能，更好的架构设计！](https://github.com/MediaCrawlerPro)

---

### 💰 赞助商展示

<a href="https://www.swiftproxy.net/?ref=nanmi">
<img src="docs/static/images/img_5.png">
<br>
Swiftproxy - 90M+ 全球高质量纯净住宅IP，注册可领免费 500MB 测试流量，动态流量不过期！
> 专属折扣码：**GHB5** 立享九折优惠！
</a>

<br>
<br>

<a href="https://h.wandouip.com">
<img src="docs/static/images/img_8.jpg">
<br>
豌豆HTTP自营千万级IP资源池，IP纯净度≥99.8%，每日保持IP高频更新，快速响应，稳定连接，满足多种业务场景，支持按需定制，注册免费提取10000ip。
</a>



### 🤝 成为赞助者

成为赞助者，可以将您的产品展示在这里，每天获得大量曝光！

**联系方式**：
- 微信：`yzglan`
- 邮箱：`relakkes@gmail.com`


## 🤝 社区与支持

### 💬 交流群组
- **微信交流群**：[点击加入](https://nanmicoder.github.io/MediaCrawler/%E5%BE%AE%E4%BF%A1%E4%BA%A4%E6%B5%81%E7%BE%A4.html)

### 📚 文档与教程
- **在线文档**：[MediaCrawler 完整文档](https://nanmicoder.github.io/MediaCrawler/)
- **爬虫教程**：[CrawlerTutorial 免费教程](https://github.com/NanmiCoder/CrawlerTutorial)
  

# 其他常见问题可以查看在线文档
> 
> 在线文档包含使用方法、常见问题、加入项目交流群等。
> [MediaCrawler在线文档](https://nanmicoder.github.io/MediaCrawler/)
> 

# 作者提供的知识服务
> 如果想快速入门和学习该项目的使用、源码架构设计等、学习编程技术、亦或者想了解MediaCrawlerPro的源代码设计可以看下我的知识付费栏目。

[作者的知识付费栏目介绍](https://nanmicoder.github.io/MediaCrawler/%E7%9F%A5%E8%AF%86%E4%BB%98%E8%B4%B9%E4%BB%8B%E7%BB%8D.html)


---

## ⭐ Star 趋势图

如果这个项目对您有帮助，请给个 ⭐ Star 支持一下，让更多的人看到 MediaCrawler！

[![Star History Chart](https://api.star-history.com/svg?repos=NanmiCoder/MediaCrawler&type=Date)](https://star-history.com/#NanmiCoder/MediaCrawler&Date)



## 📚 参考

- **小红书客户端**：[ReaJason 的 xhs 仓库](https://github.com/ReaJason/xhs)
- **短信转发**：[SmsForwarder 参考仓库](https://github.com/pppscn/SmsForwarder)
- **内网穿透工具**：[ngrok 官方文档](https://ngrok.com/docs/)


# 免责声明
<div id="disclaimer"> 

## 1. 项目目的与性质
本项目（以下简称“本项目”）是作为一个技术研究与学习工具而创建的，旨在探索和学习网络数据采集技术。本项目专注于自媒体平台的数据爬取技术研究，旨在提供给学习者和研究者作为技术交流之用。

## 2. 法律合规性声明
本项目开发者（以下简称“开发者”）郑重提醒用户在下载、安装和使用本项目时，严格遵守中华人民共和国相关法律法规，包括但不限于《中华人民共和国网络安全法》、《中华人民共和国反间谍法》等所有适用的国家法律和政策。用户应自行承担一切因使用本项目而可能引起的法律责任。

## 3. 使用目的限制
本项目严禁用于任何非法目的或非学习、非研究的商业行为。本项目不得用于任何形式的非法侵入他人计算机系统，不得用于任何侵犯他人知识产权或其他合法权益的行为。用户应保证其使用本项目的目的纯属个人学习和技术研究，不得用于任何形式的非法活动。

## 4. 免责声明
开发者已尽最大努力确保本项目的正当性及安全性，但不对用户使用本项目可能引起的任何形式的直接或间接损失承担责任。包括但不限于由于使用本项目而导致的任何数据丢失、设备损坏、法律诉讼等。

## 5. 知识产权声明
本项目的知识产权归开发者所有。本项目受到著作权法和国际著作权条约以及其他知识产权法律和条约的保护。用户在遵守本声明及相关法律法规的前提下，可以下载和使用本项目。

## 6. 最终解释权
关于本项目的最终解释权归开发者所有。开发者保留随时更改或更新本免责声明的权利，恕不另行通知。
</div>
