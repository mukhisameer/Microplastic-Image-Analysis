import os
import sys
import pathlib
# To enable importing module from the "src" folder
sys.path.insert(0, '../src')
import ImageProcessing as imgP
from zipfile import ZipFile
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename


UPLOADED = 'uploadedfiles'
UNZIPPED = 'unzippedfiles'
ANALYZED = 'analyzedfiles'
CURRENT_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(CURRENT_DIR, UPLOADED)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'zip'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["DEBUG"] = True
app.secret_key = 'super secret key'


@app.route('/')
def index():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['POST', 'GET'])
def upload_file():
    error = None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return render_template("index.html", error="No file is selected!")
            # print("No selected file:",file=sys.stderr)
            # flash('No selected file')
            # return redirect(url_for('index',error="No file Selected."))
        if not allowed_file(file.filename):
            return render_template("index.html", error=f"Allowed file types are:{ALLOWED_EXTENSIONS}")

        if file:
            filename = secure_filename(file.filename)
            check_directory(UPLOAD_FOLDER)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return ''


def check_directory(path):
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        os.chmod(path, 0o777)


@app.route(f'/{UPLOADED}/<filename>')
def uploaded_file(filename):
    file_path = app.config['UPLOAD_FOLDER']+'/'+filename
    file_name, file_ext = os.path.splitext(filename)
    if file_ext == '':
        return "The file has no extension!"

    if file_ext == '.zip':
        path_to_processingImg = CURRENT_DIR+f'/{UNZIPPED}/'+file_name
        with ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(path_to_processingImg)

        saving_location = CURRENT_DIR+f'/{ANALYZED}/'+file_name
        check_directory(saving_location)
        img_dir = pathlib.Path(path_to_processingImg)
        for item in img_dir.iterdir():
            if item.is_file():
                head, tail = os.path.split(item)
                imgProc = imgP.ImageProcessing(str(item))
                img = imgProc.getContours()
                imgProc.saveImage(img, str(tail), saving_location)

        img_saved_dir = pathlib.Path(saving_location)
        zip_file_name = file_name+'_analyzed.zip'
        with ZipFile(zip_file_name, 'w') as zipped:
            for item in img_saved_dir.iterdir():
                head, tail = os.path.split(item)
                if tail != zip_file_name:
                    zipped.write(str(tail))
    else:
        saving_location = CURRENT_DIR+f'/{ANALYZED}'
        check_directory(saving_location)
        path_to_processingImg = CURRENT_DIR+f'/{UPLOADED}'
        imgProc = imgP.ImageProcessing(path_to_processingImg+'/'+str(filename))
        img = imgProc.getContours()
        imgProc.saveImage(
            img, str(file_name+'_analyzed'+file_ext), saving_location)

    return redirect(url_for('analyzed_file',
                            file_name=filename))


@app.route('/analyzed_file/<file_name>', methods=['POST', 'GET'])
def analyzed_file(file_name):
    return render_template("index.html", file_name=file_name)


@app.route('/download/<file_name>')
def download_file(file_name):
    name, ext = os.path.splitext(file_name)
    if ext == '.zip':
        download_link = CURRENT_DIR+f"/{ANALYZED}/{name}/{name}_analyzed.zip"
    else:
        download_link = CURRENT_DIR+f"/{ANALYZED}/{name}_analyzed"+ext
    return send_file(download_link, as_attachment=True)
