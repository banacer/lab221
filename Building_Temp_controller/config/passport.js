// config/passport.js

// load all the things we need
var passport = require('passport');
var LocalStrategy   = require('passport-local').Strategy;
// load up the user model
//var User            = require('../models/user');
var models  = require('../models');
// expose this function to our app using module.exports
module.exports = function(passport) {

    // =========================================================================
    // passport session setup ==================================================
    // =========================================================================
    // required for persistent login sessions
    // passport needs ability to serialize and unserialize users out of session

    // used to serialize the user for the session
    passport.serializeUser(function(user, done) {
        done(null, user.id);
    });

    // used to deserialize the user
    passport.deserializeUser(function(id, done) {
        models.users.findById(id).then(function(err, user) {
            console.log("you are here id : "+ user);
            done(err, user);
        }).error(function(err){
            done(new Error('User ' + id + ' does not exist'));
        });
    });

    // =========================================================================
    // LOCAL SIGNUP ============================================================
    // =========================================================================
    // we are using named strategies since we have one for login and one for signup
    // by default, if there was no name, it would just be called 'local'

    passport.use('local-signup', new LocalStrategy({
            // by default, local strategy uses username and password, we will override with email
            usernameField : 'email',
            passwordField : 'pass',
            passReqToCallback : true // allows us to pass back the entire request to the callback
        },
        function(req, email, pass, done) {

            // asynchronous
            // User.findOne wont fire unless data is sent back
            models.users.find({where: {email: email}}).then( function (err,user) {
                // already exists
                if (user) {
                    console.log('User already exists');
                    return done(null, false,
                        req.flash('message', 'User Already Exists'));
                } else {
                    // if there is no user with that email
                    // create the user
                    models.users.create( {
                        email: email,
                        password: this.methods.generateHash(pass),
                        tag_id: req.body.tag_id,
                        firstName: req.body.fname,
                        lastName: req.body.lname,
                        age: req.body.age,
                        gender: req.body.gender
                    }).then(function(user) {
                        console.log("you are here id : "+ user.id);
                        return done(null, user);
                    });
                }
            }).error(function(err){
                console.log('Error in SignUp: ' + err);
                return done(err);
            });
        }));

    // =========================================================================
    // LOCAL LOGIN =============================================================
    // =========================================================================
    // we are using named strategies since we have one for login and one for signup
    // by default, if there was no name, it would just be called 'local'

    passport.use('local-login', new LocalStrategy({
            // by default, local strategy uses username and password, we will override with email
            usernameField : 'email',
            passwordField : 'pass',
            passReqToCallback : true // allows us to pass back the entire request to the callback
        },
        function(req, email, pass, done) { // callback with email and password from our form

            // find a user whose email is the same as the forms email
            // we are checking to see if the user trying to login already exists
            models.users.find({where: {email: email}}).then( function(err,user) {
                // if no user is found, return the message
                if (!user)
                    return done(null, false, req.flash('loginMessage', 'No user found.')); // req.flash is the way to set flashdata using connect-flash

                // if the user is found but the password is wrong
                if (!user.methods.validPassword(pass))
                    return done(null, false, req.flash('loginMessage', 'Oops! Wrong password.')); // create the loginMessage and save it to session as flashdata
                // all is well, return successful user
                return done(null, user);
            }).error(function(err){
                return done(err);
            });

        }));

};