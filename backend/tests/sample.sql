INSERT INTO app_db.appuser (short_name, first_name, last_name, email, role_id, team_id, start_date, created_at, updated_at, is_active)
VALUES
    ('bmoore', 'Brian', 'Moore', 'BrianFMoore@dayrep.com', 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('thyatt', 'Tammy', 'Hyatt', 'TammyDHyatt@rhyta.com', 1, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('ghills', 'George', 'Hills', 'GeorgeSHills@dayrep.com', 2, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('aryan', 'Annette', 'Ryan', 'AnnetteJRyan@teleworm.us', 1, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('jwhobrey', 'James', 'Whobrey', 'JamesJWhobrey@armyspy.com', 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('mwoodmansee', 'Mathew', 'Woodmansee', 'MathewKWoodmansee@rhyta.com', 3, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('mtaylor', 'Michael', 'Taylor', 'MichaelJTaylor@teleworm.us', 1, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE);
  
INSERT INTO app_db.client (name, is_active, created_at, updated_at)
VALUES
    ('dyvenia', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('google', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('neuralink', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_db.team (lead_user_id, name, short_name, is_active, created_at, updated_at)
VALUES
    (1, 'Seniors', 'Snrs', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, 'Mid-levels', 'Mids', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (3, 'Juniors', 'Jnrs', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_db.sponsor (client_id, name, short_name, is_active, created_at, updated_at)
VALUES
    (1, 'Alessio Civitillo', 'Alessio', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, 'Sundar Pichai', 'Sundar', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (3, 'Elon Musk', 'Elon', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_db.epic (short_name, name, team_id, sponsor_id, start_date, is_active, created_at, updated_at)
VALUES
    ('App', 'Mobile app', 1, 2, CURRENT_TIMESTAMP, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Pay', 'Payment gateway', 2, 1, CURRENT_TIMESTAMP, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_db.epicarea (epic_id, name, is_active, created_at, updated_at)
VALUES
    (1, 'Login page', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (1, 'Design', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (1, 'Night mode', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, 'Crypto', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_db.role (short_name, name, created_at, updated_at, is_active)
VALUES
    ('Data Eng', 'Data Engineer', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('Analyst', 'Data Analyst', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('Scientist', 'Data Scientist', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE);

INSERT INTO app_db.rate (user_id, client_id, valid_from, valid_to, amount, created_at, updated_at, is_active)
VALUES
    (1, 1, '2022-01-01', '2022-02-01', 300, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (1, 2, '2022-02-01', '2022-03-01', 600, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (1, 3, '2022-03-01', '2022-04-01', 400, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (2, 1, '2022-02-01', '2022-03-01', 250, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (2, 2, '2022-01-01', '2022-02-01', 550, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (2, 3, '2022-02-01', '2022-03-01', 350, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (3, 1, '2022-03-01', '2022-04-01', 200, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (3, 2, '2022-03-01', '2022-04-01', 500, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (3, 3, '2022-01-01', '2022-02-01', 300, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE);

INSERT INTO app_db.timelog (user_id, start_time, end_time, epic_id, count_hours, count_days, month, year)
VALUES
    (1, '2022-04-03 08:30:00.000000', '2022-04-03 13:45:00.000000', 1, 5.25, 0.66, 1, 2022),
    (1, '2022-05-03 09:30:00.000000', '2022-05-03 12:15:00.000000', 1, 3.25, 0.41, 4, 2022);
    
INSERT INTO app_db.forecast (user_id, epic_id, days, month, year)
VALUES
    (1, 1, 5.0, 4, 2022),
    (2, 1, 5.0, 4, 2022),
    (3, 1, 5.0, 4, 2022);
    
INSERT INTO app_db.capacity (user_id, team_id, year, month, days, created_at, updated_at, is_locked)
VALUES
    (1, 1, 2022, 1, 18, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (2, 2, 2022, 2, 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (3, 2, 2022, 2, 12, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (5, 1, 2022, 1, 13, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

INSERT INTO app_db.demand (team_id, epic_id, year, month, days, created_at, updated_at, is_locked)
VALUES
    (1, 1, 2022, 1, 18, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (2, 2, 2022, 2, 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (3, 2, 2022, 2, 12, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (2, 1, 2022, 1, 13, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);