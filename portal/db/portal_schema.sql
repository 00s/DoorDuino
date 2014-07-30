-- Schema for portal application

-- Cards are the one read by rfid-shield
create table card (
  uid         text primary key not null,
  name 				text,
  mail        text
);


-- used to indicate when an authorized card was read by the system
create table entrance(
  id           integer primary key autoincrement not null,
  entrance		 date,
  card      	 text not null references project(uid)
);
