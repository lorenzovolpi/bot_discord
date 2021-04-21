import requests
from bs4 import BeautifulSoup
import lxml
import discord

URL = "https://dragonball.fandom.com/wiki/" 

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}


def get_img_source(name:str):
    page = requests.get(URL + name, headers=headers)

    soup = BeautifulSoup(page.content, "lxml")

    div = soup.find(id="pi-tab-0")
    img = div.find("img")

    return img["src"]

def save_img(src:str):
    img_page = requests.get(src, headers=headers)

    with open("tmp.jpg", "wb") as image:
        image.write(img_page.content)


async def get_and_send_img(ctx, name):
    src = get_img_source(name)
    save_img(src)

    with open("tmp.jpg", "rb") as image:
        df = discord.File(fp=image, filename="tmp.jpg")
        await ctx.send(file=df)


    
