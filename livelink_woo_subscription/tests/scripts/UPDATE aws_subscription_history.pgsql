UPDATE aws_subscription_history
SET state = 'new', serial_id = NULL


SELECT * FROM aws_subscription_history

SELECT * FROM sale_subscription


SELECT s.id
FROM stock_move_line l, stock_move m,
    procurement_group g, sale_order s
WHERE m.id = l.move_id AND g.id = m.group_id
    AND s.id = g.sale_id
    AND lot_id = 36919
LIMIT 1


SELECT s.id, *
FROM stock_move_line l, stock_production_lot t,
    stock_move m, procurement_group g, sale_order s
WHERE l.lot_id = t.id
    AND m.id = l.move_id AND g.id = m.group_id
    AND s.id = g.sale_id
    AND t.name = 'FMU02611'
    AND l.company_id = 1
LIMIT 1