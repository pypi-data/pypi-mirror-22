# webfocus HTML网页正文提取

## 安装
```bash

$ pip install webfocus

```

## 使用方式
### 命令行
```bash
Usage: webfocus [OPTIONS] COMMAND [ARGS]...

  webfocus system. ---- Powered by qiulimao@2017.03

Options:
  --help  Show this message and exit.

Commands:
  extract  给定url提取相应的正文
```
目前仅仅`extract` 命令可用

```bash
Usage: webfocus extract [OPTIONS]

  给定url提取相应的正文

Options:
  -u, --url TEXT   the target url
  -n, --shownoise  仅输出噪声，默认为False
  -t, --textonly   输出不带标签的正文，默认为False
  --help           Show this message and exit.
```
### 使用example
```bash
$ webfocus extract
INPUT TARGET URL: 输入你的url

》》》》带标签的结果显示输出
```

```bash
$ webfocus extract -t
INPUT TARGET URL: 输入你的url

》》》》带标签的结果显示输出
```

### 程序当中使用
```
from webfocus.extractor import extract_from_url,extract_from_htmlstring
>>> info,noise = extract_from_url(YOUR_URL,text_only=False)  # 给定url输出 带标签的正文

>>> info,noise = extract_from_htmlstring(YOUR_HTML_STRING,text_only=True)  # 给定html正文输出纯文本正文
```
### 开发日志
*   2017.03.02 正对新闻网页等题材的网站屡试不爽，但是对于博客类网站还有待改进

### 常见问题

#### `Unicode strings with encoding declaration are not supported.`
检查你所访问的url是不是ban爬虫的，可能返回了一个xml的文件给你

#### 提取出来的文字好像都是噪声，不是正文
检查你所要提取的网页的正文部分是不是依靠js加载产生的？如果是，那么肯定提取不出来，比如开源中国博客就是这种方式

### bug report
email:qiu_limao@163.com