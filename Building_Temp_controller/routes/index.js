
module.exports = function(app, passport) {
    /* GET home page. */
    app.get('/', function (req, res, next) {
        res.render('index', {title: 'Express'});
    });
    app.get('/register', function (req, res, next) {
        res.render('register');
    });
    app.post('/register', passport.authenticate('local-signup', {
        successRedirect: '/hola', // redirect to the secure profile section
        failureRedirect: '/failure', // redirect back to the signup page if there is an error
        failureFlash: true // allow flash messages
    }));
    app.get('/login', function (req, res, next) {
        res.render('login');
    });

    app.post('/login', passport.authenticate('local-login', {
      successRedirect: '/hola', // redirect to the secure profile section
      failureRedirect: '/failure', // redirect back to the signup page if there is an error
      failureFlash: true // allow flash messages
    }));
};
