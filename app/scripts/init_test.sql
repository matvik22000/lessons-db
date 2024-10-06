drop table if exists `test`;
create table `test`
(
    field1 INT,
    field2 TEXT
);
insert into `test` (field1, field2)
values (1, 'test1'),
       (2, 'test2')