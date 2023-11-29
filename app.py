import io
import os
from io import BytesIO
from PIL import Image
from flask import *
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/jpgtopng", methods=['GET'])
def jpgtopng():
    return render_template("jpgtopng.html")


@app.route('/pngtojpg', methods=['GET'])
def pngtojpg():
    return render_template('pngtojpg.html')


@app.route('/webptopng', methods=['GET'])
def webptopng():
    return render_template('webptopng.html')


@app.route('/bmptopng', methods=['GET'])
def bmptopng():
    return render_template('bmptopng.html')


@app.route('/compresspdf', methods=['GET'])
def compresspdf():
    return render_template('compresspdf.html')


@app.route('/compressjpg', methods=['GET'])
def compressjpg():
    return render_template('compressjpg.html')


@app.route('/compresspng', methods=['GET'])
def compresspng():
    return render_template('compresspng.html')


@app.route('/api/jpgtopng', methods=['POST'])
def jpg_to_png():
    image_file = request.files['image']

    # Check if the file has an allowed extension (e.g., .jpg or .jpeg)
    allowed_extensions = {'jpg', 'jpeg'}
    if '.' in image_file.filename and image_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return "Invalid file format. Only JPG/JPEG files are allowed.", 400

    try:
        # Open and convert the image to PNG
        image = Image.open(image_file)
        png_bytes = io.BytesIO()
        image.save(png_bytes, format='PNG')
        png_bytes.seek(0)

        # Create a response object with the PNG image as an attachment
        response = Response(png_bytes, mimetype='image/png')
        response.headers['Content-Disposition'] = 'attachment; filename=image.png'

        return response
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/api/pngtojpg', methods=['POST'])
def png_to_jpg():
    image_file = request.files['image']

    # Check if the file has an allowed extension (e.g., .png)
    allowed_extensions = {'png'}
    if '.' in image_file.filename and image_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return "Invalid file format. Only PNG files are allowed.", 400

    try:
        # Open and convert the image to JPG
        image = Image.open(image_file)
        jpg_bytes = io.BytesIO()
        image.convert('RGB').save(jpg_bytes, format='JPEG')
        jpg_bytes.seek(0)

        # Create a response object with the JPG image as an attachment
        response = Response(jpg_bytes, mimetype='image/jpeg')
        response.headers['Content-Disposition'] = 'attachment; filename=image.jpg'

        return response
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/api/webptopng', methods=['POST'])
def webp_to_png():
    image_file = request.files['image']

    # Check if the file has an allowed extension (e.g., .webp)
    allowed_extensions = {'webp'}
    if '.' in image_file.filename and image_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return "Invalid file format. Only WebP files are allowed.", 400

    try:
        # Open and convert the image to PNG
        image = Image.open(image_file)
        png_bytes = io.BytesIO()
        image.convert('RGBA').save(png_bytes, format='PNG')
        png_bytes.seek(0)

        # Create a response object with the PNG image as an attachment
        response = Response(png_bytes, mimetype='image/png')
        response.headers['Content-Disposition'] = 'attachment; filename=image.png'

        return response
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/api/bmptopng', methods=['POST'])
def bmp_to_png():
    image_file = request.files['image']

    # Check if the file has an allowed extension (e.g., .bmp)
    allowed_extensions = {'bmp'}
    if '.' in image_file.filename and image_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return "Invalid file format. Only BMP files are allowed.", 400

    try:
        # Open and convert the image to PNG
        image = Image.open(image_file)
        png_bytes = io.BytesIO()
        image.save(png_bytes, format='PNG')
        png_bytes.seek(0)

        # Create a response object with the PNG image as an attachment
        response = Response(png_bytes, mimetype='image/png')
        response.headers['Content-Disposition'] = 'attachment; filename=image.png'

        return response
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/api/compressjpg', methods=['POST'])
def compress_jpg():
    image_file = request.files['image']

    # Check if the file has an allowed extension (e.g., .jpg or .jpeg)
    allowed_extensions = {'jpg', 'jpeg'}
    if '.' in image_file.filename and image_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return "Invalid file format. Only JPG/JPEG files are allowed.", 400

    try:
        # Open and compress the JPG image
        image = Image.open(image_file)
        compressed_jpg_bytes = io.BytesIO()
        image.save(compressed_jpg_bytes, format='JPEG', quality=85)

        # Create a response object with the compressed JPG image as an attachment
        response = Response(compressed_jpg_bytes.getvalue(), mimetype='image/jpeg')
        response.headers['Content-Disposition'] = 'attachment; filename=image_compressed.jpg'

        return response
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/api/compresspdf', methods=['POST'])
def compress_pdf():
    # Check if the 'pdf' parameter exists in the POST request
    if 'pdf' not in request.files:
        return "No 'pdf' parameter provided in the request", 400

    pdf_file = request.files['pdf']

    try:
        # Open the PDF file using PyPDF2
        pdf_buffer = pdf_file.read()
        pdf_reader = PdfReader(io.BytesIO(pdf_buffer))

        # Create a BytesIO buffer to store the compressed PDF
        compressed_pdf_buffer = io.BytesIO()
        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        # Write the compressed PDF to the output buffer
        pdf_writer.write(compressed_pdf_buffer)
        compressed_pdf_buffer.seek(0)

        # Calculate the original and compressed file sizes
        original_size = len(pdf_buffer)
        compressed_size = len(compressed_pdf_buffer.getvalue())

        # Set the appropriate response headers for a PDF file
        response = Response(compressed_pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=compressed.pdf'

        # Include file size information in the response headers
        response.headers['Original-File-Size'] = str(original_size)
        response.headers['Compressed-File-Size'] = str(compressed_size)

        return response

    except Exception as e:
        return "Error compressing PDF: " + str(e), 400


@app.route('/api/compresspng', methods=['POST'])
def compress_png():
    image_file = request.files['image']

    try:
        image = Image.open(image_file)
        image = image.convert("RGB")
        png_bytes = io.BytesIO()
        image.save(png_bytes, format='PNG', size=70)
        png_bytes.seek(0)

        # Create a response object with the PNG image as an attachment
        response = Response(png_bytes, mimetype='image/png')
        response.headers['Content-Disposition'] = 'attachment; filename=image-compressed.png'

        return response

        # Set the appropriate response headers for a PNG file

    except Exception as e:
        return "Error compressing PNG image: " + str(e), 400


if __name__ == '__main__':
     http_server = WSGIServer (('', 5000), app)
     http_server.serve_forever()
