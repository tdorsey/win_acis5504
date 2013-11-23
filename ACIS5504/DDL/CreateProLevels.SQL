
BEGIN TRANSACTION
DELETE event_manager_pro_level
INSERT INTO event_manager_pro_level(description) VALUES('Bronze');
INSERT INTO event_manager_pro_level(description) VALUES('Silver');
INSERT INTO event_manager_pro_level(description) VALUES('Gold');
INSERT INTO event_manager_pro_level(description) VALUES('Platinum');
COMMIT;
