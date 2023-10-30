USE WAREHOUSE COMPUTE_ORG;
USE ROLE USERADMIN;

-- TODO: Create role for tableau warehouse
-- system wide roles
CREATE ROLE IF NOT EXISTS MASKING_ADMIN;
CREATE ROLE IF NOT EXISTS DATA_ENGINEER;

-- GENIE roles
CREATE ROLE IF NOT EXISTS GENIE_ADMIN;

-- RECOVER roles
CREATE ROLE IF NOT EXISTS RECOVER_DATA_ENGINEER;
CREATE ROLE IF NOT EXISTS RECOVER_DATA_ANALYTICS;

-- AD
CREATE ROLE IF NOT EXISTS AD;
