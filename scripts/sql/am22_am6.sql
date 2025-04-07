-- Actualiza las grabadoras de 'am22' a 'am8'
UPDATE audio_metadata
SET recorder = 'AM6'
WHERE recorder = 'AM22';

UPDATE audio_activity
SET recorder = 'AM6'
WHERE recorder = 'AM22';
