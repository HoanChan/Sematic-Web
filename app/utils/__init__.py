def toDate(date):
    if date: 
        dateParts = date.split("-")
        if len(dateParts) == 3: # Xử lý ngày tháng năm do bên js giởi lên có dạng yyyy-mm-dd
            date = dateParts[2] + '/' + dateParts[1] + '/' + dateParts[0]
    return date