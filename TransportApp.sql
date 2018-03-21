create table TransportApp_signin
	(id int identity(1001,1) primary key,
	 FirstName nvarchar(50) not null,
	 LastName nvarchar(50) not null,
	 Password nvarchar(50) not null default '',
	 Email nvarchar(50) not null,
	 PhoneNumber nvarchar(15) not null,
	 Hashkey nvarchar(50) not null,
	 active bit not null default 0,
	)

select * from TransportApp_signin


truncate table TransportApp_signin
drop table TransportApp_signin