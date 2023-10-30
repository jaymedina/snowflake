USE WAREHOUSE COMPUTE_ORG;
USE ROLE SECURITYADMIN;
-- ACCOUNTADMIN privileges
GRANT ROLE ACCOUNTADMIN
TO USER "x.schildwachter@sagebase.org";

-- SYSADMIN privileges
GRANT ROLE SYSADMIN
TO USER "kevin.boske@sagebase.org";
GRANT ROLE SYSADMIN
TO USER "x.schildwachter@sagebase.org";

-- GENIE privileges
GRANT ROLE GENIE_ADMIN
TO ROLE USERADMIN;
GRANT ROLE GENIE_ADMIN
TO USER "alexander.paynter@sagebase.org";
GRANT ROLE GENIE_ADMIN
TO USER "xindi.guo@sagebase.org";
GRANT ROLE GENIE_ADMIN
TO USER "chelsea.nayan@sagebase.org";

-- RECOVER privileges
GRANT ROLE RECOVER_DATA_ENGINEER
TO ROLE USERADMIN;
GRANT ROLE RECOVER_DATA_ANALYTICS
TO ROLE USERADMIN;
GRANT ROLE RECOVER_DATA_ENGINEER
TO USER "phil.snyder@sagebase.org";
GRANT ROLE RECOVER_DATA_ENGINEER
TO USER "rixing.xu@sagebase.org";
GRANT ROLE RECOVER_DATA_ENGINEER
TO USER "thomas.yu@sagebase.org";

-- AD privileges
GRANT ROLE AD
TO ROLE USERADMIN;
GRANT ROLE AD
TO USER "abby.vanderlinden@sagebase.org";

-- Data engineer privileges
GRANT ROLE DATA_ENGINEER
TO ROLE USERADMIN;
GRANT ROLE DATA_ENGINEER
TO USER "phil.snyder@sagebase.org";
GRANT ROLE DATA_ENGINEER
TO USER "rixing.xu@sagebase.org";
GRANT ROLE DATA_ENGINEER
TO USER "thomas.yu@sagebase.org";
GRANT ROLE DATA_ENGINEER
TO USER "brad.macdonald@sagebase.org";
GRANT ROLE DATA_ENGINEER
TO USER "bryan.fauble@sagebase.org";

-- Create governance privileges
GRANT ROLE MASKING_ADMIN
TO USER "thomas.yu@sagebase.org";
USE ROLE ACCOUNTADMIN;
GRANT APPLY MASKING POLICY ON ACCOUNT
TO ROLE MASKING_ADMIN;