import easyocr
from PIL import Image,ImageDraw
 
reader = easyocr.Reader(['ch_sim','en'], gpu=False, model_storage_directory='./test')
result = reader.readtext('./test/9_28_16_24_47.png')

print(result)

img = Image.open('./test/9_28_16_24_47.png')
draw = ImageDraw.Draw(img)
 
for i in result:
    print(tuple(i[0][0]), tuple(i[0][2]))
    draw.rectangle((tuple(i[0][0]),tuple(i[0][2])),fill=None,outline='red',width=2)
img.save("./test/ceshi_out.png")