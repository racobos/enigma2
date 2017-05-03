drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  originNode text not null,
  destinationNode text not null,
  pwID text not null,
  localInterface text not null,
  remoteInterface text not null,
  vlanID integer not null,
  vplsID text,
  customerName text not null
);
