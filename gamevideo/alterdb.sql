use GameVideos;
ALTER TABLE Video ADD COLUMN duration int(11) default 0;
ALTER TABLE Game ADD COLUMN description varchar(4096) default '';
alter table Game add Column cover varchar(1024) default '';
alter table Game add Column banner varchar(1024) default '';
alter table Game add Column banner_enabled  bool default False;

CREATE TABLE `User` (
	`user_id` int(11) NOT NULL AUTO_INCREMENT,
	`user_name` varchar(64) COLLATE utf8_bin  NOT NULL,
	`password` varchar(64) NOT NULL,
	`user_type` int(11) DEFAULT NULL COMMENT '0: Unknown. 1: local. 2: QQ. 3: Weibo',
	PRIMARY KEY (`user_id`)
	) ENGINE=InnoDB AUTO_INCREMENT=273868 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `Comment` (
	`comment_id` int(11) NOT NULL AUTO_INCREMENT,
	`message` text COLLATE utf8_bin,
	`wrote` datetime DEFAULT NULL,
	`video_id` int(11) NOT NULL,
	`user_id` int(11) NOT NULL,
	PRIMARY KEY (`comment_id`)
	) ENGINE=InnoDB AUTO_INCREMENT=273868 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `Liked` (
	`liked_id` int(11) NOT NULL AUTO_INCREMENT,
	`video_id` int(11) NOT NULL,
	`user_id` int(11) NOT NULL,
	PRIMARY KEY (`liked_id`),
	UNIQUE KEY `VideoUserPair` (`video_id`, `user_id`)
	) ENGINE=InnoDB AUTO_INCREMENT=273868 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `OnlineVideo` (
	`video_id` int(11) NOT NULL,
	`source_id` int(11) DEFAULT NULL,
	`game_id` int(11) DEFAULT NULL,
	`href` varchar(64) COLLATE utf8_bin DEFAULT NULL,
	`log_vid` varchar(45) COLLATE utf8_bin DEFAULT NULL,
	`title` varchar(128) COLLATE utf8_bin DEFAULT NULL,
	`uploader_id` int(11) DEFAULT NULL,
	`play` int(11) DEFAULT NULL,
	`published` datetime DEFAULT NULL,
	`downloadLinks` text COLLATE utf8_bin,
	`tags` text COLLATE utf8_bin,
	`good` int(11) DEFAULT NULL COMMENT '0: Unknow. 1: Good Game Video. 2:Bad Game Video.',
	`imgSrc` varchar(255) COLLATE utf8_bin DEFAULT NULL,
	`yes_prob` double DEFAULT '0',
	`no_prob` double DEFAULT '0',
	`summary` text COLLATE utf8_bin,
	`flash` varchar(255) COLLATE utf8_bin DEFAULT NULL,
	`duration` int(11) DEFAULT '0',
	PRIMARY KEY (`video_id`),
	UNIQUE KEY `log_vid_UNIQUE` (`log_vid`)
	) ENGINE=InnoDB AUTO_INCREMENT=273868 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


    alter table OnlineVideo add Column liked_count int(11) default NULL;
