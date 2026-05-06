from lxml import html
import  requests
import csv
import re
BASE_URL = 'https://www.themoviedb.org'
URL = 'https://www.themoviedb.org/movie/top-rated'
ITEMS = 'https://www.themoviedb.org/discover/movie/items'


def get_movie_date(movie_date):
    date = movie_date.strip() if movie_date else ''
    return re.search(r"\d{4}-\d{2}-\d{2}",date).group() if date else ''




def caozuo(url):
    neirong = requests.get(url,timeout=60)
    zhuanhua = html.fromstring(neirong.text)
    # //*[@id="original_header"]/div[2]/section/div[1]/h2/a
    movie_name = zhuanhua.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/a/text()')
    # //*[@id="original_header"]/div[2]/section/div[1]/div/span[2]
    movie_date = zhuanhua.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[2]/text()')
    # //*[@id="original_header"]/div[2]/section/div[1]/div/span[3]
    movie_biaoqian = zhuanhua.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]/a/text()')
    # //*[@id="original_header"]/div[2]/section/div[3]
    movie_mingyan = zhuanhua.xpath('//*[@id="original_header"]/div[2]/section/div[3]/h3[@class="tagline"]/text()')
    # //*[@id="original_header"]/div[2]/section/div[3]/div
    movie_jianjie = zhuanhua.xpath('//*[@id="original_header"]/div[2]/section/div[3]/div/p/text()')

    movie_nei = {
        "电影名":movie_name[0].strip() if movie_name else '',
        "日期":get_movie_date(movie_date[0]) if movie_date else '',
        "标签":",".join(movie_biaoqian) if movie_biaoqian else '',
        "名言":movie_mingyan[0].strip() if movie_mingyan else '',
        "简介":movie_jianjie[0].strip() if movie_jianjie else ''
    }

    return movie_nei



def save_movie(movie_list):
    with open('movie.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['电影名', '日期', '标签', '名言', '简介'])
        writer.writeheader()
        writer.writerows(movie_list)


movie_list = []
for i in range(1, 6):
    if i==1:
        response = requests.get(URL,timeout=60)
    else :
        response = requests.post(ITEMS,
                                 f'air_date.gte=&air_date.lte=&certification=&certification_country=HK&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={i}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2026-11-06&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&watch_region=HK&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400'
                                 ,timeout=60)
    print(f"获取第{i}页数据")
    zhuanhua = html.fromstring(response.text)
    # //*[@class="media-card-list contents w-full"]/div
    # //*[@id="cmp-387d58a8"]/div
    # //*[@id="cmp-d36201e2"]/div
    # //*[@id="cmp-d36201e2"]/div
    movie_top = zhuanhua.xpath('//*[@class="media-list-results contents"]/div')

    for movie in movie_top:
        movie_neirong = movie.xpath('./div/div[1]/a/@href')
        if  movie_neirong:
            pingjie = BASE_URL+movie_neirong[0]
            print(f"获取电影详情{pingjie}")
            movie_nei = caozuo(pingjie)
            movie_list.append(movie_nei)
print("保存文件")
save_movie(movie_list)









