# Django Qiniu Plugin

Django后台插件，使得Django的`admin`系统可以完美支持七牛上传。同时，也支持`xadmin`。


---------------------------

### 使用：
1. 在项目的`settings.py`文件中，配置以下信息：
	```python
	# 七牛配置
	QINIU_DOMAIN = '七牛域名'
	QINIU_ACCESS_KEY = '七牛的access_key'
	QINIU_SECRET_KEY = '七牛的secret_key'
	QINIU_BUCKET_NAME = '七牛的bucket_name（也即空间）'
	```

2. 在`models.py`文件中，把需要保存七牛上传文件后的地址的字段，使用`QiniuField`，如下所示：
	```python
	from DjangoQiniu.models import QiniuField
	from django import models

	class Course(models.Model):
		course_name = models.CharField(max_length=100)
		video_url = models.QiniuField(max_length=100,qiniu_field='video_url',btn_title=u'上传到七牛')
	```
	其中`QiniuField`的`qiniu_field`必须传和当前字段一样的名字。`btn_title`不传则默认为`上传文件`。

