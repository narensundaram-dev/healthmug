import re


def extract(soup):
    return {
        "brand_name": get_brand_name(soup),
        "drug_name": get_drug_name(soup),
        "pack_size": get_pack_size(soup),
        "images": get_images(soup),
        "company_name": get_company_name(soup),
        "company_logo": get_company_logo(soup),
        "about": get_about(soup),
        "features": get_features(soup),
        "usage_details": get_usage_details(soup),
        "warning_details": get_warning_details(soup),
        "instruction": get_instruction(soup),
        "direction_for_use": get_direction_for_use(soup),
        "dosage": get_dosage(soup),
        "unit": get_unit(soup),
        "mrp": get_mrp(soup),
        "selling_price": get_selling_price(soup),
        "category": get_category(soup),
        "sub_category1": get_sub_category1(soup),
        "sub_category2": get_sub_category2(soup),
        "variants": get_variants(soup),
        "description[do-not-delete]": get_description(soup)
    }


def get_brand_name(soup):
    try:
        return soup.find("a", class_="brandtxtColor").get_text().replace("More from ", "")
    except:
        return "NA"


def get_drug_name(soup):
    try:
        return soup.find("div", class_="prodcutDetailTitle").contents[0].get_text()
    except:
        return "NA"


def get_pack_size(soup):
    try:
        pack_size = ""
        drug_name = get_drug_name(soup)
        matches = list(re.finditer(r"\((\w+)\)", drug_name, re.MULTILINE))
        if matches:
            pack_size = matches[-1].group(1)
        return pack_size
    except:
        return "NA"


def get_images(soup):
    try:
        images = []
        dom_images = soup.find("div", attrs={"id": "m_0"}).find_all("img")
        for dom_image in dom_images:
            images.append(dom_image.attrs["src"])
        return ",".join(images)
    except:
        return "NA"


def get_company_name(soup):
    return get_brand_name(soup)


def get_company_logo(soup):
    try:
        return soup.find("div", class_="productBrandImg").find("img").attrs["src"]
    except:
        return "NA"


def get_about(soup):
    try:
        return soup.find("div", class_="productDetailDesc").find(
            re.compile(r"h[1-6]"), text=re.compile(r".*\babout\b", re.IGNORECASE)).next_sibling.next_sibling.get_text()
    except:
        return "NA"


def get_features(soup):
    try:
        return soup.find("div", class_="productDetailDesc").find(
            re.compile(r"h[1-6]"),
            text=re.compile(r".*\bbenefit\b", re.IGNORECASE)).next_sibling.next_sibling.get_text()
    except:
        return "NA"


def get_usage_details(soup):
    return get_direction_for_use(soup)


def get_warning_details(soup):
    try:
        return soup.find("div", class_="productDetailDesc").find(
            re.compile(r"h[1-6]"),
            text=re.compile(r".*\bprecaution\b", re.IGNORECASE)).next_sibling.next_sibling.get_text()
    except:
        return "NA"


def get_instruction(soup):
    return get_direction_for_use(soup)


def get_direction_for_use(soup):
    try:
        return soup.find("div", class_="productDetailDesc").find(
            re.compile(r"h[1-6]"),
            text=re.compile(r".*direction[\s\w]+\buse", re.IGNORECASE)).next_sibling.next_sibling.get_text()
    except:
        return "NA"


def get_dosage(soup):
    try:
        return soup.find("div", class_="productDetailDesc").find(
            re.compile(r"h[1-6]"), text=re.compile(r".*dosage\b.*", re.IGNORECASE)).next_sibling.next_sibling.get_text()
    except:
        return "NA"


def get_unit(soup):
    try:
        pack_size = get_pack_size(soup)
        return re.sub(r"\d", "", pack_size)
    except:
        return "NA"


def get_mrp(soup):
    try:
        return int(soup.find("span", class_="productBoxMRP").contents[3].get_text().strip())
    except:
        return "NA"


def get_selling_price(soup):
    try:
        return int(soup.find("span", class_="productBoxSellingPrice").get_text().strip())
    except:
        return "NA"


def get_category(soup):
    try:
        return soup.find_all("span", attrs={"itemprop": "name"})[1:][0].get_text()
    except:
        return "NA"


def get_sub_category1(soup):
    try:
        hier_categ = soup.find_all("span", attrs={"itemprop": "name"})[1:]
        return hier_categ[1].get_text() if len(hier_categ) >= 2 else ""
    except:
        return "NA"


def get_sub_category2(soup):
    try:
        hier_categ = soup.find_all("span", attrs={"itemprop": "name"})[1:]
        return hier_categ[2].get_text() if len(hier_categ) >= 3 else ""
    except:
        return "NA"


def get_variants(soup):
    try:
        variants = []
        dom_variants = soup.find("div", class_="variantContent").contents
        for dom_variant in dom_variants:
            variants.append("{} (Rs.{})".format(dom_variant.contents[0].get_text(), dom_variant.contents[1].get_text()))
        return "; ".join(variants)
    except:
        return "NA"


def get_description(soup):
    try:
        return soup.find("div", class_="productDetailDesc").get_text()
    except:
        return "NA"
