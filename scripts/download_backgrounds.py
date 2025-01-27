from lxml.html import fromstring, tostring
from trafilatura import fetch_url, extract
from constants import data_dir, site_origin

from re import search, sub
from requests import get
import time

asset_type = "backgrounds"
target_dir = data_dir() + asset_type
site_url = site_origin() + asset_type + "/"

def get_file_name(url):
    name_match = search(r'/[0-9]+-([-0-9a-zA-Z]+)$', url)
    name = name_match.group(1)
    print(f'name: {name}.txt')
    return name

def get_file_ext(url):
    ext_match = search(r'\.[^./]+$', url)
    ext = ext_match.group(0)
    return ext

def load_html(url, file_name):
    html = fetch_url(url)
    # with open(target_dir + "/" + file_name + ".orig.html", "w") as html_file:
    #     html_file.write(html)
    root = fromstring(html)
    return root

def get_page_title(root):
    title_el = root.find_class("page-title")[0]
    title = title_el.text_content()
    title = title.strip()
    print(f'title: {title}')
    return title

def download_image(dom_root, file_name):
    image = dom_root.find_class("image")[0]
    image_url = image.get("src")
    if image_url.startswith("//"):
        image_url = "https:" + image_url
    print(f'image: {image_url}')
    res = get(image_url, allow_redirects=True)
    if not res.ok:
        raise Exception(f'{res.status_code} GET {image_url}')
    ext = get_file_ext(image_url)
    with open(target_dir + "/" + file_name + ext, 'wb') as image_file:
        for block in res.iter_content(1024):
            if not block:
                break
            image_file.write(block)

def clean_page(dom_root):
    def remove_el(el):
        el.getparent().remove(el)

    def remove_first(els):
        if len(els) > 0:
            el = els[0]
            el.getparent().remove(el)

    header_el = dom_root.find_class("page-header")
    remove_first(header_el)
    sitebar_el = dom_root.find_class("site-bar")
    remove_first(sitebar_el)
    menu_el = dom_root.get_element_by_id("mega-menu-target")
    remove_el(menu_el)
    comments_el = dom_root.find_class("homebrew-comments")
    remove_first(comments_el)
    footer_el = dom_root.cssselect('footer')
    remove_first(footer_el)

    subtitles_el = dom_root.find_class("mon-stat-block__description-block-heading")
    for subtitle_el in subtitles_el:
        subtitle_el.tag = "h2"

def save_html(dom_root, file_name):
    html = tostring(dom_root,pretty_print=True, method="html",
                    encoding="UTF-8", doctype="<!DOCTYPE html>")
    # with open(target_dir + "/" + file_name + ".new.html", "wb") as html_file:
    #     html_file.write(html)
    return html

def html_to_md(html, file_name, page_title):
    orig_md = extract(html, output_format='markdown', favor_recall=True,
      with_metadata=True, include_images=True, include_formatting=True,
      include_comments=False, include_tables=True, include_links=False)
    md_lines = orig_md.splitlines()

    def fix_metadata_and_header():
        hr_found = False
        i = 0
        end = len(md_lines)
        while i < end:
            line = md_lines[i]
            if line == "---":
                if hr_found:
                    md_lines.insert(i + 1, "")
                    md_lines.insert(i + 2, "# " + page_title)
                    md_lines.insert(i + 3, "")
                    md_lines.insert(i + 4, "![" + page_title + "](" + file_name + ".png)")
                    md_lines.insert(i + 5, "")
                    i = i + 5
                    break
                else:
                    hr_found = True
            else:
                if hr_found:
                    if not (line.startswith("title:") or line.startswith("url:")):
                        del md_lines[i]
                        i = i - 1
            i = i + 1

    def fix_bold_italic_list_prologs():
        for i in range(0, len(md_lines)):
            line = md_lines[i]
            line = sub(r'^\* ([^.]+\.) ([^:]+:)\* ', r'* **\1** *\2* ', line)
            line = sub(r'^\* ([^.]+\.)\* ', r'* **\1** ', line)
            md_lines[i] = line

    fix_bold_italic_list_prologs()
    fix_metadata_and_header()
    md = "\n".join(md_lines)

    with open(target_dir + "/" + file_name + ".txt", "w") as md_file:
        md_file.write(md)

def download_page(slug):
    page_url = site_url + slug
    file_name = get_file_name(page_url)
    dom_root = load_html(page_url, file_name)
    page_title = get_page_title(dom_root)
    download_image(dom_root, file_name)
    clean_page(dom_root)
    new_html = save_html(dom_root, file_name)
    html_to_md(new_html, file_name, page_title)

# accordeons = document.querySelectorAll('[data-type=backgrounds][data-slug]')
# Array.from(accordeons).map(({ dataset }) => dataset.slug)
slugs = [
  "406475-acolyte",
  "7-acolyte",
  "406474-criminal",
  "8-criminal-spy",
  "9-folk-hero",
  "10-noble",
  "406485-sage",
  "11-sage",
  "406488-soldier",
  "12-soldier"
]

for slug in slugs:
    download_page(slug)
    time.sleep(3)
