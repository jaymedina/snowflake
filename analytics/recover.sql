USE DATABASE RECOVER;
USE SCHEMA PILOT_RAW;

// Records per table
select table_name, row_count
from information_schema.tables
where table_schema = 'PILOT_RAW';

DESC TABLE FITBITDAILYDATA;
CREATE SCHEMA pilot WITH MANAGED ACCESS;
CREATE VIEW IF NOT EXISTS pilot.table_summary AS (
    WITH table_counts AS (
    SELECT
        'ENROLLEDPARTICIPANTS' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.ENROLLEDPARTICIPANTS
    UNION ALL
    SELECT
        'ENROLLEDPARTICIPANTS_CUSTOMFIELDS_SYMPTOMS' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.ENROLLEDPARTICIPANTS_CUSTOMFIELDS_SYMPTOMS
    UNION ALL
    SELECT
        'ENROLLEDPARTICIPANTS_CUSTOMFIELDS_TREATMENTS' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.ENROLLEDPARTICIPANTS_CUSTOMFIELDS_TREATMENTS
    UNION ALL
    SELECT
        'FITBITDAILYDATA' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.FITBITDAILYDATA
    UNION ALL
    SELECT
        'FITBITDEVICES' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.FITBITDEVICES
    UNION ALL
    SELECT
        'FITBITINTRADAYCOMBINED' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.FITBITINTRADAYCOMBINED
    UNION ALL
    SELECT
        'FITBITRESTINGHEARTRATES' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.FITBITRESTINGHEARTRATES
    UNION ALL
    SELECT
        'FITBITSLEEPLOGS' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.FITBITSLEEPLOGS
    UNION ALL
    SELECT
        'GARMINDAILYSUMMARY' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.GARMINDAILYSUMMARY
    UNION ALL
    SELECT
        'GARMINEPOCHSUMMARY' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.GARMINEPOCHSUMMARY
    UNION ALL
    SELECT
        'GARMINHRVSUMMARY' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.GARMINHRVSUMMARY
    UNION ALL
    SELECT
        'GARMINPULSEOXSUMMARY' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.GARMINPULSEOXSUMMARY
    UNION ALL
    SELECT
        'GARMINRESPIRATIONSUMMARY' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.GARMINRESPIRATIONSUMMARY
    UNION ALL
    SELECT
        'GARMINSLEEPSUMMARY' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.GARMINSLEEPSUMMARY
    UNION ALL
    SELECT
        'GARMINSTRESSDETAILSUMMARY' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.GARMINSTRESSDETAILSUMMARY
    UNION ALL
    SELECT
        'GOOGLEFITSAMPLES' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.GOOGLEFITSAMPLES
    UNION ALL
    SELECT
        'HEALTHKITV2ACTIVITYSUMMARIES' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.HEALTHKITV2ACTIVITYSUMMARIES
    UNION ALL
    SELECT
        'HEALTHKITV2ELECTROCARDIOGRAM' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.HEALTHKITV2ELECTROCARDIOGRAM
    UNION ALL
    SELECT
        'HEALTHKITV2HEARTBEAT' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.HEALTHKITV2HEARTBEAT
    UNION ALL
    SELECT
        'HEALTHKITV2SAMPLES' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.HEALTHKITV2SAMPLES
    UNION ALL
    SELECT
        'HEALTHKITV2STATISTICS' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.HEALTHKITV2STATISTICS
    UNION ALL
    SELECT
        'HEALTHKITV2WORKOUTS' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.HEALTHKITV2WORKOUTS
    UNION ALL
    SELECT
        'SYMPTOMLOG' AS TABLE_NAME,
        COUNT(DISTINCT "ParticipantIdentifier") AS COUNT
    FROM RECOVER.PILOT_RAW.SYMPTOMLOG
)
SELECT
    table_counts.TABLE_NAME,
    table_counts.COUNT AS unique_number_of_participants,
    info.row_count AS number_of_records
FROM table_counts
LEFT JOIN information_schema.tables as info
ON table_counts.TABLE_NAME = info.table_name);

select * from pilot.table_summary;