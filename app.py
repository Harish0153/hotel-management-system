from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'secret'

class Hotel:
    def __init__(self, name, total_rooms):
        self.name = name
        self.total_rooms = total_rooms
        self.booked_rooms = 0

    def check_availability(self):
        return self.total_rooms - self.booked_rooms

    def book_room(self, num_rooms):
        if num_rooms <= self.check_availability():
            self.booked_rooms += num_rooms
            return True
        return False

    def cancel_booking(self, num_rooms):
        if num_rooms <= self.booked_rooms:
            self.booked_rooms -= num_rooms
            return True
        return False

    def info(self):
        return {
            "name": self.name,
            "total_rooms": self.total_rooms,
            "booked_rooms": self.booked_rooms,
            "available_rooms": self.check_availability()
        }

users_db = {
    'admin': 'admin123',
    'guest': 'guest123'
}

hotels = {
    'Hotel A': Hotel('Hotel A', 10),
    'Hotel B': Hotel('Hotel B', 20)
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users_db and users_db[uname] == pwd:
            session['username'] = uname
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        selected_hotel = request.form['hotel']
        session['selected_hotel'] = selected_hotel
        return redirect(url_for('hotel_info'))

    return render_template('dashboard.html', hotels=hotels)

@app.route('/hotel_info', methods=['GET', 'POST'])
def hotel_info():
    if 'selected_hotel' not in session:
        return redirect(url_for('dashboard'))

    hotel = hotels[session['selected_hotel']]
    message = ""

    if request.method == 'POST':
        action = request.form['action']
        num_rooms = int(request.form['num_rooms'])
        if action == 'book':
            success = hotel.book_room(num_rooms)
            message = "Room(s) booked!" if success else "Not enough rooms available."
        elif action == 'cancel':
            success = hotel.cancel_booking(num_rooms)
            message = "Booking canceled!" if success else "Cannot cancel more rooms than booked."

    return render_template('hotel_info.html', hotel=hotel.info(), message=message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
    
