from pixivpy3 import *
import json
import os

aapi = AppPixivAPI()
#メールアドレス及びパスワードを環境変数から取得
PIXIV_PASS = os.environ["PIXIV_PASS"]
MAIL = os.environ["MAIL"]
TARGET = ""#探したいタグ
aapi.login(MAIL,PIXIV_PASS)
dir = ""#イラストを置きたいパスを指定

saving_dir_path =  dir + TARGET #TARGETの名前のフォルダに保存
if not os.path.exists(saving_dir_path):
    os.mkdir(saving_dir_path)
#sort = date_desc or date_asc
json_result = aapi.search_illust(word=TARGET,search_target='exact_match_for_tags',sort='date_desc',filter=None)

for num,illust in enumerate(json_result['illusts']):
    if illust['type'] == 'illust' and illust['meta_single_page']:#イラストの場合
        image_url = illust['meta_single_page']['original_image_url']
        name = (illust['title'] + '_' + illust['user']['name'] + '.jpg').replace("/","-")
        aapi.download(image_url, path=saving_dir_path, name=name)
    elif illust['type'] == 'illust' and illust['meta_pages']:#複数枚のイラストの場合
        for i in range(len(illust['meta_pages'])):
            page = illust['meta_pages'][i]
            image_url = page['image_urls']['original']
            name = (illust['title'] + '_' + illust['user']['name'] + '(' +str(i+1) + ').jpg').replace("/","-")
            aapi.download(image_url, path=saving_dir_path, name=name)
    elif illust['type'] == 'ugoira' and illust['meta_single_page']:#うごイラ
        image_url = illust['meta_single_page']['original_image_url']
        name = (illust['title'] + '_' + illust['user']['name'] + "(うごイラ)" + '.jpg').replace("/","-")
        aapi.download(image_url, path=saving_dir_path, name=name)
    elif illust['type'] == 'manga' and illust['meta_pages']:#漫画の場合
        for i in range(len(illust['meta_pages'])):
            page = illust['meta_pages'][i]
            image_url = page['image_urls']['original']
            name = (illust['title'] + '_' + illust['user']['name'] + '(' +str(i+1) + ').jpg').replace("/","-")
            aapi.download(image_url, path=saving_dir_path, name=name)
    elif illust['type'] == 'manga' and illust['meta_single_page']:
        image_url = illust['meta_single_page']['original_image_url']
        name = (illust['title'] + '_' + illust['user']['name'] + '.jpg').replace("/","-")
        aapi.download(image_url, path=saving_dir_path, name=name)
    else:
        print("サポート外の形式が検出されました"+ " (id:" + illust['id']+")")

    print("\rDownloading {0}/{1}".format(num+1,len(json_result['illusts'])),end='')



print("\nDownload Completed")
