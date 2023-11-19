insert into users (user_id, id, password, email, activated)
values (1, 'admin', '$2a$08$lDnHPz7eUkSi6ao14Twuau08mzhWrL4kyZGGU5xfiGALO/Vxd5DOi', 'admin@example.com', 1);

insert into auth (auth) values ('ROLE_USER');
insert into auth (auth) values ('ROLE_ADMIN');

insert into user_auth (user_id, auth) values (1, 'ROLE_USER');
insert into user_auth (user_id, auth) values (1, 'ROLE_ADMIN');