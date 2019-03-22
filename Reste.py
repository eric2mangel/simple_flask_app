@app.context_processor
def toto():
    def pluralize(count, singular,plural=None):
        if not isinstance(count,int):
            raise ValueError('"{}" must be an integer'.format(count))
        if plural is None:
            plural=singular + 's'
        if count==1:
            string=singular
        else:
            string=plural
        return "{} {}".format(count,string)
    return dict(pluralize=pluralize)

@app.context_processor
def inject_now():
    return {'now' : datetime.now()}

posts=[{"id":1,"title": "First Post","content": "This is my first post"},
    {"id":2,"title": "Second Post","content": "This is my second post"},
    {"id":3,"title": "Third Post","content": "This is my third post"}]

#La commande suivante est équivalente à :
#Si on demande la pacge d'accueuil, exécuter la fonction suivante
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/blog/')
def posts_index():
    post=Post.all()
    return render_template('blog/index.html',posts=posts)

@app.route('/blog/posts/<int:id>')
def posts_show(id):
    #post=posts[id-1]
    post=Post.find(id)
    return render_template('blog/show.html',post=post)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('/errors/404.html'), 404



    #Degug=True signifie qu'à chaque modification, il va relancer le serveur
    #Evite de de voir relancer le serveur à chaque fois
    #On dit également que maintenant c'est le port 3000.
    #Si on rajoutait host='0.0.0.0', on pourrait accéder à ça depuis n'importe
    #quel appareil du réseau
