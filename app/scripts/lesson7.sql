create table users (
    username varchar(50) primary key,
    password TEXT
);

create table tasks(
    id int primary key auto_increment,
    user varchar(50),
    task text,
    done bool default false
);



alter table tasks add foreign key tasks(user) references users(username);


insert into users (username, password)
values ('user1', '123'), ('user2', '456');

insert into tasks (user, task)
VALUES ('user1', 'task1'),
       ('user1', 'task2'),
       ('user2', 'task3'),
       ('user2', 'task4'),
       ('user2', 'task5')