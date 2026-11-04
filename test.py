


new_data = [{"date": "2026-10-21", "type": "income", "name": "เงินเดือน", "amount": 5000.0},{"date": "2026-10-21", "type": "expense", "name": "เติมเกม", "amount": 300.0},{"date": "2026-1-21", "type": "expense", "name": "เสื้อยืด", "amount": 500.0}]
'''
def sum_by_mount(new_data):
    sum={}
    for s in new_data:
        mount_years = s["date"][:7]
        if mount_years not in sum:
            sum[mount_years] = 0
        if s["type"] == 'income':
            sum[mount_years] += s["amount"]
        elif s["type"] == 'expense':
            sum[mount_years] -= s["amount"]
    return sum

x = sum_by_mount(new_data)
print(x)
'''
def sum_by_month(new_data):
    insum = {}
    exsum = {}
    for s in new_data:
        month = s['date'][:7]
        if s['type'] == 'income':
            insum[month] = insum.get(month, 0) + s['amount']
        if s['type'] == 'expense':
            exsum[month] = exsum.get(month, 0) + s['amount']
    print(f"รายได้รวม = {insum}")
    print(f"รายจ่ายรวม = {exsum}")
    return insum,exsum

def total_balance(insum, exsum):
    balance = {}
    for month in set(insum.keys()).union(exsum.keys()):
        balance[month] = insum.get(month, 0) - exsum.get(month, 0)
    return balance

insum, exsum = sum_by_month(new_data)
balance = total_balance(insum, exsum)

print(f"ยอดคงเหลือ = {balance}")