CREATE TABLE `news` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `rid` varchar(256) NOT NULL COMMENT '业务唯一标志',
  `tag` varchar(16) NOT NULL COMMENT '标签',
  `category` varchar(16) NOT NULL COMMENT '类别',
  `title` varchar(256) NOT NULL COMMENT '标题',
  `publish_time` datetime DEFAULT NULL COMMENT '发布时间',
  `content` MEDIUMTEXT NOT NULL COMMENT '正文',
  `created_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modified_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY udx_news_rid_tag (`rid`,`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 COLLATE=utf8mb4_0900_ai_ci COMMENT='新闻表'