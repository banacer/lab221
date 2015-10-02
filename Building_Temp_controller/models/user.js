"use strict";
var bcrypt   = require('bcrypt-nodejs');

module.exports = function(sequelize, DataTypes) {
    var User = sequelize.define('User', {
        id: {
            type: DataTypes.INTEGER,
            autoIncrement: true,
            primaryKey: true
        },
        tag_id: DataTypes.INTEGER,
        firstName: DataTypes.STRING,
        lastName: DataTypes.STRING,
        age: DataTypes.INTEGER,
        email: DataTypes.STRING,
        gender: DataTypes.STRING,
        password: DataTypes.STRING
    },
    {
        paranoid: true,
        instanceMethods: {
            setPassword: function(password) {
                this.password = bcrypt.hashSync(password, bcrypt.genSaltSync(8), null);
            },
            validPassword: function(password) {
                return bcrypt.compareSync(password, this.password);
            }
        }
    });
    return User;
};
