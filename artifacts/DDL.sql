-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

-- DROP SEQUENCE public.clientes_id_seq;

CREATE SEQUENCE public.clientes_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.produtos_id_seq;

CREATE SEQUENCE public.produtos_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.transacoes_id_seq;

CREATE SEQUENCE public.transacoes_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- public.clientes definição

-- Drop table

-- DROP TABLE public.clientes;

CREATE TABLE public.clientes (
	id serial4 NOT NULL,
	nome varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	data_criacao timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT clientes_email_key UNIQUE (email),
	CONSTRAINT clientes_pkey PRIMARY KEY (id)
);


-- public.produtos definição

-- Drop table

-- DROP TABLE public.produtos;

CREATE TABLE public.produtos (
	id serial4 NOT NULL,
	nome varchar(255) NOT NULL,
	preco numeric(10, 2) NOT NULL,
	CONSTRAINT produtos_pkey PRIMARY KEY (id)
);


-- public.transacoes definição

-- Drop table

-- DROP TABLE public.transacoes;

CREATE TABLE public.transacoes (
	id serial4 NOT NULL,
	id_cliente int4 NULL,
	id_produto int4 NULL,
	data_transacao timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	quantidade int4 NOT NULL,
	total numeric(10, 2) NOT NULL,
	CONSTRAINT transacoes_pkey PRIMARY KEY (id),
	CONSTRAINT transacoes_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES public.clientes(id) ON DELETE CASCADE,
	CONSTRAINT transacoes_id_produto_fkey FOREIGN KEY (id_produto) REFERENCES public.produtos(id) ON DELETE CASCADE
);