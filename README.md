# PKUDentist(PKU i看牙预约)

为了解决百京大学生看牙预约难的问题，俺在[PKUAutoSubmit](https://github.com/Bruuuuuuce/PKUAutoSubmit)的基础上，实现了i看牙入口的（半）自动化挂号功能。因为每次放出的号源医生和时间信息皆不确定，目前暂时没有实现全自动抢号功能，每次需要手动指定医生和时间。

## 安装与需求

目前在Windows及Linux平台下进行测试并通过，只需要安装以下依赖：

```
pip install -r requirements.txt
```

然后配置好config.sample.ini并改名为config.ini，
运行脚本：

```
python main.py
```

## 注意事项
采用了webdriver manager适应不同平台来下载浏览器，但有可能遇到局域网的阻断。此时可以手动把

```
driver_pjs = webdriver.Chrome(executable_path=ChromeDriverManager()install(), ...)
```

改为
```
driver_pjs = webdriver.Chrome(executable_path='C:\\Users\\eximple\\.wdm\\drivers\\chromedriver\\win32\\100.0.4896.60\\chromedriver.exe'，, ...)
```

即手动设定为本地地址。

## 证书

[Apache License 2.0](https://github.com/tegusi/PKUDentist/blob/main/LICENSE)