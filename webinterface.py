from flask import Flask, request, render_template
import subprocess
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)


@app.route("/")
def index():
    title = request.args.get("title")
    if title is not None:
        feedback1, feedback2 = addToSchedule(title, request.args.get("source"), request.args.get("startDate"), request.args.get("stopDate"))
    else:
        feedback1 = ""
        feedback2 = ""
    return render_template("main.html", feedback1 = feedback1, feedback2 = feedback2)

def addToSchedule(title, source, startDate, stopDate):
    try:
        _startDate = str(startDate).split("T")  # _startDate[0]: YYYY-MM-DD ; _startDate[1]: hh:mm
        _stopDate = str(stopDate).split("T") 
        _title = _startDate[0] + " - " + str(title)
        _source = int(source)
        startPrompt = """echo \"sh startRecording.sh """ + str(_source) + " \'" + _title + """\'\" | at """ + _startDate[1] + " " + _startDate[0]
        stopPrompt = """echo \"sh stopRecording.sh \" | at """ + _stopDate[1] + " " + _stopDate[0]
        stream = subprocess.Popen(startPrompt, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (_, errStart) = stream.communicate()
        stream = subprocess.Popen(stopPrompt, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (_, errStop) = stream.communicate()
        return (errStart.decode("ASCII"), errStop.decode("ASCII"))
    except Exception as error:
        return "Invalid" + str(error)


if __name__ == '__main__':
    app.run(host = "127.0.0.1", port = 8080, debug = True)
