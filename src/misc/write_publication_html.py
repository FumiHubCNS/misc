import json
import tomllib

def read_config(path):
    with open(path, 'rb') as f:
        config = tomllib.load(f)
    return config

def extract_structure(jsonl_file_path):
    structure = set()  # 重複しないキーを保持するためにセットを使用

    with open(jsonl_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 各行をJSONとして読み込む
            json_obj = json.loads(line.strip())
            # JSONオブジェクトのキーをセットに追加
            structure.update(json_obj.keys())

    return structure

def extract_key_contents(jsonl_file_path, key_val):
    insert_contents = []

    with open(jsonl_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 各行をJSONとして読み込む
            json_obj = json.loads(line.strip())
            # 'insert'キーが存在する場合、その中身を取り出す
            if key_val in json_obj:
                insert_contents.append(json_obj[key_val])

    return insert_contents

def check_structure(jsonl_file_path):
    structure = extract_structure(jsonl_file_path)
    print("JSONLファイルの構造（キーの一覧）:")
    for key in structure:
        print(f"- {key}")

def check_key(jsonl_file_path,key_val):
    insert_data = extract_key_contents(jsonl_file_path,key_val)
    print("JSONLファイル内の",key_val,"キーの中身:")
    for content in insert_data:
        print(content)

def get_content(meta, data, keyname, label, lang):
    lang_inv = 'en' if lang == 'ja' else 'ja'
    result=''
    flag = lang
    if label in data and keyname in meta['type'] :
        if lang in data[label]:
            result = data[label][lang]
            flag = lang
        else:
            result = data[label][lang_inv]
            flag = lang_inv
    return result

def get_content_without_lang(meta, data, keyname, label):
    result=''
    if label in data and keyname in meta['type'] :
        result = data[label]

    return result


def dump_content_with_lang(meta,data,keyname,lists,lang):
    all_data=[]
    for i in range(len(data)):
        row_data = []
        for j in range(len(lists)):
             row_data.append( get_content(meta[i], data[i], keyname, lists[j], lang) )

        if len(row_data[0]) > 1:
            all_data.append(row_data)
    return all_data

def dump_content_without_lang(meta,data,keyname,lists,):
    all_data=[]
    for i in range(len(data)):
        row_data = []
        for j in range(len(lists)):
             row_data.append( get_content_without_lang(meta[i], data[i], keyname, lists[j]) )

        if len(row_data[0]) > 1:
            all_data.append(row_data)

    return all_data

def dump_paper_misc_list(meta,data,pmflag):
    data1 = dump_content_with_lang(meta,data,pmflag,['paper_title','authors','publication_name'],'en')
    data2 = dump_content_without_lang(meta,data,pmflag,['volume','publication_date'])

    print(f"len(data1): {len(data1)}")
    print(f"len(data2): {len(data2)}")

    result_all = []

    for k in range(len(data1)):
        result_i = []
        output1 = []
        for j in range(len(data1[k])):  
            if j == 1:
                authors_list = []
                for i in range(len(data1[k][1])):
                    authors_list.append(data1[k][1][i]['name'])
                    if(authors_list[i]=='F. Endo'):
                        ref = i
                    elif(authors_list[i]=='遠藤史隆'):
                        ref = i
                if ref == 0:
                    #output1.append(f"<u>{authors_list[ref]}({str(ref+1)}-st)</u>")
                    authors_list[ref] = f"<u>{authors_list[ref]}({str(ref+1)}-st)</u>"
                elif ref == 1:
                    #output1.append(f"<u>{authors_list[ref]}({str(ref+1)}-nd)</u>")
                    authors_list[ref] = f"<u>{authors_list[ref]}({str(ref+1)}-nd)</u>"
                elif ref == 2:
                    #output1.append(f"<u>{authors_list[ref]}({str(ref+1)}-rd)</u>")
                    authors_list[ref] = f"<u>{authors_list[ref]}({str(ref+1)}-rd)</u>"
                else:
                    #output1.append(f"<u>{authors_list[ref]}({str(ref+1)}-th)</u>")
                    authors_list[ref] = f"<u>{authors_list[ref]}({str(ref+1)}-th)</u>"
                
                output1.append(', '.join(map(str, authors_list)))
            
            elif j == 0:
                output1.append(f"<b>{data1[k][j]}</b>")
            else:
                output1.append(f"{data1[k][j]}")
        output2 = []

    
        print(k,data1[k][0],data2[k])
        for j in range(len(data2[k])):
            
            if j == 1:
                output2.append(f"({data2[k][j][:4]})")
            else:
                output2.append(f"<b>{data2[k][j]}</b>")

        if False:
            print(f"\t<p>")
            print(f"\t\t<span class=\"toggle-btn\">")
            print(f"\t\t\t{output1[0]}")
            print(f"\t\t</span>")
            print(f"\t\t<span class=\"dots\">...</span>")
            print(f"\t\t<span class=\"moreContent\">")
            print(f"\t\t\t<br/>")
            print(f"\t\t\t{output1[1]}")
            print(f"\t\t\t<br/>")
            print(f"\t\t\t{output1[2]} {output2[0]} {output2[1]}")
            print(f"\t\t</span>")
            print(f"\t</p>")

        result_i.append(f"\t<p>")
        result_i.append(f"\t\t<span class=\"toggle-btn\">")
        result_i.append(f"\t\t\t{output1[0]}")
        result_i.append(f"\t\t</span>")
        result_i.append(f"\t\t<span class=\"dots\">...</span>")
        result_i.append(f"\t\t<span class=\"moreContent\">")
        result_i.append(f"\t\t\t<br/>")
        result_i.append(f"\t\t\t{output1[1]}")
        result_i.append(f"\t\t\t<br/>")
        result_i.append(f"\t\t\t{output1[2]} {output2[0]} {output2[1]}")
        result_i.append(f"\t\t</span>")
        result_i.append(f"\t</p>")
        
        result_all.append(result_i)

    return result_all

        
def dump_presentations_list(meta,data,pmflag):
    data1 = dump_content_with_lang(meta,data,pmflag,['presentation_title','presenters','event'],'en')
    data2 = dump_content_without_lang(meta,data,pmflag,['publication_date'])
    result_all = []

    for k in range(len(data1)):
        result_i = []
        output1 = []
        for j in range(len(data1[k])):  
            if j == 1:
                authors_list = []
                for i in range(len(data1[k][1])):
                    authors_list.append(data1[k][1][i]['name'])
                    if(authors_list[i]=='F. Endo'):
                        ref = i
                    elif(authors_list[i]=='Fumitaka ENDO'):
                        ref = i
                    elif(authors_list[i]=='遠藤　史隆'):
                        ref = i
                    elif(authors_list[i]=='遠藤史隆'):
                        ref = i                  
                if ref == 0:
                    #output1.append(f"<u>{authors_list[ref]}({str(ref+1)}-st)</u>")
                    authors_list[ref] = f"<u>{authors_list[ref]}({str(ref+1)}-st)</u>"
                elif ref == 1:
                    #output1.append(f"<u>{authors_list[ref]}({str(ref+1)}-nd)</u>")
                    authors_list[ref] = f"<u>{authors_list[ref]}({str(ref+1)}-nd)</u>"
                elif ref == 2:
                    #output1.append(f"<u>{authors_list[ref]}({str(ref+1)}-rd)</u>")
                    authors_list[ref] = f"<u>{authors_list[ref]}({str(ref+1)}-rd)</u>"
                else:
                    #output1.append(f"<u>{authors_list[ref]}({str(ref+1)}-th)</u>")
                    authors_list[ref] = f"<u>{authors_list[ref]}({str(ref+1)}-th)</u>"
                
                output1.append(', '.join(map(str, authors_list)))

            elif j == 0:
                output1.append(f"<b>{data1[k][j]}</b>")
            else:
                output1.append(data1[k][j])
        output2 = []
        for j in range(len(data2[k])):
            if j == 0:
                output2.append(f"({data2[k][j][:4]}/{data2[k][j][5:7]})")
            else:
                output2.append(data2[k][j])

        if False:
            print(f"\t<p>")
            print(f"\t\t<span class=\"toggle-btn\">")
            print(f"\t\t\t{output1[0]}")
            print(f"\t\t</span>")
            print(f"\t\t<span class=\"dots\">...</span>")
            print(f"\t\t<span class=\"moreContent\">")
            print(f"\t\t\t<br/>")
            print(f"\t\t\t{output1[1]}")
            print(f"\t\t\t<br/>")
            print(f"\t\t\t{output1[2]} {output2[0]}")
            print(f"\t\t</span>")
            print(f"\t</p>")

        result_i.append(f"\t<p>")
        result_i.append(f"\t\t<span class=\"toggle-btn\">")
        result_i.append(f"\t\t\t{output1[0]}")
        result_i.append(f"\t\t</span>")
        result_i.append(f"\t\t<span class=\"dots\">...</span>")
        result_i.append(f"\t\t<span class=\"moreContent\">")
        result_i.append(f"\t\t\t<br/>")
        result_i.append(f"\t\t\t{output1[1]}")
        result_i.append(f"\t\t\t<br/>")
        result_i.append(f"\t\t\t{output1[2]} {output2[0]}")
        result_i.append(f"\t\t</span>")
        result_i.append(f"\t</p>")
        
        result_all.append(result_i)

    return result_all

def separate_paper_mist_1st_author(data):
    
    data_1st = []
    data_other = []

    for j in range(len(data)):
        test0 = data[j][7].replace('<u>', '')
        test1 = test0.replace('</u>', '')
        test2 = test1.split(',')

        for i in range(len(test2)):
            if 'F. Endo' in test2[i]:
                ref = i 
            if 'Fumitaka ENDO' in test2[i]:
                ref = i 
            if '遠藤　史隆' in test2[i]:
                ref = i 
            if '遠藤史隆' in test2[i]:
                ref = i 

        if ref+1 == 1:
            data_1st.append(data[j])
        else:
            data_other.append(data[j])
    
    return data_1st,data_other


def write_with_hugo_format():

    config = read_config("param/publication.toml")
    input_path = config["publication"]["input"].strip()
    output_ja_path = config["publication"]["ja"]["output"].strip()
    output_en_path = config["publication"]["en"]["output"].strip()

    jsonl_file_path = input_path
    #check_structure(jsonl_file_path)
    #check_key(jsonl_file_path,'merge')
    
    data = extract_key_contents(jsonl_file_path,'merge')
    meta = extract_key_contents(jsonl_file_path,'insert')

    paper = dump_paper_misc_list(meta,data,'published_papers')
    misc  = dump_paper_misc_list(meta,data,'misc')
    prese = dump_presentations_list(meta,data,'presentations')

    p1st, poth = separate_paper_mist_1st_author(paper)

    #for i in range(len(p1st)):
    #    print(p1st[i][2])

    #for i in range(len(prese[0])):
    #    print(i,prese[0][i])

    #for i in range(len(misc)):
    #    print(paper[i][9][-5:-1])

    f = open(output_ja_path, 'w')
    f.write(f"+++\n")
    f.write(f"archetype = \"theming\"\n")
    f.write(f"weight = 2 \n")
    f.write(f"title = \"Publications\"\n")
    f.write(f"+++\n")
    f.write(f"\n")
    f.write(f"<!DOCTYPE html>\n")
    f.write(f"<html lang=\"ja\">\n")
    f.write(f"<head>\n")
    f.write(f"\t<style>\n")
    f.write(f"\t\t.moreContent {{\n")
    f.write(f"\t\t\tdisplay: none;\n")
    f.write(f"\t\t}}\n")
    f.write(f"\t\t.btn {{\n")
    f.write(f"\t\t\tcursor: pointer;\n")
    f.write(f"\t\t\tbackground-color: transparent;\n")
    f.write(f"\t\t\tborder: none;\n")
    f.write(f"\t\t\tfont-size: 16px;\n")
    f.write(f"\t\t}}\n")
    f.write(f"\t</style>\n")
    f.write(f"</head>\n")
    f.write(f"<body>\n")


    f.write(f"\t<p>\n")
    f.write(f"\t<a href=\"https://researchmap.jp/FumitakaENDO\" target=\"_blank\" rel=\"noopener noreferrer\">research map</a>\n")
    f.write(f"\tをもとに作成した業績リスト\n")
    f.write(f"\t</p>\n")
    f.write(f"\t<p>タイトルをクリックすると共著者や雑誌名が表示されます。</p>\n")
    
    f.write(f"\t<h3>学術雑誌に発表した論文 (筆頭著者)</h3>\n")
    for i in range(len(p1st)):
        for j in range(len(p1st[i])):
            if j == 2: 
                f.write(f"{p1st[i][j][:3]}[{i+1}] {p1st[i][j][3:]}")
            else:
                f.write(f"{p1st[i][j]}\n")

    f.write(f"\t<h3>学術雑誌に発表した論文 (共著者)</h3>\n")
    for i in range(len(poth)):
        for j in range(len(poth[i])):
            if j == 2: 
                f.write(f"{poth[i][j][:3]}[{i+1}] {poth[i][j][3:]}")
            else:
                f.write(f"{poth[i][j]}\n")   

    f.write(f"\t<h3>一般講演・招待講演</h3>\n")
    for i in range(len(prese)):
        for j in range(len(prese[i])):
            if j == 2: 
                f.write(f"{prese[i][j][:3]}[{i+1}] {prese[i][j][3:]}")
            else:
                f.write(f"{prese[i][j]}\n")

    f.write(f"\t<h3>MISC</h3>\n")
    for i in range(len(misc)):
        for j in range(len(misc[i])):
            if j == 2: 
                f.write(f"{misc[i][j][:3]}[{i+1}] {misc[i][j][3:]}")
            else:
                f.write(f"{misc[i][j]}\n")

    f.write(f"\t<script src=\"dump_all_info.js\"></script>\n")
    f.write(f"</body>\n")
    f.write(f"</html>\n")
    f.close()

    f = open(output_en_path, 'w')
    f.write(f"+++\n")
    f.write(f"archetype = \"theming\"\n")
    f.write(f"weight = 2 \n")
    f.write(f"title = \"Publications\"\n")
    f.write(f"+++\n")
    f.write(f"\n")
    f.write(f"<!DOCTYPE html>\n")
    f.write(f"<html lang=\"en\">\n")
    f.write(f"<head>\n")
    f.write(f"\t<style>\n")
    f.write(f"\t\t.moreContent {{\n")
    f.write(f"\t\t\tdisplay: none;\n")
    f.write(f"\t\t}}\n")
    f.write(f"\t\t.btn {{\n")
    f.write(f"\t\t\tcursor: pointer;\n")
    f.write(f"\t\t\tbackground-color: transparent;\n")
    f.write(f"\t\t\tborder: none;\n")
    f.write(f"\t\t\tfont-size: 16px;\n")
    f.write(f"\t\t}}\n")
    f.write(f"\t</style>\n")
    f.write(f"</head>\n")
    f.write(f"<body>\n")
    f.write(f"\t<p>\n")
    f.write(f"\tList of achievements created from \n")
    f.write(f"\t<a href=\"https://researchmap.jp/FumitakaENDO\" target=\"_blank\" rel=\"noopener noreferrer\">research map</a>\n")
    f.write(f"\t</p>\n")
    f.write(f"\t<p>Click on the title will display the co-authors, the journal name and so on.</p>\n")
    
    f.write(f"\t<h3>Major Papers (1st author)</h3>\n")
    for i in range(len(p1st)):
        for j in range(len(p1st[i])):
            if j == 2: 
                f.write(f"{p1st[i][j][:3]}[{i+1}] {p1st[i][j][3:]}")
            else:
                f.write(f"{p1st[i][j]}\n")

    f.write(f"\t<h3>Major Papers (co-author)</h3>\n")
    for i in range(len(poth)):
        for j in range(len(poth[i])):
            if j == 2: 
                f.write(f"{poth[i][j][:3]}[{i+1}] {poth[i][j][3:]}")
            else:
                f.write(f"{poth[i][j]}\n")   

    f.write(f"\t<h3>Presentation</h3>\n")
    for i in range(len(prese)):
        for j in range(len(prese[i])):
            if j == 2: 
                f.write(f"{prese[i][j][:3]}[{i+1}] {prese[i][j][3:]}")
            else:
                f.write(f"{prese[i][j]}\n")

    f.write(f"\t<h3>MISC</h3>\n")
    for i in range(len(misc)):
        for j in range(len(misc[i])):
            if j == 2: 
                f.write(f"{misc[i][j][:3]}[{i+1}] {misc[i][j][3:]}")
            else:
                f.write(f"{misc[i][j]}\n")

    f.write(f"\t<script src=\"dump_all_info.js\"></script>\n")
    f.write(f"</body>\n")
    f.write(f"</html>\n")
    f.close()


if __name__ == '__main__':
    config = read_config("param/publication.toml")
    input_path = config["publication"]["input"].strip()
    output_ja_path = config["publication"]["ja"]["output"].strip()
    output_en_path = config["publication"]["en"]["output"].strip()

    print("Input:", input_path)
    print("JA Output:", output_ja_path)
    print("EN Output:", output_en_path)