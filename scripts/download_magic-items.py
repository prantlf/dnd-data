from lxml.html import fromstring, tostring
from trafilatura import fetch_url, extract
from constants import data_dir, site_origin, md_ext

from re import search, sub
from requests import get
import time

asset_type = "magic-items"
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
    image = dom_root.find_class("magic-item-image")[0]
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

# accordeons = document.querySelectorAll('[data-type=magic-items][data-slug]')
# Array.from(accordeons).map(({ dataset }) => dataset.slug)
slugs = [
  "5370-adamantine-armor",
  "5407-ammunition-1",
  "5410-ammunition-2",
  "5411-ammunition-3",
  "4568-amulet-of-health",
  "4569-amulet-of-proof-against-detection-and-location",
  "4570-amulet-of-the-planes",
  "4571-animated-shield",
  "4572-apparatus-of-the-crab",
  "4574-armor-of-invulnerability",
  "5371-armor-of-resistance",
  "5376-armor-of-vulnerability",
  "5377-armor-1",
  "5378-armor-2",
  "5379-armor-3",
  "4578-arrow-of-slaying",
  "4577-arrow-catching-shield",
  "4579-bag-of-beans",
  "4580-bag-of-devouring",
  "4581-bag-of-holding",
#   "9228356-bag-of-holding",
  "4582-bag-of-tricks",
  "4583-bead-of-force",
  "27022-bead-of-nourishment",
  "4584-belt-of-dwarvenkind",
  "5372-belt-of-giant-strength",
  "5382-berserker-axe",
  "535335-boomerang-1",
  "535336-boomerang-2",
  "535339-boomerang-3",
  "4587-boots-of-elvenkind",
  "4588-boots-of-levitation",
  "4589-boots-of-speed",
  "4590-boots-of-striding-and-springing",
  "4591-boots-of-the-winterlands",
  "4592-bowl-of-commanding-water-elementals",
  "4593-bracers-of-archery",
  "4594-bracers-of-defense",
  "4595-brazier-of-commanding-fire-elementals",
  "4596-brooch-of-shielding",
  "4597-broom-of-flying",
  "9228372-broom-of-flying",
  "4598-candle-of-invocation",
  "4599-cape-of-the-mountebank",
  "5373-carpet-of-flying",
  "4601-censer-of-controlling-air-elementals",
  "4602-chime-of-opening",
  "4603-circlet-of-blasting",
  "4604-cloak-of-arachnida",
  "4605-cloak-of-displacement",
  "4606-cloak-of-elvenkind",
  "5347-cloak-of-invisibility",
  "9059006-cloak-of-invisibility",
  "4607-cloak-of-protection",
  "4608-cloak-of-the-bat",
  "4609-cloak-of-the-manta-ray",
  "4610-crystal-ball",
  "4862-crystal-ball-of-mind-reading",
  "4863-crystal-ball-of-telepathy",
  "4864-crystal-ball-of-true-seeing",
  "4611-cube-of-force",
  "4612-cubic-gate",
  "4613-dagger-of-venom",
  "5383-dancing-sword",
  "4615-decanter-of-endless-water",
  "4616-deck-of-illusions",
  "4617-deck-of-many-things",
  "9228421-deck-of-many-things",
  "5384-defender",
  "4619-demon-armor",
  "4620-dimensional-shackles",
  "5380-dragon-scale-mail",
  "5385-dragon-slayer",
  "4623-dust-of-disappearance",
  "4624-dust-of-dryness",
  "4625-dust-of-sneezing-and-choking",
  "4626-dwarven-plate",
  "9228527-dwarven-plate",
  "4627-dwarven-thrower",
  "4628-efficient-quiver",
  "4629-efreeti-bottle",
  "9228530-efreeti-chain",
  "5374-elemental-gem",
  "5351-elixir-of-health",
  "4631-elven-chain",
  "9228539-elven-chain",
  "9058960-energy-bow",
  "4632-eversmoking-bottle",
  "4633-eyes-of-charming",
  "4634-eyes-of-minute-seeing",
  "4635-eyes-of-the-eagle",
  "9276755-eyes-of-the-eagle",
  "5412-feather-token",
  "5413-figurine-of-wondrous-power",
  "5386-flame-tongue",
  "9228647-flame-tongue",
  "4639-folding-boat",
  "5387-frost-brand",
  "9228651-frost-brand",
  "4641-gauntlets-of-ogre-power",
  "4642-gem-of-brightness",
  "4643-gem-of-seeing",
  "5388-giant-slayer",
  "4645-glamoured-studded-leather",
  "4646-gloves-of-missile-snaring",
  "4647-gloves-of-swimming-and-climbing",
  "5352-gloves-of-thievery",
  "4648-goggles-of-night",
  "4649-hammer-of-thunderbolts",
  "4650-handy-haversack",
  "4651-hat-of-disguise",
  "9058998-hat-of-many-spells",
  "4652-headband-of-intellect",
  "4653-helm-of-brilliance",
  "4654-helm-of-comprehending-languages",
  "4655-helm-of-telepathy",
  "4656-helm-of-teleportation",
  "5389-holy-avenger",
  "4658-horn-of-blasting",
  "5414-horn-of-valhalla",
  "4660-horseshoes-of-a-zephyr",
  "4661-horseshoes-of-speed",
  "4662-immovable-rod",
  "4663-instant-fortress",
  "5415-ioun-stone",
  "4665-iron-bands-of-binding",
  "4666-iron-flask",
  "4667-javelin-of-lightning",
  "4668-lantern-of-revealing",
  "5393-luck-blade",
  "4670-mace-of-disruption",
  "4671-mace-of-smiting",
  "4672-mace-of-terror",
  "4673-mantle-of-spell-resistance",
  "4674-manual-of-bodily-health",
  "4675-manual-of-gainful-exercise",
  "5416-manual-of-golems",
  "4677-manual-of-quickness-of-action",
  "4678-marvelous-pigments",
  "81901-masters-amulet",
  "4679-medallion-of-thoughts",
  "4680-mirror-of-life-trapping",
  "5381-mithral-armor",
  "4682-necklace-of-adaptation",
  "4683-necklace-of-fireballs",
  "4684-necklace-of-prayer-beads",
  "9058987-nikos-mace",
  "5394-nine-lives-stealer",
  "4686-oathbow",
  "9228907-oathbow",
  "4687-oil-of-etherealness",
  "4688-oil-of-sharpness",
  "4689-oil-of-slipperiness",
  "4690-orb-of-dragonkind",
  "4691-pearl-of-power",
  "4692-periapt-of-health",
  "4693-periapt-of-proof-against-poison",
  "9276658-periapt-of-proof-against-poison",
  "4694-periapt-of-wound-closure",
  "4695-philter-of-love",
  "4696-pipes-of-haunting",
  "4697-pipes-of-the-sewers",
  "9228926-pipes-of-the-sewers",
  "4698-plate-armor-of-etherealness",
  "4699-portable-hole",
  "4700-potion-of-animal-friendship",
  "9228933-potion-of-animal-friendship",
  "4701-potion-of-clairvoyance",
  "4702-potion-of-climbing",
  "4703-potion-of-diminution",
  "4704-potion-of-flying",
  "4705-potion-of-gaseous-form",
  "5417-potion-of-giant-strength",
  "4707-potion-of-growth",
  "4709-potion-of-heroism",
  "4710-potion-of-invisibility",
  "5358-potion-of-invulnerability",
  "5359-potion-of-longevity",
  "4711-potion-of-mind-reading",
  "9228936-potion-of-mind-reading",
  "4712-potion-of-poison",
  "9228937-potion-of-poison",
  "5419-potion-of-resistance",
  "4714-potion-of-speed",
  "9228939-potion-of-speed",
  "5360-potion-of-vitality",
  "4715-potion-of-water-breathing",
  "9228940-potion-of-water-breathing",
  "4708-potions-of-healing",
  "9058897-quarterstaff-of-the-acrobat",
  "4716-restorative-ointment",
  "4719-ring-of-air-elemental-command",
  "4717-ring-of-animal-influence",
  "4718-ring-of-djinni-summoning",
  "5145-ring-of-earth-elemental-command",
  "5509-ring-of-elemental-command",
  "4720-ring-of-evasion",
  "4721-ring-of-feather-falling",
  "5146-ring-of-fire-elemental-command",
  "4722-ring-of-free-action",
  "4723-ring-of-invisibility",
  "4724-ring-of-jumping",
  "9228966-ring-of-jumping",
  "4725-ring-of-mind-shielding",
  "4726-ring-of-protection",
  "4727-ring-of-regeneration",
  "5420-ring-of-resistance",
  "9341408-ring-of-resistance",
  "4729-ring-of-shooting-stars",
  "4730-ring-of-spell-storing",
  "4731-ring-of-spell-turning",
  "4732-ring-of-swimming",
  "4733-ring-of-telekinesis",
  "4734-ring-of-the-ram",
  "4735-ring-of-three-wishes",
  "4736-ring-of-warmth",
  "9228972-ring-of-warmth",
  "5147-ring-of-water-elemental-command",
  "4737-ring-of-water-walking",
  "9228973-ring-of-water-walking",
  "4738-ring-of-x-ray-vision",
  "4739-robe-of-eyes",
  "4740-robe-of-scintillating-colors",
  "4741-robe-of-stars",
  "4742-robe-of-the-archmagi",
  "4743-robe-of-useful-items",
  "4744-rod-of-absorption",
  "4745-rod-of-alertness",
  "4746-rod-of-lordly-might",
  "5395-rod-of-resurrection",
  "4747-rod-of-rulership",
  "4748-rod-of-security",
  "4749-rope-of-climbing",
  "9228988-rope-of-climbing",
  "4750-rope-of-entanglement",
  "4751-scarab-of-protection",
  "4752-scimitar-of-speed",
  "9180147-sending-stones",
  "5403-sentinel-shield",
  "4754-shield-of-missile-attraction",
  "9058943-shield-of-the-cavalier",
  "4753-shield-1",
  "5157-shield-2",
  "5158-shield-3",
  "4755-slippers-of-spider-climbing",
  "4756-sovereign-glue",
  "5418-spell-scroll",
  "9229085-spell-scroll",
  "4757-spellguard-shield",
  "4759-sphere-of-annihilation",
  "4760-staff-of-charming",
  "4761-staff-of-fire",
  "4762-staff-of-frost",
  "4763-staff-of-healing",
  "4764-staff-of-power",
  "4765-staff-of-striking",
  "4766-staff-of-swarming-insects",
  "4767-staff-of-the-magi",
  "4768-staff-of-the-python",
  "9229102-staff-of-the-python",
  "4769-staff-of-the-woodlands",
  "4770-staff-of-thunder-and-lightning",
  "4771-staff-of-withering",
  "4772-stone-of-controlling-earth-elementals",
  "4773-stone-of-good-luck-luckstone",
  "4774-sun-blade",
  "5390-sword-of-life-stealing",
  "5391-sword-of-sharpness",
  "5392-sword-of-wounding",
  "4778-talisman-of-pure-good",
  "4779-talisman-of-the-sphere",
  "4780-talisman-of-ultimate-evil",
  "9058872-thunderous-greatclub",
  "4781-tome-of-clear-thought",
  "4782-tome-of-leadership-and-influence",
  "4783-tome-of-understanding",
  "4784-trident-of-fish-command",
  "4785-universal-solvent",
  "5399-vicious-weapon",
  "5397-vorpal-sword",
  "4788-wand-of-binding",
  "4789-wand-of-enemy-detection",
  "4790-wand-of-fear",
  "4791-wand-of-fireballs",
  "4792-wand-of-lightning-bolts",
  "4793-wand-of-magic-detection",
  "4794-wand-of-magic-missiles",
  "9237129-wand-of-magic-missiles",
  "4795-wand-of-paralysis",
  "4796-wand-of-polymorph",
  "4797-wand-of-secrets",
  "34712-wand-of-the-war-mage",
  "4799-wand-of-web",
  "4800-wand-of-wonder",
  "5400-weapon-1",
  "5401-weapon-2",
  "5404-weapon-3",
  "4802-well-of-many-worlds",
  "4803-wind-fan",
  "4804-winged-boots",
  "4805-wings-of-flying"
]

for slug in slugs:
    download_page(slug)
    time.sleep(3)
