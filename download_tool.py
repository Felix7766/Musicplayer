import os

import pygame
from lxml import etree
import requests
import json
from concurrent.futures import ThreadPoolExecutor

# # 创建线程池
# pool = ThreadPoolExecutor(max_workers=10)
# # 请求头信息
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"
# }
#
#
# def download(id, name):
#     # 构造下载链接
#     url = f'http://music.163.com/song/media/outer/url?id={id}'
#     # 发送下载请求
#     response = requests.get(url=url, headers=headers).content
#     # 将响应内容写入文件
#     with open(name + '.mp3', 'wb') as f:
#         f.write(response)
#     # 打印下载完成消息
#     print(name, '下载完成')
#
#
# def get_id(url):
#     # 发送请求获取页面内容
#     response = requests.get(url=url, headers=headers).text
#     # 使用XPath解析页面
#     page_html = etree.HTML(response)
#     # 提取歌曲列表信息
#     id_list = page_html.xpath('//textarea[@id="song-list-pre-data"]/text()')[0]
#     # 解析歌曲列表信息，并逐个提交下载任务到线程池
#     for i in json.loads(id_list):
#         name = i['name']
#         id = i['id']
#         author = i['artists'][0]['name']
#         pool.submit(download, id, name + '-' + author)
#     # 关闭线程池
#     pool.shutdown()
#
# def is_mp3_corrupted(music_path):
#     pygame.mixer.init()
#     try:
#         # 使用pygame.mixer.music加载音乐文件
#         pygame.mixer.music.load(music_path)
#         # 设置音乐音量为0（静音）
#         pygame.mixer.music.set_volume(0)
#         # 尝试播放音乐
#         pygame.mixer.music.play()
#         # # 等待音乐播放完成
#         # while pygame.mixer.music.get_busy():
#         #     pygame.time.Clock().tick(10)
#         # 等待1毫秒
#         pygame.time.delay(1)
#
#         # 停止音乐播放
#         pygame.mixer.music.stop()
#
#     except pygame.error as e:
#         print(f"播放音乐错误: {e}")
#         return False
#     finally:
#         # 停止音乐播放
#         pygame.mixer.music.stop()
#     return True
#
#
#
# if __name__ == '__main__':
#     # 用户输入歌曲关键词
#     keyword = input("请输入歌曲名称：")
#     # 构造搜索URL
#     search_url = f'https://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={keyword}&type=1&offset=0&total=true&limit=5'
#     # 发送搜索请求并获取响应内容
#     response = requests.get(url=search_url, headers=headers).json()
#     # 提取歌曲列表
#     song_list = response['result']['songs']
#     flag=False
#     list=[]
#     # 遍历歌曲列表，逐个提交下载任务到线程池
#     for song in song_list:
#         name = song['name']
#         id = song['id']
#         author = song['artists'][0]['name']
#         pool.submit(download, id, name + '-' + author)
#         list.append(name+"-"+author+".mp3")
#     # 关闭线程池
#     pool.shutdown()
#     for i in list:
#         if is_mp3_corrupted(i)==False:
#             # 检查文件是否存在，然后删除
#             print(i)
#             if os.path.exists(i):
#                 os.remove(i)
#                 print(f"文件 {i} 已被删除")
#             else:
#                 print(f"文件 {i} 不存在")


import os
import json
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import requests
import pygame

class MusicDownloader:
    def __init__(self):
        self.list=[]
        self.pool = ThreadPoolExecutor(max_workers=10)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"
        }

    def download(self, id, name):
        url = f'http://music.163.com/song/media/outer/url?id={id}'
        response = requests.get(url=url, headers=self.headers).content
        with open(name + '.mp3', 'wb') as f:
            f.write(response)
        print(name, '下载完成')

    def get_list(self,keyword):

        search_url = f'https://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={keyword}&type=1&offset=0&total=true&limit=5'
        response = requests.get(url=search_url, headers=self.headers).json()
        song_list = response['result']['songs']
        self.list=[]
        for song in song_list:
            name = song['name']
            id = song['id']
            author = song['artists'][0]['name']
            self.list.append(name + "-" + author)
        # response = requests.get(url=url, headers=self.headers).text
        # page_html = etree.HTML(response)
        # id_list = page_html.xpath('//textarea[@id="song-list-pre-data"]/text()')[0]
        # for i in json.loads(id_list):
        #     name = i['name']
        #     id = i['id']
        #     author = i['artists'][0]['name']
        #     self.pool.submit(self.download, id, name + '-' + author)
        # self.pool.shutdown()
        return self.list

    def is_mp3_corrupted(self, music_path):
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0)
            pygame.mixer.music.play()
            pygame.time.delay(1)
            pygame.mixer.music.stop()
            return True
        except pygame.error as e:
            print(f"播放音乐错误: {e}")
            return False
        finally:
            pygame.mixer.music.stop()

    def check_and_remove_corrupted(self, music_paths):
        sum= len(music_paths)
        for music_path in music_paths:
            if not self.is_mp3_corrupted(music_path):
                sum=sum-1
                print(music_path)
                if os.path.exists(music_path):
                    os.remove(music_path)
                    print(f"文件 {music_path} 已被删除")
                else:
                    print(f"文件 {music_path} 不存在")

    def search_and_download(self, keyword):
        search_url = f'https://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={keyword}&type=1&offset=0&total=true&limit=5'
        response = requests.get(url=search_url, headers=self.headers).json()
        song_list = response['result']['songs']
        music_paths = []
        for song in song_list:
            name = song['name']
            id = song['id']
            author = song['artists'][0]['name']
            self.pool.submit(self.download, id, name + '-' + author)
            music_paths.append(name + "-" + author + ".mp3")
        self.pool.shutdown()
        return self.check_and_remove_corrupted(music_paths)

    def release_resources(self):
        """释放占用的资源"""
        # 停止所有pygame音频操作
        pygame.mixer.music.stop()
        # 卸载pygame混音器模块
        pygame.mixer.quit()
        # 关闭线程池
        self.pool.shutdown()
        # 可以添加其他资源释放操作，如关闭文件句柄等

if __name__ == '__main__':
    downloader = MusicDownloader()
    keyword = input("请输入歌曲名称：")
    downloader.search_and_download(keyword)