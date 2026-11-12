import json
import datetime

def save_item(new_data):
    with open("cashbook.json", "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False)

def load_item():
    try:
        with open("cashbook.json", "r", encoding="utf-8") as f:
            data =json.load(f)
            return data
    except FileNotFoundError:
        print("ไม่มีไฟล์หรือหาไฟล์ไม่เจอหรือไม่มีรายการในบันทึก")
        return[]
    except json.JSONDecodeError:
        print("ไฟล์ข้อมูลเสียหาย เริ่มรายการใหม่")
        return []

def get_item():
        item = input("ระบุรายการที่ต้องการเพิ่ม = ").strip()
        if not item:
            print("ไม่พบชื่อรายการ")
            return get_item()
        return item

def get_amount():
    while True:
        try:
            amount = float(input("ระบุจำนวนเงิน ="))
            if amount < 0:
                print("กรุณาระบุตัวเลขในช่วงบวก")
            else:
                return amount
        except ValueError:
            print("กรุณาระบุตัวเลขให้ถูกต้อง")  


def add_item_expense(new_data,date_str):
    item = get_item()
    amount = get_amount()
    
    new_data.append({"date": date_str, "type": "expense", "name": item, "amount": amount})
    print(f"รายการที่เพิ่ม: '{item}' จำนวนเงิน: {amount} บาท.")

def add_item_income(new_data,date_str):
    item = get_item()
    amount = get_amount()
    
    new_data.append({"date": date_str, "type": "income", "name": item, "amount": amount})
    print(f"รายการที่เพิ่ม: '{item}' จำนวนเงิน: {amount} บาท.")

def type_label(item_type):
    if item_type == "income":
        return "รายรับ"
    if item_type == "expense":
        return "รายจ่าย"
    return "ไม่ทราบประเภท"

def type_option():
    try:
        return int(input(
            "เลือกรายการที่ต้องการ:\n"
            "กด 1 เพื่อบันทึกรายรับ\n"
            "กด 2 เพื่อบันทึกรายจ่าย\n"
            "กด 3 เพื่อดูบันทึก\n"
            "กด 4 เพื่อสรุปรายรับรายจ่าย\n"
            "กด 5 เพื่อลบรายการตาม index\n"
            "กด 6 เพื่อจบการทำงาน\n"
        ))
    except ValueError:
        print("กรุณากรอกตัวเลขให้ถูกต้อง") 

def delete_item(new_data):
    if not new_data:
        print("ไม่มีรายการที่สามารถลบได้")
        return False

    print("---เลือกรายการที่ต้องการลบ---")
    for index, item in enumerate(new_data, start=1):
        type_th = type_label(item["type"])
        print(f"{index}. วันที่: {item['date']} | {type_th}: {item['name']} | จำนวนเงิน: {item['amount']:,.2f} บาท")

    try:
        index = int(input("ระบุ index ของรายการที่ต้องการลบ: "))
    except ValueError:
        print("กรุณากรอก index เป็นตัวเลข")
        return False

    if index < 1 or index > len(new_data):
        print("ไม่พบรายการตาม index ที่ระบุ")
        return False

    deleted_item = new_data.pop(index - 1)
    print(f"ลบรายการ '{deleted_item['name']}' เรียบร้อยแล้ว")
    return True

def sum_by_month(new_data):
    insum = {}
    exsum = {}
    for s in new_data:
        month = s['date'][:7]
        if s['type'] == 'income':
            insum[month] = round(insum.get(month, 0) + s['amount'],2)
        if s['type'] == 'expense':
            exsum[month] = round(exsum.get(month, 0) + s['amount'],2)
    return insum,exsum

def total_balance(insum, exsum):
    balance = {}
    for month in set(insum.keys()).union(exsum.keys()):
        balance[month] = round(insum.get(month, 0) - exsum.get(month, 0), 2)
    return balance  

def core_program():
    new_data = load_item()

    while True:
        today = datetime.date.today()
        date_str = today.isoformat()
        num = type_option()
        if num == 1:
            add_item_income(new_data,date_str)
            save_item(new_data)
        elif num == 2:
            add_item_expense(new_data,date_str)
            save_item(new_data)
        elif num == 3:
            if not new_data:
                print("---สรุปรายการบัญชี---")
                print("ไม่มีรายการที่บันทึก")
            elif new_data:
                print("---สรุปรายการบัญชี---")
                for index, item in enumerate(new_data, start=1):
                    type_th = type_label(item["type"])
                    print(f"{index}. วันที่: {item['date']} | {type_th}: {item['name']} | จำนวนเงิน: {item['amount']:,.2f} บาท")
        elif num == 4:
            insum, exsum = sum_by_month(new_data)
            balance = total_balance(insum, exsum)
            for month, amount in insum.items():
                print(f"รายได้เดือน {month} = {amount} บาท")
            for month, amount in exsum.items():
                print(f"รายจ่ายเดือน {month} = {amount} บาท")

            print(f"ยอดคงเหลือ = {balance}")
        elif num == 5:
            if delete_item(new_data):
                save_item(new_data)
        elif num == 6:
            print("จบการทำงาน")
            break
        else:
            print("กรุณาเลือกรายการตามที่กำหนด")
        


core_program() 