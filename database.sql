CREATE TABLE reminder(
    id serial not null,
    when_data timestamp not null,
    gld_id varchar(50) not null,
    ch_id varchar(50) not null,
    say_user_id varchar(50) not null,
    message_id varchar(50),
    custom_message varchar(50) not null
);