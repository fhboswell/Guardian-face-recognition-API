# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of Barack Obama.
# The result is returned as json. For example:
#
# $ curl -F "file=@obama2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_obama": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import face_recognition
from flask import Flask, jsonify, request, redirect
import sys

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    # Not Python 3 - today, it is most likely to be Python 2
    # But note that this might need an update when Python 4
    # might be around one day
    from urllib import urlopen

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    print(content['one'])
    
    
    
    unknown = urlopen(content['unknown'])
    unknown_img = face_recognition.load_image_file(unknown)
    
    
    unknown_face_encoding = face_recognition.face_encodings(unknown_img)[0]
    
   
    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    
    known_faces = []
    name = "name"
    names = ["No Name"] * int(content['numfaces'])
    for i in range(int(content['numfaces'])):
        known = urlopen(content[str(i)])
        known_img = face_recognition.load_image_file(known)
        known_face_encoding = face_recognition.face_encodings(known_img)[0]
        known_faces.append(known_face_encoding)
        name = "name" + str(i)
        names[i] = content[name]
    
    
    
    
    results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
    
    for i in range(len(results)):
        if results[i]:
            return jsonify({"same":str(names[i])})
    
    
    return jsonify({"same":"neg"})


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Guardian Face Recognition API</title>
    <h1>Guardian</h1>
    <p>
    {
    "unknown":"zzz",
    "numfaces":"zzz",
    "0":"zzz",
    "name0":"zzz",
    "one":"zzz"
    }
    </p>
    '''



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
