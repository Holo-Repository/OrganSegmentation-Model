from flask import Flask, request, send_file

from models.dense_vnet_abdominal_ct.model import abdominal_model

app = Flask(__name__)

# The directory paths are given by the original model in the container

UPLOAD_FOLDER = "/models/dense_vnet_abdominal_ct/input"
OUTPUT_FOLDER = "/models/dense_vnet_abdominal_ct/output"

ALLOWED_EXTENSION = "nii"
UPLOAD_FILENAME = "seg_CT.nii"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER


def file_format_is_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == ALLOWED_EXTENSION


def format_output_filename(filename):
    filename_noextension = filename.split("_")[0]
    return filename_noextension + "__niftynet_out.nii.gz"


@app.route("/model", methods=["POST"])
def seg_file():
    if "file" not in request.files:
        return "No file in the request", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if file and file_format_is_allowed(file.filename):
        if file.filename != UPLOAD_FILENAME:
            file.filename = UPLOAD_FILENAME

        output_path = abdominal_model.predict(file)  
        
        return send_file(output_path, mimetype="application/octet-stream", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1")
