from flask import Flask, render_template, request, url_for, redirect
from tkinter import messagebox
from flask_bootstrap import Bootstrap
from PIL import Image
import urllib
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


have_details=False
url_link=True
@app.route("/")
def home():
    global have_details
    have_details=False
    
    return render_template("index.html", have_details=have_details)

@app.route('/extract_color', methods=['GET','POST'])
def extract_color():
    global have_details, url_link
    have_details=True

    img_url=request.form['img_url']
    if img_url == "":
        url_link=False
        image_file=request.files['file']
        if image_file == "":
            return "Please give a valid image"
        filename=secure_filename(image_file.filename)
        image_file.save(os.path.join('static/',filename))
        image=Image.open(image_file)
        
    else:
        url_link=True
        image = Image.open(urllib.request.urlopen(img_url))


    reduced = image.convert("P", palette=Image.Palette.WEB) # convert to web palette (216 colors)
    palette = reduced.getpalette() # get palette as [r,g,b,r,g,b,...]
    palette = [tuple(palette[3*n:3*n+3]) for n in range(256)] # group 3 by 3 = [[r,g,b],[r,g,b],...]
    color_count = [(n, palette[m]) for n,m in reduced.getcolors()]

    color_count.sort()
    top_10_extracted_colors=color_count[::-1][:10]
    
    return render_template("index.html", have_details=have_details, colors=top_10_extracted_colors, img_url=img_url, url_link=url_link, filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
