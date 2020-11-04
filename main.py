from module.news import getNews
from module.database import connectToDataBase
from module.deletestopword import removeStopWord

from os import system
from termcolor import colored


menu = """

Menu:

1. Lấy bài báo.
2. Tìm kiếm.
3. Thống kê bài báo theo thể loại.
4. Số từ xuất hiện nhiều nhất của từng thể loại.
0. Exit/Quit
"""

def get_news():
    url = 'https://dantri.com.vn/'

    urls = ['su-kien', 'xa-hoi', 'the-thao', 'suc-khoe', 'kinh-doanh', 'o-to-xe-may', 'suc-manh-so', 'giao-duc-huong-nghiep', 'van-hoa', 'giai-tri', 'phap-luat', 'the-gioi']

    category = ['Sự kiện', 'Xã hội', 'Thể thao', 'Sức khỏe', 'Kinh doanh', 'Ô tô - Xe máy', 'Sức mạnh số', 'Giáo dục', 'Văn hóa', 'Giải trí', 'Pháp luật', 'Thế giới']

    db = connectToDataBase()

    for i in range(len(urls)):
        for page in range(1, 11):
            try:
                getNews(url + urls[i] + f'/trang-{page}.htm', db, category[i])
            except:
                pass

    print('Done!')


def find_news(text):
    db = connectToDataBase()
    db.create_index([('Quote', 'text')])
    return db.find({"$text": {"$search": text}}).limit(10)


def statistics():
    db = connectToDataBase()
    print("\nThống kê số lượng bài báo theo từng thể loại:")
    category = ['Sự kiện', 'Xã hội', 'Thể thao', 'Sức khỏe', 'Kinh doanh', 'Ô tô - Xe máy', 'Sức mạnh số', 'Giáo dục', 'Văn hóa', 'Giải trí', 'Pháp luật', 'Thế giới']
    for x in category:
        print(f"  ==> {x}: {db.count_documents({'Category': x})} bài")
    print(f"Tổng: {db.count_documents({})} bài báo.")


def search():
    system('cls')
    search_text = input('\n\nTừ khóa cần tìm: ')
    i = 0
    data = list(find_news(search_text))
    print()

    if len(data) == 0:
        print(colored(f'Không tìm thấy bài viết có từ khóa "{search_text}"\n\n', 'red'))
        system('pause')
        return

    for x in data:
        i += 1
        print(f"     {i}. {x['Title']}")

    while True:
        choose = input("\nBài viết muốn xem (Enter để bỏ qua): ")
        if choose == '':
            break

        try:
            print(f"\nNội dung: {data[int(choose)-1]['Content']}")
            system('pause')
            break
        except:
            print("\nBài viết không tồn tại!")


def word_count(str):
    category = ['Sự kiện', 'Xã hội', 'Thể thao', 'Sức khỏe', 'Kinh doanh', 'Ô tô - Xe máy', 'Sức mạnh số', 'Giáo dục', 'Văn hóa', 'Giải trí', 'Pháp luật', 'Thế giới']
    counts = dict()
    str = removeStopWord(str)
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    sortCount = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    return sortCount[0]


while True:
       system('cls')
       print(menu)
       ans = input("Chọn chức năng: ")
       if ans == "1":
           system('cls')
           print('[INFO] Chờ vài phút!...')
           get_news()
           system('pause')

       elif ans == "2":
           search()

       elif ans == "3":
           system('cls')
           statistics()
           system('pause')

       elif ans == "4":
           category = ['Sự kiện', 'Xã hội', 'Thể thao', 'Sức khỏe', 'Kinh doanh', 'Ô tô - Xe máy', 'Sức mạnh số', 'Giáo dục', 'Văn hóa', 'Giải trí', 'Pháp luật', 'Thế giới']
           system('cls')

           db = connectToDataBase()

           print('Từ xuất hiện nhiều nhất theo từng thể loại: ')

           for x in category:
               myString = ''
               for i in db.find({'Category': x}):
                   myString += str(i['Content'])
               temp = word_count(myString)
               print(f"\n   - Chủ đề: {x} \n   - Từ xuất hiện nhiều nhất: {temp[0]} \n   - Số lần xuất hiện: {temp[1]}\n\n")

           system('pause')

       elif ans == "0":
           break

       else:
           print('Không tồn tài chức năng này!')
           system('pause')
