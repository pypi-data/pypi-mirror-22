SELECT CONCAT(decodeIP(n.ipstart),'/',n.subnet) AS 'address'
    , COALESCE(n.hostname, '') AS 'hostname'
    , COALESCE(l_out.unique_out_ip, 0) AS 'unique_out_ip'
    , COALESCE(l_out.unique_out_conn, 0) AS 'unique_out_conn'
    , COALESCE(l_out.total_out, 0) AS 'total_out'
    , COALESCE(l_out.b_s, 0) AS 'out_bytes_sent'
    , COALESCE(l_out.b_r, 0) AS 'out_bytes_received'
    , COALESCE(l_out.max_bps, 0) AS 'out_max_bps'
    , COALESCE(l_out.sum_b * 1.0 / l_out.sum_duration, 0) AS 'out_avg_bps'
    , COALESCE(l_out.p_s, 0) AS 'out_packets_sent'
    , COALESCE(l_out.p_r, 0) AS 'out_packets_received'
    , COALESCE(l_out.sum_duration * 1.0 / l_out.total_out, 0) AS 'out_duration'
    , COALESCE(l_in.unique_in_ip, 0) AS 'unique_in_ip'
    , COALESCE(l_in.unique_in_conn, 0) AS 'unique_in_conn'
    , COALESCE(l_in.total_in, 0) AS 'total_in'
    , COALESCE(l_in.b_s, 0) AS 'in_bytes_sent'
    , COALESCE(l_in.b_r, 0) AS 'in_bytes_received'
    , COALESCE(l_in.max_bps, 0) AS 'in_max_bps'
    , COALESCE(l_in.sum_b * 1.0 / l_in.sum_duration, 0) AS 'in_avg_bps'
    , COALESCE(l_in.p_s, 0) AS 'in_packets_sent'
    , COALESCE(l_in.p_r, 0) AS 'in_packets_received'
    , COALESCE(l_in.sum_duration * 1.0 / l_in.total_in, 0) AS 'in_duration'
    , COALESCE(l_in.ports_used, 0) AS 'ports_used'
    , children.endpoints AS 'endpoints'
    , COALESCE(t.seconds, 0) + 300 AS 'seconds'
    , (COALESCE(l_in.sum_b, 0) + COALESCE(l_out.sum_b, 0)) / (COALESCE(t.seconds, 0) + 300) AS 'overall_bps'
    , COALESCE(l_in.protocol, "") AS 'in_protocols'
    , COALESCE(l_out.protocol, "") AS 'out_protocols'
FROM (
    SELECT ipstart, subnet, alias AS 'hostname'
    FROM s1_Nodes
    WHERE ipstart = 352321536 AND ipend = 369098751
) AS n
LEFT JOIN (
    SELECT 352321536 AS 's1'
    , COUNT(DISTINCT dst) AS 'unique_out_ip'
    , (SELECT COUNT(1) FROM (SELECT DISTINCT src, dst, port FROM s1_ds1_Links WHERE src BETWEEN 352321536 AND 369098751) AS `temp1`) AS 'unique_out_conn'
    , SUM(links) AS 'total_out'
    , SUM(bytes_sent) AS 'b_s'
    , SUM(bytes_received) AS 'b_r'
    , MAX((bytes_sent + bytes_received) * 1.0 / duration) AS 'max_bps'
    , SUM(bytes_sent + bytes_received) AS 'sum_b'
    , SUM(packets_sent) AS 'p_s'
    , SUM(packets_received) AS 'p_r'
    , SUM(duration * links) AS 'sum_duration'
    , GROUP_CONCAT(DISTINCT protocol) AS 'protocol'
    FROM s1_ds1_Links
    WHERE src BETWEEN 352321536 AND 369098751
    GROUP BY 's1'
) AS l_out
    ON n.ipstart = l_out.s1
LEFT JOIN (
    SELECT 352321536 AS 's1'
    , COUNT(DISTINCT src) AS 'unique_in_ip'
    , (SELECT COUNT(1) FROM (SELECT DISTINCT src, dst, port FROM s1_ds1_Links WHERE dst BETWEEN 352321536 AND 369098751) AS `temp2`) AS 'unique_in_conn'
    , SUM(links) AS 'total_in'
    , SUM(bytes_sent) AS 'b_s'
    , SUM(bytes_received) AS 'b_r'
    , MAX((bytes_sent + bytes_received) * 1.0 / duration) AS 'max_bps'
    , SUM(bytes_sent + bytes_received) AS 'sum_b'
    , SUM(packets_sent) AS 'p_s'
    , SUM(packets_received) AS 'p_r'
    , SUM(duration * links) AS 'sum_duration'
    , COUNT(DISTINCT port) AS 'ports_used'
    , GROUP_CONCAT(DISTINCT protocol) AS 'protocol'
    FROM s1_ds1_Links
    WHERE dst BETWEEN 352321536 AND 369098751
    GROUP BY 's1'
) AS l_in
    ON n.ipstart = l_in.s1
LEFT JOIN (
    SELECT 352321536 AS 's1'
    , COUNT(ipstart) AS 'endpoints'
    FROM s1_Nodes
    WHERE ipstart = ipend AND ipstart BETWEEN 352321536 AND 369098751
) AS children
    ON n.ipstart = children.s1
LEFT JOIN (
    SELECT 352321536 AS 's1'
        , (UNIX_TIMESTAMP(MAX(timestamp)) - UNIX_TIMESTAMP(MIN(timestamp))) AS 'seconds'
    FROM s1_ds1_Links
    GROUP BY 's1'
) AS t
    ON n.ipstart = t.s1
LIMIT 1;




SELECT CONCAT(decodeIP(n.ipstart),'/',n.subnet) AS 'address'
FROM (
    SELECT ipstart, subnet, alias AS 'hostname'
    FROM s1_Nodes
    WHERE ipstart = 352321536 AND ipend = 369098751
) AS n
LEFT JOIN (
    SELECT 352321536 AS 's1'
    , COUNT(DISTINCT dst) AS 'unique_out_ip'
    , (SELECT COUNT(1) FROM (SELECT DISTINCT src, dst, port FROM s1_ds1_Links WHERE src BETWEEN 352321536 AND 369098751) AS `temp1`) AS 'unique_out_conn'
    , SUM(links) AS 'total_out'
    , SUM(bytes_sent) AS 'b_s'
    , SUM(bytes_received) AS 'b_r'
    , MAX((bytes_sent + bytes_received) * 1.0 / duration) AS 'max_bps'
    , SUM(bytes_sent + bytes_received) AS 'sum_b'
    , SUM(packets_sent) AS 'p_s'
    , SUM(packets_received) AS 'p_r'
    , SUM(duration * links) AS 'sum_duration'
    , GROUP_CONCAT(DISTINCT protocol) AS 'protocol'
    FROM s1_ds1_Links
    WHERE src BETWEEN 352321536 AND 369098751
    GROUP BY 's1'
) AS l_out
    ON n.ipstart = l_out.s1
LEFT JOIN (
    SELECT 352321536 AS 's1'
    , COUNT(DISTINCT src) AS 'unique_in_ip'
    , (SELECT COUNT(1) FROM (SELECT DISTINCT src, dst, port FROM s1_ds1_Links WHERE dst BETWEEN 352321536 AND 369098751) AS `temp2`) AS 'unique_in_conn'
    , SUM(links) AS 'total_in'
    , SUM(bytes_sent) AS 'b_s'
    , SUM(bytes_received) AS 'b_r'
    , MAX((bytes_sent + bytes_received) * 1.0 / 1) AS 'max_bps'
    , SUM(bytes_sent + bytes_received) AS 'sum_b'
    , SUM(packets_sent) AS 'p_s'
    , SUM(packets_received) AS 'p_r'
    , SUM(duration * links) AS 'sum_duration'
    , COUNT(DISTINCT port) AS 'ports_used'
    , GROUP_CONCAT(DISTINCT protocol) AS 'protocol'
    FROM s1_ds1_Links
    WHERE dst BETWEEN 352321536 AND 369098751
    GROUP BY 's1'
) AS l_in
    ON n.ipstart = l_in.s1
LEFT JOIN (
    SELECT 352321536 AS 's1'
    , COUNT(ipstart) AS 'endpoints'
    FROM s1_Nodes
    WHERE ipstart = ipend AND ipstart BETWEEN 352321536 AND 369098751
) AS children
    ON n.ipstart = children.s1
LEFT JOIN (
    SELECT 352321536 AS 's1'
        , (UNIX_TIMESTAMP(MAX(timestamp)) - UNIX_TIMESTAMP(MIN(timestamp))) AS 'seconds'
    FROM s1_ds1_Links
    GROUP BY 's1'
) AS t
    ON n.ipstart = t.s1
LIMIT 1;
