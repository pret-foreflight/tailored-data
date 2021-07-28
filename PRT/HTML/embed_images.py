#!/usr/bin/env python3

'''
Jeppesen Proprietary

This work contains valuable confidential and proprietary information.
Disclosure, use or reproduction outside of Jeppesen is prohibited
except as authorized in writing. This unpublished work is protected by
the laws of the United States and other countries. In the event of
publication, the following notice shall apply:

Copyright © 2021 Jeppesen. All rights reserved.
'''

'''
Reads a list of HTML files with tags pointing to image files and embeds
the image using base64.
'''


from bs4 import BeautifulSoup
import base64
import sys
import os


def embed_images(html_file):

    with open(html_file, 'r') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

        if not soup.head:
            print(f'File {html_file} not html, skipping.')
            return None

        for tag, attr in [('source', 'srcset'), ('img', 'src')]:
            for link in soup.find_all(tag):
                file_uri = link.get(attr)

                img_type = file_uri.split('.')[-1]

                if os.path.exists(file_uri):
                    img_b64 = base64.b64encode(open(file_uri, 'rb').read()).decode('utf-8')
                    link[attr] = f'data:image/{img_type};base64,{img_b64}'
                else:
                    print(f'Resource {file_uri[:32]}... not found, skipping.')

    return str(soup.prettify())


def main(argv):
    if len(argv) == 1:
        print('Usage: python embed_image html_file1 [html_file2 ...]')

    for in_file in argv[1:]:

        if not os.path.exists(in_file):
            print(f'File {in_file} not found, skipping.')
            continue

        embedded_html = embed_images(in_file)

        if embedded_html:
            out_file = os.path.splitext(in_file)[0] + '.emb.html'

            with open(out_file, 'w') as file:
                file.write(embedded_html)


if __name__ == '__main__':
    main(sys.argv)
