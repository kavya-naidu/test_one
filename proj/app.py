from flask import Flask,render_template

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    dic = {"name":"kavya","mobile":9876543210}
    return render_template('index.html', context=dic)


@flask_app.route('/about-us')
def about_us():
    dic = {"name":"lohi","mobile":9876543210}
    return render_template('index.html', context=dic)




@flask_app.route('/contact-us')
def contact_us():
    dic = {"name":"rakshitha","mobile":9876543210}
    return render_template('index.html', context=dic)


if __name__ == '__main__':
    flask_app.run(
        host='127.0.0.1',
        port=5010,
        debug=True
    )