# !usr/bin/env python
# coding=gbk
import os
from subprocess import call

import pyPdf
from tqdm import tqdm


def pdf_link_2_txt(path_pdf='drm20150330-20170310.pdf'):
    PDFFile = open(path_pdf, 'rb')

    PDF = pyPdf.PdfFileReader(PDFFile)
    pages = PDF.getNumPages()
    key = '/Annots'
    uri = '/URI'
    ank = '/A'
    all_link = []
    for page in range(pages):

        pageSliced = PDF.getPage(page)
        pageObject = pageSliced.getObject()

        if pageObject.has_key(key):
            ann = pageObject[key]
            for a in ann:
                u = a.getObject()
                if u[ank].has_key(uri):
                    print u[ank][uri]
                    if 'maomaoChyan' not in u[ank][uri]:
                        if 'channel' not in u[ank][uri]:
                            all_link.append(u[ank][uri])
    out_path = path_pdf.replace('.pdf', '.txt')
    file_txt = open(out_path, 'w')
    all_link_set = set(all_link)
    for link in all_link_set:
        link = link.split('&')[0]
        file_txt.writelines(link)
        file_txt.writelines('\n')
    file_txt.close()
    return out_path


def download_youtube_playlist(list_link='http://'):
    command = "youtube-dl -c " + list_link
    call(command.split(), shell=False)
    return 0


def download_youtube(link_txt='linkdrm20130701-20150325.txt'):
    txt_file = open(link_txt, 'r')
    links = txt_file.readlines()
    txt_file.close()
    for download_link in tqdm(links):
        # print links
        command = "youtube-dl " + download_link.split('&')[0] + " -c"
        print command
        call(command.split(), shell=False)

    # command = "youtube-dl https://www.youtube.com/watch?v=NG3WygJmiVs -c"
    # call(command.split(), shell=False)
    return 0


def rename_tag(rename_file_dir='toberename', tag='���ݡ�', digital_len=3):
    for parent, dirnames, filenames in os.walk(rename_file_dir):
        for filename in filenames:
            files_in = os.path.join(parent, filename)
            files_in_name = os.path.basename(files_in)
            numbers = [num for num in files_in_name if num.isdigit()]
            date = ''
            for digit_str in numbers:
                date += digit_str
            files_out = files_in.replace(files_in_name, tag + date[:digital_len] + files_in_name)
            os.rename(files_in, files_out)
    return 0
