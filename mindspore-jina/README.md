# 三分钟教你用MindSpore和Jina搭建一个服装搜索系统

## 准备环境

- Mac OS or Linux
- Python 3.7, 3.8
- [Jina 0.7+ with Hub extenstion (i.e. `pip install "jina[hub]"`)](https://get.jina.ai)
- Docker

## 执行步骤
### 1.创建Jina Hub 镜像

```bash
git clone https://github.com/hanxiao/mindspore-jina-example.git

jina hub build MindsporeLeNet/ --pull --test-uses
```

### 2. Use in Jina Hello-World

```
jina hello-world --uses-index helloworld.flow.index.yml --uses-query helloworld.flow.query.yml
```

## 参考博客