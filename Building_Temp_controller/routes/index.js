var express = require('express');
var router = express.Router();
var models  = require('../models');
var passport = require('passport');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express'});
});
router.get('/register',function(req,res,next) {
  res.render('register');
});
router.post('/register',passport.authenticate('local-signup', {
    successRedirect : '/hola', // redirect to the secure profile section
    failureRedirect : '/register', // redirect back to the signup page if there is an error
    failureFlash : true // allow flash messages
  }));
router.get('/login',function(req,res,next) {
  res.render('login');
});

router.post('/login',function(req,res,next) {
  console.log('you are here');
});

module.exports = router;
