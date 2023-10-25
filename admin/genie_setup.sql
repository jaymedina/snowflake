USE ROLE sysadmin;
CREATE DATABASE IF NOT EXISTS genie;

-- ! Grant roles
USE ROLE securityadmin;
GRANT USAGE ON DATABASE genie
TO ROLE genie_admin;
GRANT USAGE ON FUTURE SCHEMAS IN DATABASE genie
TO ROLE genie_admin;
GRANT SELECT ON FUTURE TABLES IN DATABASE genie
TO ROLE genie_admin;

GRANT USAGE ON WAREHOUSE tableau
TO ROLE genie_admin;