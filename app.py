from flask import Flask, render_template, request

app = Flask(__name__)

@app.after_request
def add_no_cache_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        return render_template('thankyou.html', full_name=full_name, phone=phone, email=email)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
