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
