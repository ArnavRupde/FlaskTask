from flask import Flask, request, redirect, url_for, render_template, send_from_directory, Response 
from werkzeug.utils import secure_filename
import os
import pandas as pd
import xlsxwriter

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['UPLOADED_FILE'] = "abc"

def process_file_plasmogen(path, filename):
  print("path= ")
  print(str(path))
  df = pd.read_excel(path)
  # print(df)
  df2 = df[df['Accepted Compound ID'].str.endswith("plasmalogen", na=False)]
  print(df2)
  return Response(
       df2.to_csv(),
       mimetype="text/csv",
       headers={"Content-disposition":
       "attachment; filename=plasmalogen.csv"})

def process_file_lpc(path, filename):
  print("path= ")
  print(str(path))
  df = pd.read_excel(path)
  # print(df)
  df2 = df[df['Accepted Compound ID'].str.endswith("LPC", na=False)]
  print(df2)
  return Response(
       df2.to_csv(),
       mimetype="text/csv",
       headers={"Content-disposition":
       "attachment; filename=lpc.csv"})

def process_file_pc(path, filename):
  print("path= ")
  print(str(path))
  df = pd.read_excel(path)
  # print(df)
  df2 = df[df['Accepted Compound ID'].str.endswith("PC", na=False)]
  print(df2)
  return Response(
       df2.to_csv(),
       mimetype="text/csv",
       headers={"Content-disposition":
       "attachment; filename=pc.csv"})

def process_file_getroundoff(path, filename):
  print("path= ")
  print(str(path))
  df = pd.read_excel(path)
  # print(df)
  df['Retention Time Roundoff (in mins)']=round(df['Retention time (min)'].astype(float)).astype(int)
  return Response(
       df.to_csv(),
       mimetype="text/csv",
       headers={"Content-disposition":
       "attachment; filename=task2.csv"})

def process_file_getmean(path, filename):
  print("path= ")
  print(str(path))
  df = pd.read_excel(path)
  # print(df)
  df['Retention Time Roundoff (in mins)']=round(df['Retention time (min)'].astype(float)).astype(int)
  del df['m/z']
  del df['Accepted Compound ID']
  del df['Retention time (min)']
  df2= df.groupby(['Retention Time Roundoff (in mins)']).mean()
  return Response(
       df2.to_csv(),
       mimetype="text/csv",
       headers={"Content-disposition":
       "attachment; filename=task3.csv"})

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':
       if 'file' not in request.files:
           print('No file attached in request')
           return redirect(request.url)
       file = request.files['file']
       if file.filename == '':
           print('No file selected')
           return redirect(request.url)
       if file:
           filename = secure_filename(file.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           # process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
           print("Here")
           app.config['UPLOADED_FILE'] = filename
           # return redirect(url_for('uploaded_file', filename=filename))
           return render_template('fileuploadsuccess.html')
   return render_template('index.html')

@app.route('/getplasmogen', methods=['GET', 'POST'])
def getplasmogen():

  return process_file_plasmogen(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOADED_FILE']), app.config['UPLOADED_FILE'])
  return render_template('index.html')

@app.route('/getlpc', methods=['GET', 'POST'])
def getlpc():

  return process_file_lpc(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOADED_FILE']), app.config['UPLOADED_FILE'])
  return render_template('index.html')

@app.route('/getpc', methods=['GET', 'POST'])
def getpc():

  return process_file_pc(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOADED_FILE']), app.config['UPLOADED_FILE'])
  return render_template('index.html')

@app.route('/getroundoff', methods=['GET', 'POST'])
def getroundoff():
  return process_file_getroundoff(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOADED_FILE']), app.config['UPLOADED_FILE'])
  return render_template('index.html')

@app.route('/getmean', methods=['GET', 'POST'])
def getmean():
  return process_file_getmean(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOADED_FILE']), app.config['UPLOADED_FILE'])
  return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print("Here2")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=5000)