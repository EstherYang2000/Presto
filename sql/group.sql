SELECT platform, COUNT(*) AS count
FROM postgresql."data".latest_audience
GROUP BY platform
ORDER BY count DESC;