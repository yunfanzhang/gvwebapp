use GameVideos;
alter table Video add column duration int(11) default 0;
alter table Game add Column description varchar(4096) default '';
alter table Game add Column cover varchar(1024) default '';
alter table Game add Column banner varchar(1024) default '';
alter table Game add Column banner_enabled  bool default False;
