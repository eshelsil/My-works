import urllib, re, os

def get_img_src(txt):
    txt = re.split(r'[ >?]', txt)
    for text in txt:
        if text[:3] in ["SRC", "src"]:
            if text[-1] in["'", '"']:            
                return text[5:-1]
            return text[5:]
    return None

def get_folder(file_path):
    if file_path[-1] == "\\":
        return file_path
    else:
        return get_folder(file_path[:-1])

def pic_saver():
    dest_folder = get_folder(__file__) + "pictures"
    if not os.path.isdir(dest_folder):
        os.makedirs(dest_folder)
    address = raw_input("enter url address: ")
    try:
        page = urllib.urlopen(address)
    except:
        print "Couldn't open url, try again."
        pic_saver()
        return
    source = page.read()
    images = re.findall(r'<img .*>', source)
    couldnt_get = []
    for image in images:
        image = get_img_src(image)
        img_name = re.split(r'/', image)[-1]
        if image[:7] != "http://":
            if address[-1] == "/":
                image = address + image
            else:
                image = address + "/" + image
        try:
            img_src = urllib.urlopen(image)
            image_txt = img_src.read()
            file = open(dest_folder + "\\" + img_name, "wb")
            file.write(image_txt)
            file.close()
        except:
            couldnt_get.append(image)
    if len(couldnt_get) > 0:
        print "Pictures I couldn't get (" + str(len(couldnt_get)) + "):"
        for pic in couldnt_get:
            print pic

if __name__ == '__main__':
    pic_saver()
