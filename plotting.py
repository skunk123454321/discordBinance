import base64
import io
import seaborn as sns

sns.set_theme(style="darkgrid")
sns.set(rc={'figure.figsize': (19.2, 10.8)})


def get_line_plot(symbol: str, data) -> io.BytesIO:
    # sns.lineplot(x="time", y="price", data=data)
    # fig = sns.get_figure()
    # # plt.show()
    # print()
    svm = sns.lineplot(x="time (EST)", y="price", data=data)
    svm.set_title(symbol.upper())
    fig = svm.get_figure()
    pic_io_bytes = io.BytesIO()
    fig.savefig(pic_io_bytes, format='jpg')
    pic_io_bytes.seek(0)
    # return base64.b64encode(pic_io_bytes.read())
    return pic_io_bytes


# if __name__ == '__main__':
#     prices = []
#     times = []
#     for i in range(200):
#         prices.append(i + random.random())
#         times.append(datetime.now().strftime("%m/%d/%Y %H:%M:%S:%f"))
#     svm = sns.lineplot(x="time", y="price", data=pd.DataFrame({"price": prices, "time": times}))
#     fig = svm.get_figure()
#     pic_io_bytes = io.BytesIO()
#     fig.savefig(pic_io_bytes, format='jpg')
#     pic_io_bytes.seek(0)
#     pic_hash = base64.b64encode(pic_io_bytes.read())



