def query_annual_unique_users():
    """Return the number of unique users for a given year."""

    return f"""
    WITH
    htan_project_ids AS (

        SELECT
            DISTINCT cast(scopes.value as integer) as project_id
        FROM
            synapse_data_warehouse.synapse.node_latest,
            LATERAL flatten(input => node_latest.scope_ids) scopes
        WHERE
            id = '20446927'

    )
    SELECT
        count(DISTINCT user_id) as annual_unique_users
    FROM
        synapse_data_warehouse.synapse.filedownload
    WHERE
        project_id in (SELECT project_id FROM htan_project_ids)
    AND
        RECORD_DATE >= DATEADD(month, -12, CURRENT_DATE);
    """


def query_annual_downloads():
    """Return the annual downloads (in TiB) for a given year."""

    return f"""
    WITH
    htan_project_ids AS (

        SELECT
            DISTINCT cast(scopes.value as integer) as project_id
        FROM
            synapse_data_warehouse.synapse.node_latest,
            LATERAL flatten(input => node_latest.scope_ids) scopes
        WHERE
            id = '20446927'

    ),
    file_handle_ids AS (

        SELECT
            DISTINCT file_handle_id
        FROM
            synapse_data_warehouse.synapse.filedownload
        WHERE
            project_id in (SELECT project_id FROM htan_project_ids)
        AND
            record_date >= DATEADD(month, -12, CURRENT_DATE)
    )
    SELECT
        SUM(content_size) / POWER(1024, 4) as annual_downloads_in_tib
    FROM
        synapse_data_warehouse.synapse.file_latest
    WHERE
        id in (SELECT file_handle_id FROM file_handle_ids);
    """


def query_annual_cost():
    """Return the annual cost for a given year."""

    return f"""
    WITH htan_projects AS (
    SELECT
        cast(scopes.value as integer) as project_id
    FROM
        synapse_data_warehouse.synapse.node_latest,
        LATERAL flatten(input => node_latest.scope_ids) scopes
    WHERE
        id = 20446927
    ), price_per_year AS (
        SELECT
            CASE
                WHEN FILE_LATEST.CONCRETE_TYPE = 'org.sagebionetworks.repo.model.file.GoogleCloudFileHandle'
                THEN FILE_LATEST.CONTENT_SIZE / power(2, 30) * 0.026 * 12
                ELSE FILE_LATEST.CONTENT_SIZE / power(2, 30) * 0.023 * 12
            END AS price_per_file_annually
        FROM
            htan_projects
        LEFT JOIN
            synapse_data_warehouse.synapse.node_latest
        ON
            htan_projects.project_id = node_latest.project_id
        LEFT JOIN
            synapse_data_warehouse.synapse.file_latest FILE_LATEST
        ON
            node_latest.FILE_HANDLE_ID = FILE_LATEST.ID
        WHERE
            node_latest.node_type != 'folder'
    )
    SELECT
        SUM(price_per_file_annually) AS annual_cost
    FROM
        price_per_year;
    """


def query_monthly_download_trends():
    """Return the monthly download trends for a given year."""

    return f"""
    WITH htan_projects AS (
        SELECT
            CAST(scopes.value AS INTEGER) AS project_id
        FROM
            synapse_data_warehouse.synapse.node_latest,
            LATERAL FLATTEN(input => node_latest.scope_ids) scopes
        WHERE
            id = 20446927
    ),
    project_files AS (
        SELECT
            nl.id AS node_id,
            hp.project_id
        FROM
            synapse_data_warehouse.synapse.node_latest nl
        JOIN
            htan_projects hp
        ON
            nl.project_id = hp.project_id
    ),
    file_access AS (
        SELECT
            pf.project_id,
            filedownload.user_id,
            DATE_TRUNC('month', filedownload.TIMESTAMP) AS access_month
        FROM
            project_files pf
        JOIN
            synapse_data_warehouse.synapse.filedownload filedownload
        ON
            pf.node_id = filedownload.file_handle_id
        WHERE
            filedownload.TIMESTAMP >= DATEADD(month, -12, CURRENT_DATE)
    )
    SELECT
        project_id,
        access_month,
        COUNT(DISTINCT user_id) AS distinct_user_count
    FROM
        file_access
    GROUP BY
        project_id,
        access_month
    ORDER BY
        project_id,
        access_month;
    """


def query_current_project_sizes():
    """Return the annual project sizes for a given year."""

    return f"""
    WITH
    htan_project_ids AS (

        SELECT
            DISTINCT cast(scopes.value as integer) as project_id
        FROM
            synapse_data_warehouse.synapse.node_latest,
            LATERAL flatten(input => node_latest.scope_ids) scopes
        WHERE
            id = '20446927'

    )
    SELECT
        count(DISTINCT user_id) as annual_unique_users
    FROM
        synapse_data_warehouse.synapse.filedownload
    WHERE
        project_id in (SELECT project_id FROM htan_project_ids)
    AND
        RECORD_DATE >= DATEADD(month, -12, CURRENT_DATE);
    """


def query_annual_project_downloads():
    """Return the annual project downloads for a given year."""

    return f"""
    WITH
    htan_project_ids AS (
        SELECT
            DISTINCT cast(scopes.value as integer) as project_id
        FROM
            synapse_data_warehouse.synapse.node_latest,
            LATERAL flatten(input => node_latest.scope_ids) scopes
        WHERE
            id = '20446927'
    ),
    file_handle_ids AS (
        SELECT
            project_id,
            file_handle_id
        FROM
            synapse_data_warehouse.synapse.filedownload
        WHERE
            project_id in (SELECT project_id FROM htan_project_ids)
        AND
            record_date >= DATEADD(month, -12, CURRENT_DATE)
    ),
    total_download_size AS (
        SELECT
            fh.project_id,
            SUM(fl.content_size) / POWER(1024, 4) as annual_downloads_in_tib
        FROM
            file_handle_ids fh
        JOIN
            synapse_data_warehouse.synapse.file_latest fl
        ON
            fh.file_handle_id = fl.id
        GROUP BY
            fh.project_id
    ),
    total_project_size AS (
        SELECT
            nl.project_id,
            SUM(fl.content_size) / POWER(1024, 4) as total_project_size_in_tib
        FROM
            synapse_data_warehouse.synapse.node_latest nl
        JOIN
            synapse_data_warehouse.synapse.file_latest fl
        ON
            nl.file_handle_id = fl.id
        WHERE
            nl.project_id in (SELECT project_id FROM htan_project_ids)
        GROUP BY
            nl.project_id
    )
    SELECT
        tds.project_id,
        tds.annual_downloads_in_tib,
        tps.total_project_size_in_tib
    FROM
        total_download_size tds
    JOIN
        total_project_size tps
    ON
        tds.project_id = tps.project_id
    ORDER BY
        tds.annual_downloads_in_tib DESC;
    """


def query_top_annotations():
    """Return the top annotations for HTAN."""

    return f"""
    WITH htan_projects AS (
    SELECT
        cast(scopes.value as integer) as project_id
    FROM
        synapse_data_warehouse.synapse.node_latest,
        LATERAL flatten(input => node_latest.scope_ids) scopes
    WHERE
        id = 20446927
    ), dedup_downloads AS (
        SELECT
            DISTINCT filedownload.user_id, 
            filedownload.file_handle_id, 
            filedownload.RECORD_DATE, 
            node_latest.annotations:annotations:Component:value[0] AS component
        FROM
            htan_projects
        INNER JOIN
            synapse_data_warehouse.synapse.filedownload
            ON htan_projects.project_id = filedownload.project_id
        INNER JOIN
            synapse_data_warehouse.synapse.node_latest
            ON filedownload.file_handle_id = node_latest.file_handle_id
        WHERE
            node_latest.annotations:annotations:Component:value[0] IS NOT NULL
        AND
            filedownload.RECORD_DATE >= DATEADD(month, -12, CURRENT_DATE)
    ), component_popularity AS (
        SELECT
            node_latest.annotations:annotations:Component:value[0] as component,
            COUNT(DISTINCT node_latest.id) AS occurrences
        FROM
            synapse_data_warehouse.synapse.node_latest node_latest
        JOIN
            htan_projects
        ON
            node_latest.project_id = htan_projects.project_id
        WHERE
            node_latest.annotations:annotations:Component:value[0] IS NOT NULL
        GROUP BY
            component
    )
    SELECT
        dd.component AS component_name,
        cp.occurrences,
        COUNT(DISTINCT dd.user_id) AS number_of_unique_downloads
    FROM
        dedup_downloads dd
    JOIN
        component_popularity cp
    ON
        dd.component = cp.component
    GROUP BY
        dd.component, cp.occurrences
    ORDER BY
        number_of_unique_downloads DESC;
    """


def query_entity_distribution(synapse_id=20446927):
    """Returns the number of files for a given project (synapse_id)."""

    return f"""
    with htan_projects as (
        // select distinct cast(replace(NF.projectid, 'syn', '') as INTEGER) as project_id from sage.portal_raw.HTAN
        select
            cast(scopes.value as integer) as project_id
        from
            synapse_data_warehouse.synapse.node_latest,
            lateral flatten(input => node_latest.scope_ids) scopes
        where
            id = {synapse_id}
    )
    SELECT
        node_type,
        count(*) as number_of_files,
        count(*) * 100.0 / SUM(COUNT(*)) OVER () AS percentage_of_total
    FROM
        SYNAPSE_DATA_WAREHOUSE.SYNAPSE.NODE_LATEST
    JOIN
        htan_projects
        on NODE_LATEST.project_id = htan_projects.project_id
    group by
        node_type
    order by
        number_of_files DESC;
    """

def query_project_sizes():
    """Return the cumulative size of all projects."""

    return f"""
    WITH
    htan_project_ids AS (

        SELECT
            DISTINCT cast(scopes.value as integer) as project_id
        FROM
            synapse_data_warehouse.synapse.node_latest,
            LATERAL flatten(input => node_latest.scope_ids) scopes
        WHERE
            id = '20446927'

    ),
    htan_project_files AS (

        SELECT
            node_latest.id AS node_id,
            htan_project_ids.project_id
        FROM
            synapse_data_warehouse.synapse.node_latest
        JOIN
            htan_project_ids
        ON
            node_latest.project_id = htan_project_ids.project_id
        WHERE
            node_type = 'file'

    ),
    htan_file_sizes AS (

        SELECT
            content_size,
            htan_project_files.node_id,
            htan_project_files.project_id
        FROM
            synapse_data_warehouse.synapse.file_latest file_latest
        JOIN
            htan_project_files
        ON
            file_latest.id = htan_project_files.node_id

    )
    SELECT
        project_id,
        SUM(content_size) / POWER(1024, 3) AS project_size_in_gib
    FROM
        htan_file_sizes
    GROUP BY
        project_id;
    """

def query_project_downloads():
    """Return the total number of downloads for all projects."""

    return """
    WITH htan_projects AS (
        SELECT
            CAST(scopes.value AS INTEGER) AS project_id
        FROM
            synapse_data_warehouse.synapse.node_latest,
            LATERAL FLATTEN(input => node_latest.scope_ids) scopes
        WHERE
            id = 20446927
    ),
    project_files AS (
        SELECT
            nl.id AS node_id,
            hp.project_id
        FROM
            synapse_data_warehouse.synapse.node_latest nl
        JOIN
            htan_projects hp
        ON
            nl.project_id = hp.project_id
    ),
    file_content_size AS (
        SELECT
            pf.project_id,
            filedownload.file_handle_id,
            filelatest.content_size
        FROM
            project_files pf
        JOIN
            synapse_data_warehouse.synapse.filedownload filedownload
        ON
            pf.node_id = filedownload.file_handle_id
        JOIN
            synapse_data_warehouse.synapse.file_latest filelatest
        ON
            filelatest.id = filedownload.file_handle_id
    )
    SELECT
        project_id,
        SUM(content_size) AS total_downloads
    FROM
        file_content_size
    GROUP BY
        project_id;
    """

def query_unique_users(months_back):
    """Return the number of monthly unique users going back x months (months_back)."""

    return f"""
    WITH htan_projects AS (
        SELECT
            CAST(scopes.value AS INTEGER) AS project_id
        FROM
            synapse_data_warehouse.synapse.node_latest,
            LATERAL FLATTEN(input => node_latest.scope_ids) scopes
        WHERE
            id = 20446927
    ),
    project_files AS (
        SELECT
            nl.id AS node_id,
            hp.project_id
        FROM
            synapse_data_warehouse.synapse.node_latest nl
        JOIN
            htan_projects hp
        ON
            nl.project_id = hp.project_id
    ),
    file_access AS (
        SELECT
            pf.project_id,
            filedownload.user_id,
            DATE_TRUNC('month', filedownload.TIMESTAMP) AS access_month
        FROM
            project_files pf
        JOIN
            synapse_data_warehouse.synapse.filedownload filedownload
        ON
            pf.node_id = filedownload.file_handle_id
        WHERE
            filedownload.TIMESTAMP >= DATEADD(month, -{months_back}, CURRENT_DATE)
    )
    SELECT
        project_id,
        access_month,
        COUNT(DISTINCT user_id) AS distinct_user_count
    FROM
        file_access
    GROUP BY
        project_id,
        access_month
    ORDER BY
        project_id,
        access_month;
    """
