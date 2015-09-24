var express = require('express');
var router = express.Router();
var models  = require('../models');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express'});
});
router.get('/register',function(req,res,next) {
  res.render('register');
});
router.post('/register',function(req,res,next) {
  models.users.create({
    tag_id: req.body.tag_id,
    firstName: req.body.fname,
    lastName: req.body.lname,
    age: req.body.age,
    email: req.body.email,
    gender: req.body.gender,
    password: req.body.pass
  }).then(function(){
    res.redirect('/');
  });
});
router.get('/login',function(req,res,next) {
  res.render('login');
});

router.post('/login',function(req,res,next) {
  console.log('you are here');
});

module.exports = router;
