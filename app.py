from flask import Flask, render_template

app = Flask(__name__)

# In-memory database with Live Unsplash URLs for immediate rendering
NEW_ARRIVALS = [
    {
        "id": 1,
        "name": "Sri Amman Jewellery 1 - Indian Temple Jewellery",
        "price": "115,000",
        "image": "https://plus.unsplash.com/premium_photo-1681276170092-446cd1b5b32d?q=80&w=688&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    },
    {
        "id": 2,
        "name": "Sri Amman Jewellery 2 - Contemporary Gold",
        "price": "85,000",
        "image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=400&auto=format&fit=crop"
    },
    {
        "id": 3,
        "name": "Sri Amman Jewellery 3 - Diamond Set",
        "price": "250,000",
        "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?q=80&w=400&auto=format&fit=crop"
    },
    {
        "id": 4,
        "name": "Sri Amman Jewellery 4 - Bridal Choker",
        "price": "195,000",
        "image": "https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?q=80&w=400&auto=format&fit=crop"
    }
]

@app.route('/')
def home():
    return render_template('index.html', products=NEW_ARRIVALS)

if __name__ == '__main__':
    # host='0.0.0.0' = accessible on local network (Redmi as server)
    # debug=False for Redmi (saves CPU/RAM); use True for local dev
    # threaded=False reduces memory on low-resource devices
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)