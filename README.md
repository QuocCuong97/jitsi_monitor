# Tool giám sát thông số phòng họp Jitsi Meet
### Các thông số giám sát :
- Số phòng đang mở
- Tổng số người tham dự
- Tên phòng
- Chủ trì phòng họp (nếu có)
- Số người tham dự trong từng phòng
### Đưa ra thông số tại thời điểm hiện tại :
```
python3 now.py
```
- Output :
```
--------------------ACTIVE ROOMS--------------------
----------------------------------------------------
Trạng thái domain testings123.space
------------------------
Số phòng đang mở: 2
Số người tham dự: 5
       + newroom [admin]  ->  2 người tham dự
       + hop-giao-ban [admin3]  ->  3 người tham dự
----------------------------------------------------
```
### Đưa ra thông số theo real-time :
```
python3 real.py
```
- Output :
```
--------------------ACTIVE ROOMS--------------------
----------------------------------------------------
Trạng thái domain testings123.space
------------------------
Số phòng đang mở: 2
Số người tham dự: 5
------------------------
       + newroom [admin]  ->  2 người tham dự
       + hop-giao-ban [admin3]  ->  3 người tham dự
----------------------------------------------------
----------------(Ctrl + Z) for Quit-----------------
Updating...
/
```
### Đọc log thông số hiển thị lần gần nhất :
```
cat output.json
```
```json
[
    {
        "total_room": 2,
        "total_participants": 5
    },
    [
        {
            "name": "newroom",
            "participants": 2,
            "host": "admin"
        },
        {
            "name": "hop-giao-ban",
            "participants": 3,
            "host": "admin3"
        }
    ]
]
```