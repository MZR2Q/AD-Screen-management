from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
import random



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def all():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM images WHERE for='all'")
    images = c.fetchall()
    conn.close()
    return render_template('all_screen_camp.html', images=images)

@app.route('/drh')
def Dr_h():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM images WHERE for='dr_hamed'")
    images = c.fetchall()
    conn.close()
    return render_template('CSE_Main.html', images=images)

@app.route('/maincse')
def CSE_MAIN():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM images WHERE for='main'")
    images = c.fetchall()
    conn.close()
    return render_template('Dr_Hamed_offece.html', images=images)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM images WHERE for='main'")
    main_images = c.fetchall()

    c.execute("SELECT * FROM images WHERE for='dr_hamed'")
    dr_hamed_images = c.fetchall()

    c.execute("SELECT * FROM images WHERE for='all'")
    all_images = c.fetchall()

    conn.close()

    if request.method == 'POST':
        if 'delete_images' in request.form:
            image_ids = request.form.getlist('selected_images')
            conn = sqlite3.connect('database.db')
            c = conn.cursor()

            for image_id in image_ids:
                c.execute("SELECT name FROM images WHERE id=?", (image_id,))
                image = c.fetchone()
                if image:
                    filename = image[0]
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    c.execute("DELETE FROM images WHERE id=?", (image_id,))
                    conn.commit()
                    return redirect('/admin')

            conn.close()

        else:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = file.filename
                random_integer = random.randint(10000000000, 50000000000)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(random_integer) + filename[-5:]))

                section = request.form['section']

                conn = sqlite3.connect('database.db')
                c = conn.cursor()
                c.execute("INSERT INTO images (name, for) VALUES (?, ?)", (str(random_integer) + filename[-5:], section))
                conn.commit()
                conn.close()
                return redirect('/admin')

    return render_template('admin.html', main_images=main_images, dr_hamed_images=dr_hamed_images, all_images=all_images)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080')