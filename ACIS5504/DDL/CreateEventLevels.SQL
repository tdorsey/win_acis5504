BEGIN TRANSACTION
INSERT INTO event_manager_event_level(level,description,points_multiplier,required_judge_level) VALUES(1,'Friday Night Magic',1,1);
INSERT INTO event_manager_event_level(level,description,points_multiplier,required_judge_level) VALUES(2,'Game Day,',1,1);
INSERT INTO event_manager_event_level(level,description,points_multiplier,required_judge_level) VALUES(3,'Grand Prix Trial',3,2);
INSERT INTO event_manager_event_level(level,description,points_multiplier,required_judge_level) VALUES(4, 'Grand Prix',5,4);
INSERT INTO event_manager_event_level(level,description,points_multiplier,required_judge_level) VALUES(5,'Pro Tour Qualifier',5,3);
INSERT INTO event_manager_event_level(level,description,points_multiplier,required_judge_level) VALUES(6,'Pro Tour',9,5);
COMMIT