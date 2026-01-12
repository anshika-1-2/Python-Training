
import logging
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

logging.basicConfig(
    level=logging.DEBUG,  
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "change-this-in-production"  

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def main():
    """
    Handles GET requests to the site root.
    Renders the index.html template.
    """
    logger.debug("Rendering index page")
    return render_template("index.html")

@app.route("/success", methods=["POST"])
def success():
    """
    Handles POST requests to /success.
    Retrieves a file from the request, saves it,
    and renders Acknowledgement.html with the filename.
    """
    if "file" not in request.files:
        flash("No file part in the request.")
        logger.warning("No file part found in the request")
        return redirect(url_for("main"))

    f = request.files["file"]

    if f.filename == "":
        flash("No file selected.")
        logger.warning("Empty filename submitted")
        return redirect(url_for("main"))

    if allowed_file(f.filename):
        filename = secure_filename(f.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        f.save(save_path)
        logger.debug("File saved to %s", save_path)
        return render_template("Acknowledgement.html", name=filename)
    else:
        flash("File type not allowed.")
        logger.warning("Disallowed file type: %s", f.filename)
        return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(debug=True)
