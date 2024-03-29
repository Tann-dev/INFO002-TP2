from PIL import Image, ImageFont, ImageDraw
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from datetime import date
import locale

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

def hide(img, sign):
    print("Taile de la signature : " + str(len(sign)))
    if img.mode != "RGB":
        img = img.convert("RGB")
    pixels = img.load()
    w, h = img.size
    i = 0
    bi = 0
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            bit = (sign[i] >> bi) & 1
            r = r & 0xfe | bit
            pixels[x, y] = (r, g, b)
            bi += 1
            if bi == 8:
                bi = 0
                i += 1
                if i == len(sign):
                    return img

def unhide(img, size):
    pixels = img.load()
    w, h = img.size
    sign = bytearray(size)
    i = 0
    bi = 0
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            bit = r & 1
            sign[i] = sign[i] | (bit << bi)
            bi += 1
            if bi == 8:
                bi = 0
                i += 1
                if i == size:
                    return sign
            

def generate_key():
    key = RSA.generate(4096)
    private_key = key.export_key("PEM")
    public_key = key.publickey().export_key("PEM")

    file_out = open("private_key.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    file_out = open("public_key.pem", "wb")
    file_out.write(public_key)
    file_out.close()

def signMessage(msg):
    hash = SHA256.new(msg)
    private_key = RSA.import_key(open("private_key.pem").read())
    signature = pkcs1_15.new(private_key).sign(hash)
    return signature

def verify(msg, signature):
    public_key = RSA.import_key(open("public_key.pem").read())
    try:
        pkcs1_15.new(public_key).verify(SHA256.new(msg), signature)
        print("The signature is valid.")
    except (ValueError, TypeError):
        print("The signature is not valid.")

def add_degree_label(img):
    msg = "Diplôme"
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font.ttf", 70)
    _, _, w, h = draw.textbbox((0, 0), msg, font=font)
    draw.text(((img.width - w) / 2, 150), msg, "black", font)

def add_degree_name(img):
    msg = "Master Bacon Grill"
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font.ttf", 52)
    _, _, w, h = draw.textbbox((0, 0), msg, font=font)
    draw.text(((img.width - w) / 2, 240), msg, "black", font)

def add_candidate_name(img, candidate_name):
    msg = candidate_name + " a réussi la formation"
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font2.otf", 36)
    _, _, w, h = draw.textbbox((0, 0), msg, font=font)
    draw.text(((img.width - w) / 2, 320), msg, "black", font)

def add_grade_mean(img, grade_mean):
    msg = "avec une moyenne de  " + grade_mean
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font2.otf", 36)
    _, _, w, h = draw.textbbox((0, 0), msg, font=font)
    draw.text(((img.width - w) / 2, 380), msg, "black", font)

def add_emission_date(img):
    msg = "Diplôme émis le  " + date.today().strftime('%A %d %B %Y')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font3.otf", 28)
    _, _, w, h = draw.textbbox((0, 0), msg, font=font)
    draw.text(((img.width - w) /4 * 3, 450), msg, "black", font)

def create_degree(filename, output, student_name, mean_student):
    img = Image.open(filename)  # ouverture de l'image contenue dans un fichier
    add_degree_label(img)
    add_degree_name(img)
    add_candidate_name(img, student_name)
    add_grade_mean(img, mean_student)
    add_emission_date(img)
    now = date.today()
    msg = str(now) + student_name + mean_student
    sign = signMessage(msg.encode())
    img = hide(img, sign)
    img.save(output)            # sauvegarde de l'image obtenue dans un autre fichier

def verify_degree(filename, msg, size):
    img = Image.open(filename)
    sign = unhide(img, size)
    verify(msg.encode(), sign)
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <function to call> ...")
        sys.exit(1)
    if sys.argv[1] == "hide":
        if len(sys.argv) != 5:
            print("Usage: python main.py hide <input image> <message> <output image>")
            sys.exit(1)
        img = Image.open(sys.argv[2])
        msg = sys.argv[3]
        image = hide(img, msg)
        image.save(sys.argv[4])
    elif sys.argv[1] == "unhide":
        if len(sys.argv) != 4:
            print("Usage: python main.py unhide <input image> <size>")
            sys.exit(1)
        img = Image.open(sys.argv[2])
        size = int(sys.argv[3])
        msg = unhide(img, size)
        print("".join(chr(c) for c in msg))
    elif sys.argv[1] == "generate_key":
        generate_key()
    elif sys.argv[1] == "sign":
        if len(sys.argv) != 3:
            print("Usage: python main.py sign <message>")
            sys.exit(1)
        msg = sys.argv[2]
        signMessage(msg.encode())
    elif sys.argv[1] == "verify":
        if len(sys.argv) != 3:
            print("Usage: python main.py verify <msg>")
            sys.exit(1)
        msg = sys.argv[2]
        dec_msg = verify(msg.encode())
    elif sys.argv[1] == "make_degree":
        if len(sys.argv) != 6:
            print("Usage: python main.py test_degree <input image> <output image> <student_name> <mean_student>")
        create_degree(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif sys.argv[1] == "verify_degree":
        if len(sys.argv) != 5:
            print("Usage: python main.py verify_degree <input image> <msg> <size>")
        verify_degree(sys.argv[2], sys.argv[3], int(sys.argv[4]))

