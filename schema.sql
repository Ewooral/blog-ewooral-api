CREATE TYPE chattype AS ENUM ('DIRECT', 'GROUP', 'BROADCAST', 'CHANNEL')
CREATE TYPE privacylevel AS ENUM ('EVERYONE', 'CONTACTS', 'NOBODY')
CREATE TYPE messagetype AS ENUM ('TEXT', 'IMAGE', 'VIDEO', 'AUDIO', 'VOICE', 'DOCUMENT', 'LOCATION', 'CONTACT', 'STICKER', 'GIF', 'POLL', 'STATUS', 'SYSTEM')
CREATE TYPE grouprole AS ENUM ('MEMBER', 'ADMIN', 'SUPER_ADMIN')
CREATE TYPE messagestatus AS ENUM ('SENDING', 'SENT', 'DELIVERED', 'READ', 'FAILED')

CREATE TABLE quote (
	id SERIAL NOT NULL, 
	uuid VARCHAR NOT NULL, 
	client_email VARCHAR NOT NULL, 
	service_type VARCHAR NOT NULL, 
	description VARCHAR, 
	status VARCHAR NOT NULL, 
	estimated_price DOUBLE PRECISION, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT quote_pkey PRIMARY KEY (id)
)


CREATE UNIQUE INDEX ix_quote_uuid ON quote (uuid)

CREATE TABLE contactmessage (
	id SERIAL NOT NULL, 
	uuid VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	phone VARCHAR, 
	service VARCHAR, 
	message VARCHAR(2000) NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT contactmessage_pkey PRIMARY KEY (id)
)


CREATE UNIQUE INDEX ix_contactmessage_uuid ON contactmessage (uuid)

CREATE TABLE "user" (
	id SERIAL NOT NULL, 
	uuid VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	hashed_password VARCHAR NOT NULL, 
	full_name VARCHAR, 
	phone_number VARCHAR, 
	avatar_url VARCHAR, 
	about VARCHAR, 
	is_active BOOLEAN NOT NULL, 
	is_admin BOOLEAN NOT NULL, 
	is_business BOOLEAN NOT NULL, 
	profile_photo_privacy VARCHAR NOT NULL, 
	last_seen_privacy VARCHAR NOT NULL, 
	status_privacy VARCHAR NOT NULL, 
	read_receipts_enabled BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT user_pkey PRIMARY KEY (id)
)


CREATE UNIQUE INDEX ix_user_uuid ON "user" (uuid)
CREATE UNIQUE INDEX ix_user_email ON "user" (email)
CREATE INDEX ix_user_phone_number ON "user" (phone_number)

CREATE TABLE role (
	id SERIAL NOT NULL, 
	name VARCHAR NOT NULL, 
	description VARCHAR, 
	CONSTRAINT role_pkey PRIMARY KEY (id)
)


CREATE UNIQUE INDEX ix_role_name ON role (name)

CREATE TABLE permission (
	id SERIAL NOT NULL, 
	name VARCHAR NOT NULL, 
	description VARCHAR, 
	CONSTRAINT permission_pkey PRIMARY KEY (id)
)


CREATE UNIQUE INDEX ix_permission_name ON permission (name)

CREATE TABLE user_contacts (
	user_id INTEGER NOT NULL, 
	contact_id INTEGER NOT NULL, 
	contact_name VARCHAR, 
	is_blocked BOOLEAN NOT NULL, 
	is_favorite BOOLEAN NOT NULL, 
	added_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT user_contacts_pkey PRIMARY KEY (user_id, contact_id), 
	CONSTRAINT user_contacts_contact_id_fkey FOREIGN KEY(contact_id) REFERENCES "user" (id), 
	CONSTRAINT user_contacts_user_id_fkey FOREIGN KEY(user_id) REFERENCES "user" (id)
)



CREATE TABLE chat (
	id SERIAL NOT NULL, 
	uuid VARCHAR NOT NULL, 
	type chattype NOT NULL, 
	name VARCHAR, 
	description VARCHAR, 
	avatar_url VARCHAR, 
	is_announcement_only BOOLEAN NOT NULL, 
	is_invite_link_enabled BOOLEAN NOT NULL, 
	invite_link VARCHAR, 
	max_participants INTEGER NOT NULL, 
	disappearing_messages_duration INTEGER, 
	is_archived BOOLEAN NOT NULL, 
	is_pinned BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	created_by_id INTEGER, 
	CONSTRAINT chat_pkey PRIMARY KEY (id), 
	CONSTRAINT chat_created_by_id_fkey FOREIGN KEY(created_by_id) REFERENCES "user" (id)
)


CREATE UNIQUE INDEX ix_chat_uuid ON chat (uuid)

CREATE TABLE user_presence (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	is_online BOOLEAN NOT NULL, 
	last_seen TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	status_message VARCHAR, 
	show_online_status privacylevel NOT NULL, 
	show_last_seen privacylevel NOT NULL, 
	show_read_receipts BOOLEAN NOT NULL, 
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT user_presence_pkey PRIMARY KEY (id), 
	CONSTRAINT user_presence_user_id_fkey FOREIGN KEY(user_id) REFERENCES "user" (id)
)


CREATE UNIQUE INDEX ix_user_presence_user_id ON user_presence (user_id)

CREATE TABLE story (
	id SERIAL NOT NULL, 
	uuid VARCHAR NOT NULL, 
	user_id INTEGER NOT NULL, 
	content VARCHAR, 
	media_url VARCHAR, 
	media_type messagetype, 
	privacy_level privacylevel NOT NULL, 
	duration INTEGER NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	expires_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT story_pkey PRIMARY KEY (id), 
	CONSTRAINT story_user_id_fkey FOREIGN KEY(user_id) REFERENCES "user" (id)
)


CREATE INDEX ix_story_user_id ON story (user_id)
CREATE UNIQUE INDEX ix_story_uuid ON story (uuid)

CREATE TABLE business_info (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	business_name VARCHAR NOT NULL, 
	category VARCHAR NOT NULL, 
	description VARCHAR, 
	website VARCHAR, 
	email VARCHAR, 
	address VARCHAR, 
	hours JSON, 
	is_verified BOOLEAN NOT NULL, 
	catalog_enabled BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT business_info_pkey PRIMARY KEY (id), 
	CONSTRAINT business_info_user_id_fkey FOREIGN KEY(user_id) REFERENCES "user" (id), 
	CONSTRAINT business_info_user_id_key UNIQUE NULLS DISTINCT (user_id)
)



CREATE TABLE backup_sessions (
	id SERIAL NOT NULL, 
	uuid VARCHAR NOT NULL, 
	user_id INTEGER NOT NULL, 
	backup_type VARCHAR NOT NULL, 
	file_path VARCHAR NOT NULL, 
	file_size INTEGER NOT NULL, 
	encryption_key_hash VARCHAR NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	expires_at TIMESTAMP WITHOUT TIME ZONE, 
	CONSTRAINT backup_sessions_pkey PRIMARY KEY (id), 
	CONSTRAINT backup_sessions_user_id_fkey FOREIGN KEY(user_id) REFERENCES "user" (id)
)


CREATE UNIQUE INDEX ix_backup_sessions_uuid ON backup_sessions (uuid)
CREATE INDEX ix_backup_sessions_user_id ON backup_sessions (user_id)

CREATE TABLE device_sessions (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	device_id VARCHAR NOT NULL, 
	device_name VARCHAR NOT NULL, 
	device_type VARCHAR NOT NULL, 
	os_name VARCHAR, 
	os_version VARCHAR, 
	app_version VARCHAR, 
	is_active BOOLEAN NOT NULL, 
	last_active TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	push_token VARCHAR, 
	login_timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	ip_address VARCHAR, 
	location VARCHAR, 
	CONSTRAINT device_sessions_pkey PRIMARY KEY (id), 
	CONSTRAINT device_sessions_user_id_fkey FOREIGN KEY(user_id) REFERENCES "user" (id)
)


CREATE INDEX ix_device_sessions_user_id ON device_sessions (user_id)
CREATE UNIQUE INDEX ix_device_sessions_device_id ON device_sessions (device_id)

CREATE TABLE userrolelink (
	user_id INTEGER NOT NULL, 
	role_id INTEGER NOT NULL, 
	CONSTRAINT userrolelink_pkey PRIMARY KEY (user_id, role_id), 
	CONSTRAINT userrolelink_role_id_fkey FOREIGN KEY(role_id) REFERENCES role (id), 
	CONSTRAINT userrolelink_user_id_fkey FOREIGN KEY(user_id) REFERENCES "user" (id)
)



CREATE TABLE rolepermissionlink (
	role_id INTEGER NOT NULL, 
	permission_id INTEGER NOT NULL, 
	CONSTRAINT rolepermissionlink_pkey PRIMARY KEY (role_id, permission_id), 
	CONSTRAINT rolepermissionlink_permission_id_fkey FOREIGN KEY(permission_id) REFERENCES permission (id), 
	CONSTRAINT rolepermissionlink_role_id_fkey FOREIGN KEY(role_id) REFERENCES role (id)
)



CREATE TABLE chat_participants (
	chat_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	role grouprole NOT NULL, 
	joined_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	is_muted BOOLEAN NOT NULL, 
	custom_notification_tone VARCHAR, 
	CONSTRAINT chat_participants_pkey PRIMARY KEY (chat_id, user_id), 
	CONSTRAINT chat_participants_chat_id_fkey FOREIGN KEY(chat_id) REFERENCES chat (id), 
	CONSTRAINT chat_participants_user_id_fkey FOREIGN KEY(user_id) REFERENCES "user" (id)
)



CREATE TABLE message (
	id SERIAL NOT NULL, 
	uuid VARCHAR NOT NULL, 
	content VARCHAR, 
	message_type messagetype NOT NULL, 
	metadata JSON, 
	chat_id INTEGER NOT NULL, 
	sender_id INTEGER NOT NULL, 
	reply_to_id INTEGER, 
	forwarded_from_id INTEGER, 
	thread_root_id INTEGER, 
	is_edited BOOLEAN NOT NULL, 
	is_deleted BOOLEAN NOT NULL, 
	is_pinned BOOLEAN NOT NULL, 
	is_starred BOOLEAN NOT NULL, 
	expires_at TIMESTAMP WITHOUT TIME ZONE, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	edited_at TIMESTAMP WITHOUT TIME ZONE, 
	CONSTRAINT message_pkey PRIMARY KEY (id), 
	CONSTRAINT message_chat_id_fkey FOREIGN KEY(chat_id) REFERENCES chat (id), 
	CONSTRAINT message_forwarded_from_id_fkey FOREIGN KEY(forwarded_from_id) REFERENCES message (id), 
	CONSTRAINT message_reply_to_id_fkey FOREIGN KEY(reply_to_id) REFERENCES message (id), 
	CONSTRAINT message_sender_id_fkey FOREIGN KEY(sender_id) REFERENCES "user" (id), 
	CONSTRAINT message_thread_root_id_fkey FOREIGN KEY(thread_root_id) REFERENCES message (id)
)


CREATE UNIQUE INDEX ix_message_uuid ON message (uuid)
CREATE INDEX ix_message_sender_id ON message (sender_id)
CREATE INDEX ix_message_chat_id ON message (chat_id)

CREATE TABLE typing_indicators (
	id SERIAL NOT NULL, 
	chat_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	is_typing BOOLEAN NOT NULL, 
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT typing_indicators_pkey PRIMARY KEY (id), 
	CONSTRAINT typing_indicators_chat_id_fkey FOREIGN KEY(chat_id) REFERENCES chat (id), 
	CONSTRAINT typing_indicators_user_id_fkey FOREIGN KEY(user_id) REFERENCES "user" (id)
)


CREATE INDEX ix_typing_indicators_chat_id ON typing_indicators (chat_id)
CREATE INDEX ix_typing_indicators_user_id ON typing_indicators (user_id)

CREATE TABLE story_views (
	id SERIAL NOT NULL, 
	story_id INTEGER NOT NULL, 
	viewer_id INTEGER NOT NULL, 
	viewed_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT story_views_pkey PRIMARY KEY (id), 
	CONSTRAINT story_views_story_id_fkey FOREIGN KEY(story_id) REFERENCES story (id), 
	CONSTRAINT story_views_viewer_id_fkey FOREIGN KEY(viewer_id) REFERENCES "user" (id)
)


CREATE INDEX ix_story_views_story_id ON story_views (story_id)
CREATE INDEX ix_story_views_viewer_id ON story_views (viewer_id)

CREATE TABLE call_logs (
	id SERIAL NOT NULL, 
	uuid VARCHAR NOT NULL, 
	chat_id INTEGER NOT NULL, 
	initiator_id INTEGER NOT NULL, 
	call_type VARCHAR NOT NULL, 
	started_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	ended_at TIMESTAMP WITHOUT TIME ZONE, 
	duration INTEGER, 
	status VARCHAR NOT NULL, 
	participants JSON, 
	CONSTRAINT call_logs_pkey PRIMARY KEY (id), 
	CONSTRAINT call_logs_chat_id_fkey FOREIGN KEY(chat_id) REFERENCES chat (id), 
	CONSTRAINT call_logs_initiator_id_fkey FOREIGN KEY(initiator_id) REFERENCES "user" (id)
)


CREATE INDEX ix_call_logs_chat_id ON call_logs (chat_id)
CREATE INDEX ix_call_logs_initiator_id ON call_logs (initiator_id)
CREATE UNIQUE INDEX ix_call_logs_uuid ON call_logs (uuid)

CREATE TABLE chat_settings (
	id SERIAL NOT NULL, 
	chat_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	is_muted BOOLEAN NOT NULL, 
	mute_until TIMESTAMP WITHOUT TIME ZONE, 
	custom_notification_tone VARCHAR, 
	wallpaper_url VARCHAR, 
	theme VARCHAR NOT NULL, 
	disappearing_messages_duration INTEGER, 
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT chat_settings_pkey PRIMARY KEY (id), 
	CONSTRAINT chat_settings_chat_id_fkey FOREIGN KEY(chat_id) REFERENCES chat (id), 
	CONSTRAINT chat_settings_user_id_fkey FOREIGN KEY(user_id) REFERENCES "user" (id), 
	CONSTRAINT chat_settings_chat_id_key UNIQUE NULLS DISTINCT (chat_id)
)



CREATE TABLE message_reactions (
	message_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	emoji VARCHAR NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT message_reactions_pkey PRIMARY KEY (message_id, user_id), 
	CONSTRAINT message_reactions_message_id_fkey FOREIGN KEY(message_id) REFERENCES message (id), 
	CONSTRAINT message_reactions_user_id_fkey FOREIGN KEY(user_id) REFERENCES "user" (id)
)



CREATE TABLE attachment (
	id SERIAL NOT NULL, 
	uuid VARCHAR NOT NULL, 
	message_id INTEGER NOT NULL, 
	file_name VARCHAR NOT NULL, 
	file_path VARCHAR NOT NULL, 
	file_size INTEGER NOT NULL, 
	mime_type VARCHAR NOT NULL, 
	thumbnail_path VARCHAR, 
	duration INTEGER, 
	width INTEGER, 
	height INTEGER, 
	metadata JSON, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT attachment_pkey PRIMARY KEY (id), 
	CONSTRAINT attachment_message_id_fkey FOREIGN KEY(message_id) REFERENCES message (id)
)


CREATE UNIQUE INDEX ix_attachment_uuid ON attachment (uuid)

CREATE TABLE message_status_records (
	id SERIAL NOT NULL, 
	message_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	status messagestatus NOT NULL, 
	timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT message_status_records_pkey PRIMARY KEY (id), 
	CONSTRAINT message_status_records_message_id_fkey FOREIGN KEY(message_id) REFERENCES message (id), 
	CONSTRAINT message_status_records_user_id_fkey FOREIGN KEY(user_id) REFERENCES "user" (id)
)


CREATE INDEX ix_message_status_records_message_id ON message_status_records (message_id)
CREATE INDEX ix_message_status_records_user_id ON message_status_records (user_id)

CREATE TABLE poll (
	id SERIAL NOT NULL, 
	message_id INTEGER NOT NULL, 
	question VARCHAR NOT NULL, 
	options JSON, 
	multiple_choice BOOLEAN NOT NULL, 
	anonymous BOOLEAN NOT NULL, 
	expires_at TIMESTAMP WITHOUT TIME ZONE, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT poll_pkey PRIMARY KEY (id), 
	CONSTRAINT poll_message_id_fkey FOREIGN KEY(message_id) REFERENCES message (id), 
	CONSTRAINT poll_message_id_key UNIQUE NULLS DISTINCT (message_id)
)



CREATE TABLE message_mentions (
	id SERIAL NOT NULL, 
	message_id INTEGER NOT NULL, 
	mentioned_user_id INTEGER NOT NULL, 
	start_index INTEGER NOT NULL, 
	length INTEGER NOT NULL, 
	CONSTRAINT message_mentions_pkey PRIMARY KEY (id), 
	CONSTRAINT message_mentions_mentioned_user_id_fkey FOREIGN KEY(mentioned_user_id) REFERENCES "user" (id), 
	CONSTRAINT message_mentions_message_id_fkey FOREIGN KEY(message_id) REFERENCES message (id)
)


CREATE INDEX ix_message_mentions_mentioned_user_id ON message_mentions (mentioned_user_id)
CREATE INDEX ix_message_mentions_message_id ON message_mentions (message_id)

CREATE TABLE message_reports (
	id SERIAL NOT NULL, 
	message_id INTEGER NOT NULL, 
	reported_by_id INTEGER NOT NULL, 
	reason VARCHAR NOT NULL, 
	description VARCHAR, 
	status VARCHAR NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	reviewed_at TIMESTAMP WITHOUT TIME ZONE, 
	reviewed_by_id INTEGER, 
	CONSTRAINT message_reports_pkey PRIMARY KEY (id), 
	CONSTRAINT message_reports_message_id_fkey FOREIGN KEY(message_id) REFERENCES message (id), 
	CONSTRAINT message_reports_reported_by_id_fkey FOREIGN KEY(reported_by_id) REFERENCES "user" (id), 
	CONSTRAINT message_reports_reviewed_by_id_fkey FOREIGN KEY(reviewed_by_id) REFERENCES "user" (id)
)


CREATE INDEX ix_message_reports_message_id ON message_reports (message_id)
CREATE INDEX ix_message_reports_reported_by_id ON message_reports (reported_by_id)

CREATE TABLE poll_votes (
	id SERIAL NOT NULL, 
	poll_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	option_index INTEGER NOT NULL, 
	voted_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT poll_votes_pkey PRIMARY KEY (id), 
	CONSTRAINT poll_votes_poll_id_fkey FOREIGN KEY(poll_id) REFERENCES poll (id), 
	CONSTRAINT poll_votes_user_id_fkey FOREIGN KEY(user_id) REFERENCES "user" (id)
)


CREATE INDEX ix_poll_votes_poll_id ON poll_votes (poll_id)
CREATE INDEX ix_poll_votes_user_id ON poll_votes (user_id)