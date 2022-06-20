import os
from flask import Flask, flash, request, redirect, url_for, Response
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import potrace
import cv2
import json
import uuid


"""
The original code that converts the image into graphs were developed by
https://github.com/kevinjycui/DesmosBezierRenderer
Special thanks to kevinjycui for the original code.

This code uses following functions from the original DesmosBezierRenderer
- get_trace
- get_latex
- get_contours

This code added some features so that it is possible to run a API that turns
given image by POST request into a series of graphs.
Please check https://github.com/gooday2die/DesmosPic for more information
"""



COLOUR = '#2464b4' # Hex value of colour for graph output
BILATERAL_FILTER = False # Reduce number of lines with bilateral filter
USE_L2_GRADIENT = False # Creates less edges but is still accurate (leads to faster renders)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)

def get_trace(data):
    for i in range(len(data)):
        data[i][data[i] > 1] = 1
    bmp = potrace.Bitmap(data)
    path = bmp.trace(2, potrace.TURNPOLICY_MINORITY, 1.0, 1, .5)
    return path


def get_latex(filename):
    latex = []
    path = get_trace(get_contours(filename))

    for curve in path.curves:
        segments = curve.segments
        start = curve.start_point
        for segment in segments:
            x0, y0 = start
            if segment.is_corner:
                x1, y1 = segment.c
                x2, y2 = segment.end_point
                latex.append('((1-t)%f+t%f,(1-t)%f+t%f)' % (x0, x1, y0, y1))
                latex.append('((1-t)%f+t%f,(1-t)%f+t%f)' % (x1, x2, y1, y2))
            else:
                x1, y1 = segment.c1
                x2, y2 = segment.c2
                x3, y3 = segment.end_point
                latex.append('((1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)),\
                (1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)))' % \
                (x0, x1, x1, x2, x1, x2, x2, x3, y0, y1, y1, y2, y1, y2, y2, y3))
            start = segment.end_point
    return latex

def get_contours(image, nudge = .33):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if BILATERAL_FILTER:
        median = max(10, min(245, np.median(gray)))
        lower = int(max(0, (1 - nudge) * median))
        upper = int(min(255, (1 + nudge) * median))
        filtered = cv2.bilateralFilter(gray, 5, 50, 50)
        edged = cv2.Canny(filtered, lower, upper, L2gradient = USE_L2_GRADIENT)
    else:
        edged = cv2.Canny(gray, 30, 200)

    return edged[::-1]


def generate_js(result):
    """
    A function that generates html code that has javascript code that represents
    the function using Desmos API.

    While trying to fit Desmos graph into our website, there was a wierd bug.
    This was fixed via modifying the original calculator.js.
    The modified calculator.js is stored and hosted in local machine and was
    named as modified.js

    :param results: a list that has all the latex expressions of the picture.
    :return: returns a string object that represnts all javascript expressions
             for visualizing Desmos graph
    """

    js_base = """
    <script src="./modified.js"></script>
    <div id="calculator" style="width: 1980px, height: 1080px;"></div>
    <script type='text/javascript'>
    var elt = document.getElementById('calculator');
    var calculator = Desmos.GraphingCalculator(elt);
    """

    js_end = "</script>"

    set_exprs = list()
    expr_count = 0
    for i in result:
        cur_expr =  "calculator.setExpression({ id: 'expr-" + str(expr_count) +\
            "\', latex: \'" + i + "\', color: \'" + COLOUR + "\'});\n"
        expr_count += 1
        set_exprs.append(cur_expr)
    js_result = js_base

    for i in set_exprs:
        js_result += i.replace(" ", "")
    js_result += js_end

    return js_result

def generate_function_text(result):
    """
    A function that generates a textarea HTML that includes all functions.

    :param results: a list that has all the latex expressions of the picture.
    :return: returns a string object that represnts HTML code of textarea.
    """

    text_base = "<textarea class=\"form-control\" id=\"message\" name=\"message\" rows=\"7\">"

    text_end = "</textarea>"
    text_result = text_base

    for i in result:
        text_result += i.replace(" ", "") + "\n"

    text_result += text_end
    return text_result

def allowed_file(filename):
    """
    A function that figures out if this file is allowed file extension
    :param filename: the string object that represents file's name
    :return: returns valid or not
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(js_result):
    """
    """
    uuid_name = str(uuid.uuid4())
    f = open("/var/www/Gooday2die/DesmosPics/saves/" + uuid_name + ".html", "w+")
    f.write(js_result)
    f.close()
    return

@app.route('/pic', methods=['GET', 'POST'])
def pic():
    """
    A function that is for pic route.
    This member function will take care of POST requests using images.
    When the image was valid and could be processed, it will return a
    json object that is in following format.

    {'js_result': "string that has all javascript codes",
    'text_results': "string that has all HTML codes for textarea"}
    """

    if request.method == 'POST':  # if this was POST request,
        try:
            img = cv2.imdecode(np.frombuffer(request.files['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
            result = get_latex(img)
            js_result = generate_js(result)
            text_result = generate_function_text(result)

            total_data = {"js_result": js_result, "text_result": text_result}
            json_result = json.dumps(total_data)
            save_file(js_result)

            return Response(json_result, status=200)
        except:  # if the POST request was invalid
            return Response("[Error] File is invalid or cannot process file. Please submit an issue", status=400)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="0.0.0.0", port=5001)
