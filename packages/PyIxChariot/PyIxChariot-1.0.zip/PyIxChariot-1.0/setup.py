#encoding=utf-8
from distutils.core import setup  
setup(name='PyIxChariot',  #��Ҫ������ļ�
      version='1.0',    #�汾��
      description='Request websites to use different clients',    #������Ϣ
      author='qdyxmas',   #����  
      author_email='qdyxmas@gmail.com',    #��������
      url='https://github.com/qdyxmas/Portal-authentication',keywords='python portal Web Authentication', # Դ�����ӵ�ַ
      install_requires=[	
        'requests','requests_toolbelt' #������
      ],
      platform='linux',	#����ƽ̨
      py_modules=['PyIxChariot.kt','PyIxChariot.km','PyIxChariot.kc','PyIxChariot.all'],  #ģ����
)    