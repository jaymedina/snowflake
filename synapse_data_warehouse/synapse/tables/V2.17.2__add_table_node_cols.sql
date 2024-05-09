USE SCHEMA {{database_name}}.synapse; --noqa: JJ01,PRS,TMP
ALTER TABLE NODE_LATEST ADD COLUMN version_comment STRING COMMENT 'A short description assigned to this node version.';
ALTER TABLE NODE_LATEST ADD COLUMN version_label STRING COMMENT 'A short label assigned to this this node version.';
ALTER TABLE NODE_LATEST ADD COLUMN alias STRING COMMENT 'An alias assigned to a project entity if present.';
ALTER TABLE NODE_LATEST ADD COLUMN activity_id INT COMMENT 'The reference to the id of an activity assigned to the node.';
ALTER TABLE NODE_LATEST ADD COLUMN column_model_ids VARIANT COMMENT 'For entities that define a table schema (e.g. table, views etc), the list of column ids assigned to the schema.';
ALTER TABLE NODE_LATEST ADD COLUMN scope_ids VARIANT COMMENT 'For entities that define a scope (e.g. entity views, submission views etc), the list of entity ids included in the scope.';
ALTER TABLE NODE_LATEST ADD COLUMN items VARIANT COMMENT 'For entities that define a fixed list of entity references (e.g. dataset, dataset collections), the list of entity references included in the scope.';
ALTER TABLE NODE_LATEST ADD COLUMN reference VARIANT COMMENT 'For Link entities, the reference to the linked target.';
ALTER TABLE NODE_LATEST ADD COLUMN is_search_enabled BOOLEAN COMMENT 'For Table like entities (e.g. EntityView, MaterializedView etc), defines if full text search is enabled on those entities.';
ALTER TABLE NODE_LATEST ADD COLUMN defining_sql STRING COMMENT 'For tables that are driven by a synapse SQL query (e.g. MaterializedView, VirtualTable), defines the underlying SQL query.';
ALTER TABLE NODE_LATEST ADD COLUMN internal_annotations VARIANT COMMENT 'The json representation of the entity internal annotations that are used to store additional data about different types of entity (e.g. dataset checksum, size)';

COMMENT ON COLUMN NODE_LATEST.change_type IS 'The type of change that occurred on the node, e.g., CREATE, UPDATE, DELETE.';
COMMENT ON COLUMN NODE_LATEST.change_timestamp IS 'The time when the change (created/updated/deleted) on the node is pushed to the queue for snapshotting.';
COMMENT ON COLUMN NODE_LATEST.change_user_id IS 'The unique identifier of the user who made the change to the node.';
COMMENT ON COLUMN NODE_LATEST.snapshot_timestamp IS 'The time when the snapshot was taken. (It is usually after the change happened).';
COMMENT ON COLUMN NODE_LATEST.id IS 'The unique identifier of the node.';
COMMENT ON COLUMN NODE_LATEST.benefactor_id IS 'The identifier of the (ancestor) node which provides the permissions that apply to this node. Can be the id of the node itself.';
COMMENT ON COLUMN NODE_LATEST.project_id IS 'The project where the node resides. It will be empty for the change type DELETE.';
COMMENT ON COLUMN NODE_LATEST.parent_id IS 'The unique identifier of the parent in the node hierarchy.';
COMMENT ON COLUMN NODE_LATEST.node_type IS 'The type of the node. Allowed node types are : project, folder, file, table, link, entityview, dockerrepo, submissionview, dataset, datasetcollection, materializedview, virtualtable.';
COMMENT ON COLUMN NODE_LATEST.created_on IS 'The creation time of the node.';
COMMENT ON COLUMN NODE_LATEST.created_by IS 'The unique identifier of the user who created the node.';
COMMENT ON COLUMN NODE_LATEST.modified_on IS 'The most recent change time of the node.';
COMMENT ON COLUMN NODE_LATEST.modified_by IS 'The unique identifier of the user who last modified the node.';
COMMENT ON COLUMN NODE_LATEST.version_number IS 'The version of the node on which the change occurred, if applicable.';
COMMENT ON COLUMN NODE_LATEST.file_handle_id IS 'The unique identifier of the file handle if the node is a file, null otherwise.';
COMMENT ON COLUMN NODE_LATEST.name IS 'The name of the node.';
COMMENT ON COLUMN NODE_LATEST.is_public IS 'If true, READ permission is granted to all the Synapse users, including the anonymous user, at the time of the snapshot.';
COMMENT ON COLUMN NODE_LATEST.is_controlled IS 'If true, an access requirement managed by the ACT is set on the node.';
COMMENT ON COLUMN NODE_LATEST.is_restricted IS 'If true, a terms-of-use access requirement is set on the node.';
COMMENT ON COLUMN NODE_LATEST.effective_ars IS 'The list of access requirement ids that apply to the entity at the time the snapshot was taken.';
COMMENT ON COLUMN NODE_LATEST.annotations IS 'The json representation of the entity annotations assigned by the user.';
COMMENT ON COLUMN NODE_LATEST.derived_annotations IS 'The json representation of the entity annotations that were derived by the schema of the entity.';
