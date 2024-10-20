from PIL import Image, ImageFont, ImageDraw#, ImageFilter

class Makecard:
    def __init__(
        self,
        image="card image.png",
        face="face.png",
        output="card.png",
        text_list=[
            'Id',
            'phone',
            'full name',
            'bird',
            'country',
            'city',
            'gender',
            'job',
            'web',
            'mail',
            'address']
        ):
        
        self.image = image
        self.face = face
        self.output = output
        self.text = text_list
        self.position = (44,50) # face positiion
        self.start()

    def start(self):
        # paste face
        base_image = Image.open(self.image).convert('RGBA')
        face = Image.open(self.face).convert('RGBA')
        face = face.resize((139,150))
        #face.putalpha(130)
        width, height = base_image.size
        card = Image.new('RGBA', (width, height), (0,0,0,0))
        card.paste(base_image, (0,0))
        card.paste(face, self.position, mask=face)

        #--------- write text ----------
        draw = ImageDraw.Draw(card)
        font = ImageFont.truetype("./media/fonts/neuropolitical rg.ttf", 14)
        # write id and phone
        y = 220 # y position
        for line in self.text[:3:]:
            draw.text((55,y), line[:29:], (153, 230, 255), font=font)
            y += 20
 
        # write the rest of info, Not the address
        y = 50 # y position
        for line in self.text[3:-1:]:
            draw.text((210,y), line[:29:], (200, 255, 255), font=font)
            y += 20


            
        # write long address start new line if text len is bigger than 26
        comment = self.text[-1::][0]
        text_len = len(comment)
        if text_len > 0:
            line_len = 24
            y = 210
            while True:
                draw.text((250,y), comment[line_len - 24:line_len:], (200, 255, 255), font=font)
                if line_len > text_len:
                    break
                line_len += 24
                y += 20
                
            
        card.save(self.output)


    
if __name__ == '__main__':
    # test
    Makecard(
        image='./media/card.png',
        face='./media/opencamera.png',
        output="card.png",
        text_list=["0011334400","+50377777777","+50377777777","erick esau martinez", "29/01/1990", "El salvador","Cuidad barrios", "hombre", "Programador", "www.erickesau.wordpress.com", "martinezesau90@gmail.com","san miguel ciudad barrios",]
        )


