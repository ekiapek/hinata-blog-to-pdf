import argparse
import json
import pathlib
import requests
from bs4 import BeautifulSoup
import os
import filedate
from weasyprint import HTML, CSS
import css
import datetime
from pathvalidate import validate_filename, ValidationError
member_list = '''
 {"members": [
        {
            "memberName": "Ushio Sarina",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=2"
        },
        {
            "memberName": "Kageyama Yuka",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=4"
        },
        {
            "memberName": "Kato Shiho",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=5"
        },
        {
            "memberName": "Saito Kyoko",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=6"
        },
        {
            "memberName": "Sasaki Kumi",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=7"
        },
        {
            "memberName": "Sasaki Mirei",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=8"
        },
        {
            "memberName": "Takase Mana",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=9"
        },
        {
            "memberName": "Takamoto Ayaka",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=10"
        },
        {
            "memberName": "Higashimura Mei",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=11"
        },
        {
            "memberName": "Kanemura Miku",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=12"
        },
        {
            "memberName": "Kawata Hina",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=13"
        },
        {
            "memberName": "Kosaka Nao",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=14"
        },
        {
            "memberName": "Tomita Suzuka",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=15"
        },
        {
            "memberName": "Nibu Akari",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=16"
        },
        {
            "memberName": "Hamaigishi Hiyori",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=17"
        },
        {
            "memberName": "Matsuda Konoka",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=18"
        },
        {
            "memberName": "Miyata Manamo",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=19"
        },
        {
            "memberName": "Watanabe Miho",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=20"
        },
        {
            "memberName": "Kamimura Hinano",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=21"
        },
        {
            "memberName": "Takahashi Mikuni",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=22"
        },
        {
            "memberName": "Morimoto Marii",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=23"
        },
        {
            "memberName": "Yamaguchi Haruyo",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=24"
        },
        {
            "memberName": "POKA",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=000"
        }
    ]}
'''

css1 = css.sph20201212
css2 = css.sph_custom20211001
css3 = css.style_edit220114
template = '''

<html>
<head>
<link href="./common/sph20201212.css" rel="stylesheet" />
<link href="./common/sph_custom20211001.css" rel="stylesheet" />
<link href="./common/style_edit220114.css" rel="stylesheet" />
</head>
<body class="pages pages_sph pages_sph_60021 pages_sph_60021_index">
    <div class="l-wrap p-wrap__bg">
        <main class="l-main">
            <section class="l-section">
                <div class="l-container" style="break-inside:avoid;">
                    <div class="p-blog-head-container" style="break-inside:avoid;">
                    </div>

                            <div class="p-blog-group" style="padding: 30px 40px 30px 40px">
                            </div>

                </div>
            </section>
        </main>
    </div>
</body>
</html>

'''

listcss = [CSS(string='''
@page:nth(1) {
  size: Legal; /* Change from the default size of A4 */
  margin: 0mm 0mm 10mm 0mm; /* Set margin on each page */
}
@page {
  size: Legal; /* Change from the default size of A4 */
  margin: 15mm 0mm 10mm 0mm; /* Set margin on each page */
}
'''),CSS(string=css1), CSS(string=css2), CSS(string=css3)]

#region parse argument
parser = argparse.ArgumentParser()
parser.add_argument(
    "-p", "--page", help="Define from which page to download.", type=int, default=1)
parser.add_argument(
    "-d", "--dir", help="Define where to save the PDF.", default=str(pathlib.Path(__file__).parent.resolve()))
parser.add_argument(
    "-a", "--allPages", help="Save all of each member's blog.", action='store_true')
args = parser.parse_args()
#endregion

def download_pdf(member, path, title, content, article_date):
    print("Archiving {0} from {1}".format(str(title), member["memberName"]))
    html = HTML(string=str(content))
    html.write_pdf(path, stylesheets=listcss)

    file = filedate.File(path)
    file.set(
        created = article_date,
        modified = article_date
    )

def process_page(member, base_path, pages):
    is_success = True
    try:
        URL = member["blogUrl"]

        if pages > 1:            
            base_url = URL.split("?")[0]
            params = URL.split("?")[1].split("&")
            params.insert(1, "page={0}".format(str(pages)))
            params.append("cd=member")
            paramString = "&".join(params)
            URL = "?".join([base_url, paramString])

        print(URL)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        if soup.find("div", class_="l-contents--blog-list") is None:
            is_success = False

        if is_success:
            blog_article = soup.find_all("div", class_="p-blog-article")
            member_info = soup.find("div", class_="p-blog-member__info")
            detailbtn = member_info.find("div", class_="p-button")
            if detailbtn is not None:
                detailbtn.decompose()
            member_info.find("div", class_="p-blog-member-filter").decompose()
            member_info.find("div", class_="calender_pats").decompose()
            blog_head = soup.find("div", class_="p-blog-head")
            blog_head["style"] = "padding: 30px 40px 30px 40px;width:inherit!important;margin:0px!important;"
            name = blog_article[0].find("div", class_="c-blog-article__name")
            save_path = os.path.join(base_path, name.text.strip())

            if not os.path.exists(save_path):
                os.makedirs(save_path)

            for article in blog_article:
                try:
                    article["style"] = ""
                    content = BeautifulSoup(template, "html.parser")    
                    article_title = article.find(
                        "div", class_="c-blog-article__title").text.strip("\n").strip()
                    article_info = article.find(
                        "div", class_="p-blog-article__info")
                    article_date = article_info.find("div", class_="c-blog-article__date")
                    datetime_string = article_date.text.strip("\n").strip()
                    full_datetime = datetime_string+":00"
                    content.find("div", class_="p-blog-head-container").append(blog_head)
                    content.find("div", class_="p-blog-group").append(article)
                    content.find("div", class_="p-button__blog_detail").decompose()
                    
                    filename = article_title+".pdf"
                    full_path = os.path.join(save_path, filename)

                    try:
                        validate_filename(filename)
                    except ValidationError as e:
                        filename = member["memberName"] + datetime_string.replace(" ","-").replace(":","-") + "_" + ".pdf"  
                        full_path = os.path.join(save_path, filename)       

                    if not os.path.exists(full_path):
                        download_pdf(member, full_path, article_title, content, full_datetime)
                    else:
                        file = filedate.File(full_path)
                        exist_file_date = file.get()
                        created = exist_file_date.get("created")
                        modified = exist_file_date.get("modified")
                        article_datetime = datetime.datetime.strptime(full_datetime,"%Y.%m.%d %H:%M:%S")
                        if created != article_datetime and modified != article_datetime:
                            filename = article_title + "_" + datetime_string.replace(" ","-").replace(":","-") + "_" + ".pdf"  
                            full_path = os.path.join(save_path, filename)
                            if not os.path.exists(full_path):
                                download_pdf(member, full_path, article_title, content, full_datetime)
                        
                except Exception as e:
                    print("Problem downloading {0}-{1}".format(member["memberName"],str(article_title)))
                    print(str(e))
    except Exception as e:
        is_success = False
        print("Problem getting data of {0} \n".format(member["memberName"]))
        print(e)

    return is_success

config = json.loads(member_list)
BASE_PATH = args.dir

print("Save Path: {0}".format(BASE_PATH))
for member in config["members"]:
    print("Archiving {0}'s blog.".format(member["memberName"]))        
    page = args.page
    if args.allPages:
        while(process_page(member, BASE_PATH, page)):
            page += 1
    else:
        process_page(member, BASE_PATH, page)

    print("Downloaded {0}'s blog.\n".format(member["memberName"]))