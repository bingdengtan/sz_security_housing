MonthlySqlMapping = {
    'insert': "insert into data_monthly (userid, creditid, name, seqno, applyNo, num, place) values ('%s', '%s', '%s', %d, '%s', %d, '%s')",
    'delete': "delete from data_monthly"
}

TodaySqlMapping = {
    'insert': "insert into data_today (userid, creditid, name, seqno, applyNo, num, place) values (%s, %s, %s, %s, %s, %s, %s)",
    'delete': "delete from data_today"
}

