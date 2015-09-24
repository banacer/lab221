"use strict";

module.exports = function(sequelize, DataTypes) {
    var User = sequelize.define("users", {
        user_id: {
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

    });

    return User;
};
