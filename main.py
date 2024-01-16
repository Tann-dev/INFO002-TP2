from PIL import Image, ImageFont, ImageDraw
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

def hide(img, msg):
    pixels = img.load()             # tableau des pixels
    w, h = img.size                 # dimensions de l'image
    i = 0                           # indice dans le message
    bi = 0                           # indice dans le bit du message
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]  # on récupère les composantes RGB du pixel (x,y)
            bit = (ord(msg[i]) >> bi) & 1
            r = r & 0xfe | bit
            pixels[x, y] = (r, g, b)
            bi += 1
            if bi == 8:
                bi = 0
                i += 1
                if i == len(msg):
                    return img

def unhide(img, size):
    pixels = img.load()             # tableau des pixels
    w, h = img.size                 # dimensions de l'image
    msg = [0 for i in range(size)]
    i = 0                           # indice dans le message
    bi = 0                           # indice dans le bit du message
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]  # on récupère les composantes RGB du pixel (x,y)
            bit = r & 1
            msg[i] |= bit << bi
            bi += 1
            if bi == 8:
                bi = 0
                i += 1
                if i == size:
                    return msg

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
    output_file = open("signature.pkcs", "wb")
    output_file.write(signature)
    output_file.close()

def verify(msg):
    file_in = open("signature.pkcs", "rb")
    signature = file_in.read()
    file_in.close()
    public_key = RSA.import_key(open("public_key.pem").read())
    try:
        pkcs1_15.new(public_key).verify(SHA256.new(msg), signature)
        print("The signature is valid.")
    except (ValueError, TypeError):
        print("The signature is not valid.")
    

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
        dec_msg = verify(msg)
