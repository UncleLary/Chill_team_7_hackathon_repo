
CREATE TABLE public."user" (
	profile_picture_url varchar(200) NULL,
	full_name varchar(75) NULL,
	id uuid NOT NULL,
	email varchar(320) NOT NULL,
	hashed_password varchar(1024) NOT NULL,
	is_active bool NOT NULL,
	is_superuser bool NOT NULL,
	is_verified bool NOT NULL,
	rec_date timestamp DEFAULT now() NOT NULL,
	is_profile_complete bool DEFAULT false NOT NULL,
	CONSTRAINT user_pkey PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);

CREATE TABLE public.accesstoken (
	user_id uuid NOT NULL,
	"token" varchar(43) NOT NULL,
	created_at timestamptz NOT NULL,
	CONSTRAINT accesstoken_pkey PRIMARY KEY (token)
);
CREATE INDEX ix_accesstoken_created_at ON public.accesstoken USING btree (created_at);


-- public.accesstoken foreign keys

ALTER TABLE public.accesstoken ADD CONSTRAINT accesstoken_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;

CREATE TABLE public.oauth_account (
	id uuid NOT NULL,
	user_id uuid NOT NULL,
	oauth_name varchar(100) NOT NULL,
	access_token varchar(1024) NOT NULL,
	expires_at int4 NULL,
	refresh_token varchar(1024) NULL,
	account_id varchar(320) NOT NULL,
	account_email varchar(320) NOT NULL,
	CONSTRAINT oauth_account_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_oauth_account_account_id ON public.oauth_account USING btree (account_id);
CREATE INDEX ix_oauth_account_oauth_name ON public.oauth_account USING btree (oauth_name);


-- public.oauth_account foreign keys

ALTER TABLE public.oauth_account ADD CONSTRAINT oauth_account_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;
