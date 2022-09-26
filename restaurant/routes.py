from flask import render_template, request, redirect, url_for, jsonify, flash
from flask import session as login_session
import google.oauth2.credentials
import google_auth_oauthlib.flow
import cachelib
from restaurant import app
from restaurant.sql import cursor
from restaurant.sql.models import Restaurant, Menu

"Global variables for OAuth"
cache = cachelib.SimpleCache()

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    client_secrets_file='client_secret.json',
    scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid'],
    redirect_uri='http://localhost:8080/restaurants/oauth2callback'
)

def login_required(func):
    def is_logged(*args, **kwargs):
        if 'credentials' not in login_session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    is_logged.__name__ = func.__name__
    return is_logged

@app.route('/restaurants/error/<string:error>')
def errorRestaurant(error):
    login = 'credentials' in login_session
    return render_template('error.html', error=error, login=login)

@app.route('/')
@app.route('/restaurants')
def showRestaurant():
    try:
        restaurants = cursor.query(Restaurant).all()
    except:
        restaurants = None
    login = 'credentials' in login_session
    return render_template('home.html', restaurants=restaurants, login=login)
    

@app.route('/restaurant/new', methods=['POST', 'GET'])
@login_required
def newRestaurant():
    if request.method == 'POST':
        try:
            restaurant_name = request.form['restaurant_name']
            if not restaurant_name:
                raise Exception
            
            new_restaurant = Restaurant(name=restaurant_name)
            
            cursor.add(new_restaurant)
            cursor.commit()
            
            flash('New restaurant created', 'success')
            return redirect(url_for('showRestaurant'))
        except:
            return redirect(url_for('errorRestaurant', error='Creating restaurant'))
    return render_template('restaurantForm.html', new=True, login=True)

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['POST', 'GET'])
@login_required
def editRestaurant(restaurant_id):
    if request.method == 'POST':
        try:
            new_restaurant_name = request.form['restaurant_name']
            if not new_restaurant_name:
                raise Exception
            
            restaurant = cursor.query(Restaurant).get(restaurant_id)
            restaurant.name = new_restaurant_name
            
            cursor.add(restaurant)
            cursor.commit()
            
            flash('Restaurant successfully Edited', 'warning')
            return redirect(url_for('showRestaurant'))
        except:
            return redirect(url_for('errorRestaurant', error='Editing restaurant'))
    try:
        restaurant = cursor.query(Restaurant).get(restaurant_id)
        return render_template('restaurantForm.html', edit=True, restaurant=restaurant, login=True)
    except:
        return redirect(url_for('errorRestaurant', error='Retrieving restaurant'))
    

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['POST', 'GET'])
@login_required
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        try:
            restaurant = cursor.query(Restaurant).get(restaurant_id)
            
            menus = cursor.query(Menu).filter_by(restaurant_id=restaurant_id).all()
            for menu in menus:
                cursor.delete(menu)
            
            cursor.delete(restaurant)
            cursor.commit()
            
            flash('Restaurant successfully Deleted', 'danger')
            return redirect(url_for('showRestaurant'))
        except:
            return redirect(url_for('errorRestaurant', error='Deleting restaurant'))
    try:
        restaurant = cursor.query(Restaurant).get(restaurant_id)
        return render_template('restaurantForm.html', delete=True, restaurant=restaurant, login=True)
    except:
        return redirect(url_for('errorRestaurant', error='Retrieving restaurant'))
    

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu', methods=['GET'])
@login_required
def showMenu(restaurant_id):
    try:
        restaurant = cursor.query(Restaurant).get(restaurant_id)
        menus = cursor.query(Menu).filter_by(restaurant_id=restaurant_id).all()    
        return render_template('menus.html', restaurant=restaurant, menus=menus, login=True)
    except:
        return redirect(url_for('errorRestaurant', error='Retrieving menus or restaurant'))

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['POST', 'GET'])
@login_required
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        try:
            restaurant = cursor.query(Restaurant).get(restaurant_id)
            
            menu_name = request.form['menu_name']
            menu_price = float(request.form['menu_price'])
            menu_description = request.form['menu_description']
            
            new_menu = Menu(name=menu_name, price=menu_price, description=menu_description, restaurant_id=restaurant_id, restaurant=restaurant)
            
            cursor.add(new_menu)
            cursor.commit()
            
            flash('Menu Item successfully Created', 'success')
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
        except:
            return redirect(url_for('errorRestaurant'))
    try:
        restaurant = cursor.query(Restaurant).get(restaurant_id)
        return render_template('menusForm.html', new=True, restaurant=restaurant, login=True)
    except:
        return redirect(url_for('errorRestaurant', error='Retrieving restaurant'))

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
@login_required
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        try:
            menu = cursor.query(Menu).get(menu_id)
            
            menu.name = request.form['menu_name']
            menu.price = float(request.form['menu_price'])
            menu.description = request.form['menu_description']
                       
            cursor.commit()
            
            flash('Menu Item successfully Edited', 'warning')
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
        except:
            return redirect(url_for('errorRestaurant'))
    try:
        restaurant = cursor.query(Restaurant).get(restaurant_id)
        menu = cursor.query(Menu).get(menu_id)
        return render_template('menusForm.html', edit=True, restaurant=restaurant, menu=menu, login=True)
    except:
        return redirect(url_for('errorRestaurant', error='Retrieving menu or restaurant'))
        

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if 'credentials' not in login_session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        try:
            restaurant = cursor.query(Restaurant).get(restaurant_id)
            menu = cursor.query(Menu).get(menu_id)
            
            cursor.delete(menu)
            cursor.commit()
            
            flash('Menu Item successfully Deleted', 'danger')
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
        except:
            return redirect(url_for('errorRestaurant', error='Deleting Menu Item'))
    try:
        restaurant = cursor.query(Restaurant).get(restaurant_id)
        menu = cursor.query(Menu).get(menu_id)
        return render_template('menusForm.html', delete=True, restaurant=restaurant, menu=menu, login=True)
    except:
        return redirect(url_for('errorRestaurant', error='Retrieving menu or restaurant'))
    
@app.route('/restaurants/JSON')
def restaurants_JSON():
    restaurants = cursor.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])
    
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menus_JSON(restaurant_id):
    try:
        restaurant = cursor.query(Restaurant).get(restaurant_id)
        menus = cursor.query(Menu).filter_by(restaurant_id=restaurant_id).all()
        return jsonify(Restaurant={
            'Restaurant': restaurant.serialize,
            'menus': [i.serialize for i in menus]    
        })
    except:
        return jsonify(Error={'Message':'Restaurant not found'})

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurant_menu_JSON(restaurant_id, menu_id):
    try:
        restaurant = cursor.query(Restaurant).get(restaurant_id)
        menu = cursor.query(Menu).filter_by(menu_id=menu_id).one()
        return jsonify(Menu=menu.serialize)
    except:
        return jsonify(Error={'Message':'Restaurant or Menu not found'})

@app.route('/restaurants/login')
def login():  
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    login_session['state'] = state
    cache.add('state', state)
    return redirect(auth_url)

@app.route('/restaurants/oauth2callback')
def oauth2callback():
    login_session['state'] = cache.get('state')
    flow.fetch_token(authorization_response=request.url)
    if not login_session['state'] == request.args['state']:
        flash('Unsucessfully Authentication', 'danger')
        return redirect(url_for('showRestaurant'))
    
    credentials = flow.credentials
    login_session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
    }
    flash('Sucessfully Authentication', 'success')
    return redirect(url_for('showRestaurant'))

@app.route('/restaurants/logout')
def logout():
    if 'credentials' in login_session:
        del(login_session['credentials'])
        cache.delete('state')
        flash('Logout succesfully', 'warning')
    return redirect(url_for('showRestaurant'))