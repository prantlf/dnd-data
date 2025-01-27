from lxml.html import fromstring, tostring
from trafilatura import fetch_url, extract
from constants import data_dir, site_origin, md_ext

from re import search, sub
from requests import get
import time

asset_type = "monsters"
target_dir = data_dir() + asset_type
site_url = site_origin() + asset_type + "/"

def get_file_name(url):
    name_match = search(r'/[0-9]+-([-0-9a-zA-Z]+)$', url)
    name = name_match.group(1)
    print(f'name: {name}')
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
    image = dom_root.find_class("monster-image")[0]
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

    header_el = dom_root.find_class("page-header")[0]
    remove_el(header_el)
    sitebar_el = dom_root.find_class("site-bar")[0]
    remove_el(sitebar_el)
    menu_el = dom_root.get_element_by_id("mega-menu-target")
    remove_el(menu_el)
    comments_el = dom_root.find_class("homebrew-comments")[0]
    remove_el(comments_el)
    footer_el = dom_root.cssselect('footer')[0]
    remove_el(footer_el)

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

    with open(target_dir + "/" + file_name + md_ext(), "w") as md_file:
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

# accordeons = document.querySelectorAll('[data-type=monsters][data-slug]')
# Array.from(accordeons).map(({ dataset }) => dataset.slug)
slugs = [
  "16762-aboleth",
  "16763-acolyte",
  "16764-adult-black-dragon",
  "16765-adult-blue-dragon",
  "16766-adult-brass-dragon",
  "16767-adult-bronze-dragon",
  "16768-adult-copper-dragon",
  "16769-adult-gold-dragon",
  "16770-adult-green-dragon",
  "16771-adult-red-dragon",
  "16772-adult-silver-dragon",
  "16773-adult-white-dragon",
  "16774-air-elemental",
  "17087-allosaurus",
  "16775-ancient-black-dragon",
  "16776-ancient-blue-dragon",
  "16777-ancient-brass-dragon",
  "16778-ancient-bronze-dragon",
  "16779-ancient-copper-dragon",
  "16780-ancient-gold-dragon"
  "16781-ancient-green-dragon",
  "16782-ancient-red-dragon",
  "16783-ancient-silver-dragon",
  "16784-ancient-white-dragon",
  "16785-androsphinx",
  "16786-animated-armor",
  "16787-ankheg",
  "17088-ankylosaurus",
  "16788-ape",
  "4775801-ape",
  "16789-archmage",
  "16790-assassin",
  "16791-awakened-shrub",
  "16792-awakened-tree",
  "16793-axe-beak",
  "16794-azer",
  "16795-baboon",
  "16796-badger",
  "4775802-badger",
  "16797-balor",
  "16798-bandit",
  "16799-bandit-captain",
  "17089-banshee",
  "16800-barbed-devil",
  "16801-basilisk",
  "16802-bat",
  "4775803-bat",
  "16803-bearded-devil",
  "16804-behir",
  "16805-berserker",
  "16806-black-bear",
  "4775804-black-bear",
  "16807-black-dragon-wyrmling",
  "16808-black-pudding",
  "16809-blink-dog",
  "16810-blood-hawk",
  "16811-blue-dragon-wyrmling",
  "16812-boar",
  "4775805-boar",
  "16813-bone-devil",
  "16814-brass-dragon-wyrmling",
  "16815-bronze-dragon-wyrmling",
  "16816-brown-bear",
  "4775806-brown-bear",
  "16817-bugbear",
  "16818-bulette",
  "16819-camel",
  "4775807-camel",
  "16820-cat",
  "4775808-cat",
  "16821-centaur",
  "16822-chain-devil",
  "16823-chimera",
  "16824-chuul",
  "16825-clay-golem",
  "16826-cloaker",
  "16827-cloud-giant",
  "16828-cockatrice",
  "16829-commoner",
  "16830-constrictor-snake",
  "4775809-constrictor-snake",
  "16831-copper-dragon-wyrmling",
  "16832-couatl",
  "16833-crab",
  "4775810-crab",
  "16834-crocodile",
  "4775811-crocodile",
  "16836-cult-fanatic",
  "16835-cultist",
  "17090-cyclops",
  "16837-darkmantle",
  "16838-death-dog",
  "17211-deep-gnome-svirfneblin",
  "16839-deer",
  "16840-deva",
  "16841-dire-wolf",
  "4775812-dire-wolf",
  "288142-diseased-giant-rat",
  "16842-djinni",
  "16843-doppelganger",
  "16844-draft-horse",
  "4775813-draft-horse",
  "16845-dragon-turtle",
  "16846-dretch",
  "16847-drider",
  "17133-drow",
  "16848-druid",
  "16849-dryad",
  "16850-duergar",
  "804867-dust-devil",
  "16851-dust-mephit",
  "16852-eagle",
  "16853-earth-elemental",
  "16854-efreeti",
  "16855-elephant",
  "4775814-elephant",
  "16857-elk",
  "4775815-elk",
  "16858-erinyes",
  "16859-ettercap",
  "16860-ettin",
  "16861-fire-elemental",
  "16862-fire-giant",
  "17091-flameskull",
  "16863-flesh-golem",
  "16864-flying-snake",
  "16865-flying-sword",
  "16866-frog",
  "4775816-frog",
  "16867-frost-giant",
  "16868-gargoyle",
  "16869-gelatinous-cube",
  "16870-ghast",
  "16871-ghost",
  "16872-ghoul",
  "16873-giant-ape",
  "16874-giant-badger",
  "4775817-giant-badger",
  "16875-giant-bat",
  "16876-giant-boar",
  "16877-giant-centipede",
  "16878-giant-constrictor-snake",
  "16879-giant-crab",
  "4775818-giant-crab",
  "16880-giant-crocodile",
  "16881-giant-eagle",
  "16882-giant-elk",
  "16883-giant-fire-beetle",
  "16884-giant-frog",
  "16885-giant-goat",
  "4775819-giant-goat",
  "16886-giant-hyena",
  "16887-giant-lizard",
  "16888-giant-octopus",
  "16889-giant-owl",
  "16890-giant-poisonous-snake",
  "16891-giant-rat",
  "16892-giant-scorpion",
  "16893-giant-sea-horse",
  "4775820-giant-seahorse",
  "16894-giant-shark",
  "16895-giant-spider",
  "4775821-giant-spider",
  "16896-giant-toad",
  "16897-giant-vulture",
  "16898-giant-wasp",
  "16899-giant-weasel",
  "4775822-giant-weasel",
  "16900-giant-wolf-spider",
  "16901-gibbering-mouther",
  "16902-glabrezu",
  "16903-gladiator",
  "16904-gnoll",
  "16906-goat",
  "4775823-goat",
  "16907-goblin",
  "17098-gold-dragon-wyrmling",
  "16908-gorgon",
  "16909-gray-ooze",
  "16910-green-dragon-wyrmling",
  "16911-green-hag",
  "16912-grick",
  "16913-griffon",
  "16914-grimlock",
  "16915-guard",
  "16916-guardian-naga",
  "16917-gynosphinx",
  "16918-half-red-dragon-veteran",
  "16919-harpy",
  "16920-hawk",
  "4775824-hawk",
  "16921-hell-hound",
  "16922-hezrou",
  "16923-hill-giant",
  "16924-hippogriff",
  "16925-hobgoblin",
  "16926-homunculus",
  "16927-horned-devil",
  "16928-hunter-shark",
  "16929-hydra",
  "16930-hyena",
  "16931-ice-devil",
  "16932-ice-mephit",
  "16933-imp",
  "4775825-imp",
  "257235-incubus",
  "16934-invisible-stalker",
  "16935-iron-golem",
  "16936-jackal",
  "16937-killer-whale",
  "16938-knight",
  "16939-kobold",
  "16940-kraken",
  "16941-lamia",
  "16942-lemure",
  "16943-lich",
  "16944-lion",
  "4775826-lion",
  "16945-lizard",
  "4775827-lizard",
  "16946-lizardfolk",
  "16947-mage",
  "16948-magma-mephit",
  "16949-magmin",
  "16950-mammoth",
  "16951-manticore",
  "16952-marilith",
  "16953-mastiff",
  "4775828-mastiff",
  "16954-medusa",
  "16955-merfolk",
  "16956-merrow",
  "16957-mimic",
  "16958-minotaur",
  "16959-minotaur-skeleton",
  "16960-mule",
  "4775829-mule",
  "16961-mummy",
  "16962-mummy-lord",
  "16963-nalfeshnee",
  "16965-night-hag",
  "16964-nightmare",
  "16966-noble",
  "17092-nothic",
  "16967-ochre-jelly",
  "16968-octopus",
  "4775830-octopus",
  "16969-ogre",
  "16970-ogre-zombie",
  "16971-oni",
  "16972-orc",
  "16973-otyugh",
  "16974-owl",
  "4775831-owl",
  "16975-owlbear",
  "16976-panther",
  "4775832-panther",
  "16977-pegasus",
  "16978-phase-spider",
  "16979-pit-fiend",
  "16980-planetar",
  "16981-plesiosaurus",
  "16982-poisonous-snake",
  "16983-polar-bear",
  "16984-pony",
  "4775833-pony",
  "16985-priest",
  "16986-pseudodragon",
  "4775834-pseudodragon",
  "17093-pteranodon",
  "16987-purple-worm",
  "16988-quasit",
  "4775835-quasit",
  "16989-quipper",
  "16990-rakshasa",
  "16991-rat",
  "4775836-rat",
  "16992-raven",
  "4775837-raven",
  "16993-red-dragon-wyrmling",
  "16994-reef-shark",
  "4775838-reef-shark",
  "16995-remorhaz",
  "16996-rhinoceros",
  "16997-riding-horse",
  "4775839-riding-horse",
  "16998-roc",
  "16999-roper",
  "17000-rug-of-smothering",
  "17001-rust-monster",
  "17002-saber-toothed-tiger",
  "17003-sahuagin",
  "17004-salamander",
  "17005-satyr",
  "17006-scorpion",
  "4775840-scorpion",
  "17007-scout",
  "17008-sea-hag",
  "17009-sea-horse",
  "17010-shadow",
  "17011-shambling-mound",
  "17012-shield-guardian",
  "17013-shrieker",
  "17014-silver-dragon-wyrmling",
  "17015-skeleton",
  "4775841-skeleton",
  "17016-solar",
  "17094-spectator",
  "17017-specter",
  "17018-spider",
  "4775844-spider",
  "17019-spirit-naga",
  "17020-sprite",
  "4775845-sprite",
  "17021-spy",
  "17022-steam-mephit",
  "17023-stirge",
  "17024-stone-giant",
  "17025-stone-golem",
  "17026-storm-giant",
  "17027-succubus",
  "17028-swarm-of-bats",
  "17029-swarm-of-insects",
  "301407-swarm-of-insects-beetles",
  "301411-swarm-of-insects-centipedes",
  "301414-swarm-of-insects-spiders",
  "301415-swarm-of-insects-wasps",
  "17030-swarm-of-poisonous-snakes",
  "17031-swarm-of-quippers",
  "17032-swarm-of-rats",
  "17033-swarm-of-ravens",
  "17034-tarrasque",
  "17035-thug",
  "17036-tiger",
  "4775846-tiger",
  "17037-treant",
  "17038-tribal-warrior",
  "17039-triceratops",
  "17040-troll",
  "17095-twig-blight",
  "17041-tyrannosaurus-rex",
  "17042-unicorn",
  "17043-vampire",
  "17044-vampire-spawn",
  "17045-veteran",
  "17046-violet-fungus",
  "17047-vrock",
  "17048-vulture",
  "17049-warhorse",
  "4775848-warhorse",
  "17050-warhorse-skeleton",
  "17051-water-elemental",
  "17052-weasel",
  "4775849-weasel",
  "17053-werebear",
  "17054-wereboar",
  "17055-wererat",
  "17056-weretiger",
  "17057-werewolf",
  "17058-white-dragon-wyrmling",
  "17059-wight",
  "17060-will-o-wisp",
  "17061-winter-wolf",
  "17062-wolf",
  "4775850-wolf",
  "17063-worg",
  "17064-wraith",
  "17065-wyvern",
  "17066-xorn",
  "17096-yeti",
  "17067-young-black-dragon",
  "17068-young-blue-dragon",
  "17069-young-brass-dragon",
  "17070-young-bronze-dragon",
  "17071-young-copper-dragon",
  "17072-young-gold-dragon",
  "17073-young-green-dragon",
  "17074-young-red-dragon",
  "17075-young-silver-dragon",
  "17076-young-white-dragon",
  "17077-zombie",
  "4775851-zombie"
]

for slug in slugs:
    download_page(slug)
    time.sleep(3)
