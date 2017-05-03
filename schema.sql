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

insert into entries (originNode, destinationNode, pwID, localInterface, remoteInterface, vlanID, vplsID, customerName) values ('PE1','PE2','1000','Gi0/0','Gi0/0',100,'VLAN100','Claro');
insert into entries (originNode, destinationNode, pwID, localInterface, remoteInterface, vlanID, vplsID, customerName) values ('PE1','PE2','1000','Gi0/0','Gi0/0',100,'VLAN100','Claro');
insert into entries (originNode, destinationNode, pwID, localInterface, remoteInterface, vlanID, vplsID, customerName) values ('PE1','PE2','1000','Gi0/0','Gi0/0',100,'VLAN100','Claro');
insert into entries (originNode, destinationNode, pwID, localInterface, remoteInterface, vlanID, vplsID, customerName) values ('PE1','PE2','1000','Gi0/0','Gi0/0',100,'VLAN100','Claro');
insert into entries (originNode, destinationNode, pwID, localInterface, remoteInterface, vlanID, vplsID, customerName) values ('PE1','PE2','1000','Gi0/0','Gi0/0',100,'VLAN100','Claro');
