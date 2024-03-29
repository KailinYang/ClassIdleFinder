from flask import Flask, render_template, request
import main

db = main.get_db()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        option1 = request.form.get("option1") # Day of week
        option2 = request.form.get("option2") # Class time 
        option3 = request.form.get("option3", default=1, type=int) # Week number

        data = main.query(db, option2, option1, option3)
        print(option1, option2, option3, data)
        
        params = {
            "option1": option1,
            "option2": option2,
            "option3": str(option3),
            "data": data,
            "weekOptions": [["2",'2(2.26-3.3)'], ["3",'3(3.4-3.10)'], ["4",'4(3.11-3.17)'], ["5",'5(3.18-3.24)'], ["6",'6(3.25-3.31)'],["7",'7(4.1-4.7)'], ["8",'8(4.8-4.14)'], ["9",'9(4.15-4.21)'], ["10",'10(4.22-4.28)'], ["11",'11(4.29-5.5)'], ["12",'12(5.6-5.12)'], ["13",'13(5.13-5.19)'], ["14",'14(5.20-5.26)'], ["15",'15(5.27-6.2)'], ["16",'16(6.3-6.9)'], ["17",'17(6.10-6.16)'], ["18",'18(6.17-6.23)'], ["19",'14(6.24-6.30)']],
            "dayOptions" : ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"],
            "timeOptions": [["一",'第1-2节(8:20-10:00)'], ["二",'第3-4节(10:20-12:00)'], ["三",'第5-6节(14:00-15:40)'], ["四",'第7-8节(16:00-17:40)'], ["五",'第9-10节(18:30-20:00)']]
        }
        return render_template("./index.html", **params)

    params = {
        "weekOptions": [["2",'2(2.26-3.3)'], ["3",'3(3.4-3.10)'], ["4",'4(3.11-3.17)'], ["5",'5(3.18-3.24)'], ["6",'6(3.25-3.31)'],["7",'7(4.1-4.7)'], ["8",'8(4.8-4.14)'], ["9",'9(4.15-4.21)'], ["10",'10(4.22-4.28)'], ["11",'11(4.29-5.5)'], ["12",'12(5.6-5.12)'], ["13",'13(5.13-5.19)'], ["14",'14(5.20-5.26)'], ["15",'15(5.27-6.2)'], ["16",'16(6.3-6.9)'], ["17",'17(6.10-6.16)'], ["18",'18(6.17-6.23)'], ["19",'14(6.24-6.30)']],
        "dayOptions" : ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"],
        "timeOptions": [["一",'第1-2节(8:20-10:00)'], ["二",'第3-4节(10:20-12:00)'], ["三",'第5-6节(14:00-15:40)'], ["四",'第7-8节(16:00-17:40)'], ["五",'第9-10节(18:30-20:00)']]
    }
    return render_template("index.html", **params)