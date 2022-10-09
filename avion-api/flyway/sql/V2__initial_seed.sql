/* Initial admin account. Password: 'admin' */
INSERT INTO user_account (firstname, lastname, email, username, password, salt)
    VALUES ("Admin", "Admin", "admin@example.com", "admin", "0b053e226ecc2f1ed31fda50209b26adb7289d02e4159fb8270f88d4204ecc84", "c0m1CaX2FmT2eFDsBoMs");


/* AIRCRAFT MODELS */
INSERT INTO aircraft_model (manufacturer, model, icao_code, engine_count, engine_type, max_fuel, empty_weight, max_takeoff_weight, max_passengers, price)
    VALUES ("Cessna", "172 Skyhawk (G1000)", "C172", 1, "piston", 212, 743, 1111, 3, 50000);
