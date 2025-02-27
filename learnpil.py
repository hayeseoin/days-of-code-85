from PIL import Image

def main():
    img = Image.open('excellent-cat.jpeg')
    watermark = Image.open('watermark.png')
    watermark_new_size: tuple[int, int] = (int(img.width*0.5), int(img.height*0.5))
    resized_watermark = watermark.resize(watermark_new_size)
    img.paste(
        resized_watermark, 
        (0,0),
        resized_watermark)
    img.show()


if __name__ == "__main__":
    main()