import os
import qrcode
from PIL import Image, ImageFont, ImageDraw

os.makedirs("./qr_cards/outputs", exist_ok=True)

# def get_users():
#     try:
#         conn = mysql.connector.connect(**db_config)
#     except Exception as e:
#         print(f"{e} \n --- Error --- ")
#         exit()
#     cursor = conn.cursor()

#     sql = "SELECT DISTINCT name,full_name FROM users WHERE role='USER'"
#     # Untuk melihat yang duplikat : SELECT name,full_name,COUNT(*) FROM users WHERE role='USER' GROUP BY name,full_name HAVING COUNT(*) > 1; 
#     cursor.execute(sql)
#     data = cursor.fetchall()
#     info = {}
#     # JSON
#     for row in data:
#         nis,nama = row
#         info[f"nis-{nis}"] = {"nama":nama,"nis":nis}
#     return info

def make_qr(nis:str):
    qr = qrcode.QRCode(
        version=2,  # Controls the size of the QR Code (1 is smallest, 40 is largest)
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(nis)
    qr.make()
    qr_image = qr.make_image(
        fill_color=(11, 92, 230),
        back_color="white"
    )
    return qr_image

def make_fronts(qr_img:Image, nama:str):
    template = Image.open("./qr_cards/templates/front.png")
    template_width, template_height = template.size

    qr_width, qr_height = qr_img.size
    x_offset = (template_width - qr_width) // 2
    y_offset = (template_height - qr_height) // 2
    position = (x_offset, y_offset)

    font_path = "./qr_cards/fonts/Montserrat-Bold.ttf"
    font_size = 30
    font = ImageFont.truetype(font_path, font_size)

    text = nama.upper()
    text_color = (11, 92, 230)
    border_color = (255, 255, 255)

    draw = ImageDraw.Draw(template)
    text_width = draw.textlength(text, font=font)
    text_height = font_size
    x_position = 110
    y_position = template.height - text_height - 130

    offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # Adjust as needed for thicker borders
    # Draw the border by drawing the text multiple times in the border color
    for offset in offsets:
        draw.text((x_position + offset[0], y_position + offset[1]), text, font=font, fill=border_color)
    draw.text((x_position, y_position), text, font=font, fill=text_color)

    template.paste(qr_img, position)
    # template.show()
    return template

if __name__ == "__main__":
    nis = "1101"
    qr_img = make_qr(nis)
    output = make_fronts(qr_img, "Testing")
    output.save(f"./qr_cards/outputs/card_{nis}.png")
    # data_siswa = get_users()
    # for key,value in data_siswa.items():
    #     qr_image = make_qr(value.get("nis"))
    #     qr_image.show()