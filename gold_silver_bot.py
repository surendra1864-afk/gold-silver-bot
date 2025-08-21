import os
import requests
import datetime
from PIL import Image, ImageDraw, ImageFont
import telegram
from bs4 import BeautifulSoup

# 🔑 Bot Info from GitHub Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ✅ Fetch gold & silver rates from GoodReturns (Bangalore)
def fetch_rates():
    url = "https://www.goodreturns.in/gold-rates/bangalore.html"
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.content, "html.parser")

    gold_elem = soup.find("div", {"class": "gold_silver_table"}).find_all("td")[1]
    gold_rate = float(gold_elem.text.strip().replace("₹", "").replace(",", ""))

    url_silver = "https://www.goodreturns.in/silver-rates/"
    page_silver = requests.get(url_silver, headers={'User-Agent': 'Mozilla/5.0'})
    soup_silver = BeautifulSoup(page_silver.content, "html.parser")

    silver_elem = soup_silver.find("div", {"class": "gold_silver_table"}).find_all("td")[1]
    silver_rate = float(silver_elem.text.strip().replace("₹", "").replace(",", ""))

    return gold_rate, silver_rate

# ✅ Make branded image
def make_image(gold, silver):
    img = Image.new("RGB", (800, 600), color=(255, 253, 245))
    d = ImageDraw.Draw(img)

    # Fonts
    title_font = ImageFont.truetype("arial.ttf", 50)
    rate_font = ImageFont.truetype("arial.ttf", 40)
    small_font = ImageFont.truetype("arial.ttf", 30)

    today = datetime.date.today().strftime("%d %B %Y")

    # Title
    d.text((100, 50), "Dhanlakshmi Jewellers", fill=(139, 0, 0), font=title_font)

    # Rates
    d.text((100, 200), f"Gold (22K / 916): ₹{gold:.2f} per gram", fill=(0, 0, 0), font=rate_font)
    d.text((100, 280), f"Silver (999): ₹{silver:.2f} per gram", fill=(0, 0, 0), font=rate_font)

    # Footer
    d.text((100, 400), f"Date: {today}", fill=(60, 60, 60), font=small_font)
    d.text((100, 450), "Location: Bengaluru", fill=(60, 60, 60), font=small_font)

    img.save("rate.png")

# ✅ Send to Telegram
def job():
    gold, silver = fetch_rates()
    make_image(gold, silver)
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_photo(chat_id=CHAT_ID, photo=open("rate.png", "rb"))

if __name__ == "__main__":
    job()
