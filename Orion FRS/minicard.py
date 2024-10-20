from PIL import Image, ImageFont, ImageDraw#, ImageFilter

class Minicard:
    def __init__(self, image="", face="", output="card.png", text_list=[" "]):
        self.image = image
        self.face = face
        self.output = output
        self.text = text_list
        self.position = (14,19)
        self.start()

    def start(self):
        # paste face
        base_image = Image.open(self.image).convert('RGBA')
        face = Image.open(self.face).convert('RGBA')
        face = face.resize((110,125))
        #face.putalpha(130)
        width, height = base_image.size
        card = Image.new('RGBA', (width, height), (0,0,0,0))
        card.paste(base_image, (0,0))
        card.paste(face, self.position, mask=face)

        #--------- write text ----------
        draw = ImageDraw.Draw(card)
        font = ImageFont.truetype("./media/fonts/neuropolitical rg.ttf", 11)
        n = 15
        for line in self.text:
            draw.text((125,n), line[:19:], (153, 230, 255), font=font)
            n += 12
            if n >= 120:
                break
        card.save(self.output)


    
if __name__ == '__main__':
    # test
    Minicard(
        image='./media/minicard.png',
        face='./media/opencamera.png',
        output="card.png",
        text_list=["erick esau martinez", "fgfghggfddf", "prueba","erick esau", "programador", "prueba"]
        )


