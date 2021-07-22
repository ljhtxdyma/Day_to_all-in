# -*- coding: utf-8 -*-
"""
By LIU JIAHUI
"""
import tkinter as tk
import akshare as ak
from datetime import datetime
import pandas as pd

'''
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2. - 0.2, 1.03 * height, '%.2f%%' % (height * 100), fontsize=14)

def plotchart(final, name):
    y = final["日增长率"].values.tolist()
    y = y[0:5]
    x = ['周一', '周二', '周三', '周四', '周五']
    fig = plt.figure(figsize=(16, 16))
    delta = max(y) - min(y)
    ax = fig.add_subplot(1, 1, 1)
    plt.xticks(np.arange(len(x)), x)
    a = plt.bar(np.arange(len(x)), y, width=0.5, color='b')
    plt.title(name)
    ax.set_ylabel('涨跌概率')
    autolabel(a)
    plt.ylim((0.3, 0.8))
    # plt.legend(handles=[],labels=('%.2f%%' % (delta*100)),loc='upper right',fancybox=True, framealpha=0.1)
    plt.plot([], [], ' ', label=('概率差值：' + '%.2f%%' % (delta * 100)))
    plt.legend(loc='upper right', fancybox=False, framealpha=0, fontsize=14)
    fig.tight_layout(pad=3, w_pad=3.0, h_pad=5.0)
    plt.savefig(name + '.png')
    plt.show()
'''

def show_result(input_code):
    date = 260
    code=input_code
    try:
        df = ak.fund_em_open_fund_info(fund=code, indicator="单位净值走势")
    except:
        try:
            df = ak.fund_em_money_fund_info(fund=code, indicator="单位净值走势")
        except:
            try:
                df = ak.fund_em_financial_fund_info(fund=code, indicator="单位净值走势")
            except:
                try:
                    df = ak.fund_em_graded_fund_info(fund=code, indicator="单位净值走势")
                except:
                    try:
                        df = ak.fund_em_etf_fund_info(fund=code, indicator="单位净值走势")
                    except:
                        df=pd.DataFrame()

    if df.empty == False:
        df.dropna(axis=0, how='any', inplace=True)
        df.drop("单位净值", axis=1, inplace=True)
        j = 0
        for i in df["净值日期"]:
            weekday = datetime.strptime(str(i), "%Y-%m-%d").weekday()
            df.loc[[j], ["净值日期"]] = weekday
            j = j + 1

        df = df.astype(float)

        j = 0
        for i in df["日增长率"]:
            if i >= 0:
                df.loc[[j], ["日增长率"]] = 1
            else:
                df.loc[[j], ["日增长率"]] = 0
            j = j + 1

        final_df = df.tail(date)

        final = final_df.groupby(['净值日期']).mean()
        result = final["日增长率"].values.tolist()
        # plotchart(final, code)
        output= ("过去一年结果如下:"+'\n'+'\n'+"周一:" + str(round(result[0], 2)) + "  " + "周二:" + str(round(result[1],2)) + "  " + "周三:" + str(round(result[2],2)) + "  " + "周四:" + str(round(result[
            3],2)) + "  " + "周五:" + str(round(result[4],2)))
        return(output)
    else:
        output= ("查无信息！请确认基金代码是否正确。")
        return(output)


if __name__ == '__main__':
    root= tk.Tk()
    root.title("Day to All-in")
    root.geometry('400x300')
    canvas = tk.Canvas(root, width=400, height=135)
    image = tk.PhotoImage(file='image.gif')
    img= tk.Label(root, image=image)
    img.place(x=120, y=0)
    j = tk.Label(root, text="©2021-2031 LIU_JIAHUI All Rights Reserved", fg='black',font=("宋体", 8,"italic"))
    j.place(x=140, y=280)
    i = tk.Label(root, text="请输入基金代码：", fg='black')
    i.place(x=20, y=150)
    entry = tk.Entry(root,show = None)
    entry.place(x=120, y=150)

    def hello():
        text=show_result(str(entry.get()))
        t.set(text)



    button = tk.Button(root,text='确定', command=hello, bg='black', fg='white')
    button.place(x=300, y=145)

    t = tk.StringVar()
    l = tk.Label(root, textvariable=t,width=50, height=5, bg='white', fg='black')
    l.place(x=10, y=180)

    root.mainloop()




