from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request, redirect
from bson.objectid import ObjectId

app = Flask(__name__)

uri = "mongodb+srv://<username>:<password>@<cluster_name>.xetvd.mongodb.net/?retryWrites=true&w=majority&appName=<cluster_name>"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['note_app']
notes_collection = db['notes']

@app.route('/')
def home():
  all_notes = notes_collection.find()
  return render_template('home.html', notes = all_notes)

@app.route('/add', methods=['GET','POST'])
def add_note():
  if request.method == 'POST':
    new_note = {
      'cwid' : request.form['cwid'],
      'full_name' : request.form['full_name'],
    }
    notes_collection.insert_one(new_note)
    return redirect('/')
  return render_template('home.html')

@app.route('/delete/<note_id>')
def delete_note(note_id):
  print(f"Received note_id: {note_id}")
  notes_collection.delete_one({'_id' : ObjectId(note_id)})
  return redirect('/')

if __name__ == '__main__':
  app.run(debug=True)