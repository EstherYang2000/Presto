SET SESSION enable_dynamic_filtering = true;

SELECT
    post.platform_user_id,
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
    post.post_time,
    hermes.id,
    hermes.platform,
    hermes.post_id,
    hermes.post_time,
    hermes.model_output,
    hermes.version,
    hermes.created_at,
    hermes.updated_at,
    hermes.deleted_at
FROM
    postgresql.data.latest_instagram_post as post 
LEFT JOIN postgresql.data.ml_post_hermes AS hermes on post.platform_post_id = hermes.post_id
And post.post_time = hermes.post_time;
