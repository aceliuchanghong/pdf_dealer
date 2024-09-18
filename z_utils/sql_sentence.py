create_rule_table_sql = """
CREATE TABLE IF NOT EXISTS rule_info (
  rule_name TEXT, 
  entity_name TEXT, 
  entity_format TEXT, 
  entity_regex_pattern TEXT, 
  rule_state TEXT, 
  latest_modified_insert TEXT, 
  remark TEXT
)
"""

select_rule_sql = """
SELECT 
  entity_name,
  entity_format,
  entity_regex_pattern,
  rule_state,
  latest_modified_insert,
  remark 
FROM rule_info
WHERE 
  rule_name = ? 
"""

insert_rule_sql = """
INSERT INTO rule_info (
  rule_name, 
  entity_name, 
  entity_format, 
  entity_regex_pattern, 
  rule_state, 
  latest_modified_insert, 
  remark
) 
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

update_rule_sql = """
UPDATE rule_info 
SET 
  entity_name = ?, 
  entity_format = ?, 
  entity_regex_pattern = ?, 
  rule_state = ?, 
  latest_modified_insert = ?, 
  remark = ? 
WHERE rule_name = ?
"""
