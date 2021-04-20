import io
from bs4 import BeautifulSoup
import lxml
import requests
import discord

URL = "https://dragonball.fandom.com/wiki/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}


def get_proper_name(names):
    ln = [str(x[0]).upper() + x[1:].lower() for x in names]
    return " ".join(ln), "_".join(ln)

def find_src(soup):
    return soup.find(id="mw-content-text") \
            .find("aside") \
            .find("figure") \
            .find("img")["src"]

def get_string(tag):
    res = ""
    try:
        contents = tag.contents 

        for c in contents:
            try:
                if c["id"] == "toc":
                    break
            except:
                pass 


            if len([x for x in ["dl", "table", "aside"] if x == c.name]) == 0:
                res += get_string(c)

            
    except AttributeError as _:
        res += tag
    
    return res


def find_text(soup, name):
    text_tag = soup.find(id="mw-content-text") \
            .find("div")

    text = get_string(text_tag).strip()
    start = text.find(name)

    return text[start:]



async def get_soup(name:str):
    page = requests.get(URL+name, headers=headers)

    return BeautifulSoup(page.content, "lxml")

 
async def fetch_and_reply(ctx, names):
    name, uname = get_proper_name(names)

    soup = await get_soup(uname)

    reply = ""
    try:
        src = find_src(soup) 
        text = find_text(soup, name)

        reply = text
        reply += "\n\n"
        reply += "Here's a pic of " + name

        image = requests.get(src, headers=headers)
        with io.BytesIO(image.content) as img:
            await ctx.send(reply, file=discord.File(fp=img, filename=name + ".jpg"))

    except AttributeError as ae:
        reply = name + " is not in the radar"
        await ctx.send(reply)



