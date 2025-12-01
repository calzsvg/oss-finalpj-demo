import os
import asyncio

import cv2
import discord
from dotenv import load_dotenv

from grayscale.preprocessor import grayscale_image

load_dotenv()
DI_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

def to_gray_image(input_path: str, output_path: str):

    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("이미지 읽기 실패")

    max_width = 1920
    h, w = img.shape[:2]
    if w > max_width:
        scale = max_width / w
        new_h = int(h * scale)
        img = cv2.resize(img, (max_width, new_h), interpolation=cv2.INTER_AREA)

    gray = grayscale_image(img)

    cv2.imwrite(output_path, gray, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

@bot.event
async def on_ready():
    print(f"로그인 완료: {bot.user}")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if not message.attachments:
        return

    for attachment in message.attachments:
        filename = attachment.filename.lower()

        if any(filename.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif",".webp"]):
            await image_attach(message, attachment)
        
        elif any(filename.endswith(ext) for ext in [".mp4", ".mov", ".avi", ".mkv"]):
            await message.channel.send("")


async def image_attach(message: discord.Message, attachment: discord.Attachment):
    ori_path = f"temp_original_{attachment.id}.png"
    gray_path = f"temp_gray_{attachment.id}.jpg"

    try:
        byte = await attachment.read()
        with open(ori_path, "wb") as f:
            f.write(byte)

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, to_gray_image, ori_path, gray_path)

        if os.path.getsize(gray_path) >= 8 * 1024 * 1024:
             await message.channel.send("8MB이상은 못올립니다.")
        else:
            await message.channel.send(
                content=f"{message.author.mention} 변환 성공",
                file=discord.File(gray_path))

    except Exception as e:
        print("에러:", e)
        await message.channel.send("오류 발생")
    finally:
        for path in [ori_path, gray_path]:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    bot.run(DI_TOKEN)
