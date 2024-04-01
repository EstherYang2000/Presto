SET SESSION enable_dynamic_filtering = true;
SELECT *
FROM (
    SELECT post.platform_user_id,
    post.platform_post_id,
    post.content,
    post.like_count,
    post.comment_count,
    post.share_count,
    post.view_count,
    post.play_count,
    post.url,
    post.is_video,
    post.is_live,
    post.is_disable_like,
    post.post_time
    FROM postgresql."data".latest_instagram_post as post
    WHERE post_time >= TIMESTAMP '2014-01-01' AND post_time <= TIMESTAMP '2023-12-31'
) AS post
LEFT JOIN (
    SELECT followers.kol_id,
    followers.platform_user_id,
    followers.platform,
    followers.week_num,
    followers.follower_count_processed,
    followers.follower_count_origin,
    followers.leng_diff,
    followers.normalized_std
    FROM postgresql."data".kol_followers as followers
    WHERE created_time >= TIMESTAMP '2014-01-01' AND created_time <= TIMESTAMP '2023-12-31'
) AS followers
ON post.platform_user_id = followers.platform_user_id;