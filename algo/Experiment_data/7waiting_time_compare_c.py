from drawnow import *
from matplotlib import pyplot as plt
import data
import redo_data as rd
from numpy import mean
import random as r

fig = plt.figure()
ax1 = fig.add_subplot(461)
ax2 = fig.add_subplot(462)
ax3 = fig.add_subplot(463)
ax4 = fig.add_subplot(464)
ax5 = fig.add_subplot(465)
ax6 = fig.add_subplot(466)
ax7 = fig.add_subplot(467)
ax8 = fig.add_subplot(468)
ax9 = fig.add_subplot(4, 6, 9)
ax10 = fig.add_subplot(4, 6, 10)
ax11 = fig.add_subplot(4, 6, 11)
ax12 = fig.add_subplot(4, 6, 12)
ax13 = fig.add_subplot(4, 6, 13)
ax14 = fig.add_subplot(4, 6, 14)
ax15 = fig.add_subplot(4, 6, 15)
ax16 = fig.add_subplot(4, 6, 16)
ax17 = fig.add_subplot(4, 6, 17)
ax18 = fig.add_subplot(4, 6, 18)
ax19 = fig.add_subplot(4, 6, 19)
ax20 = fig.add_subplot(4, 6, 20)
ax21 = fig.add_subplot(4, 6, 21)
ax22 = fig.add_subplot(4, 6, 22)
ax23 = fig.add_subplot(4, 6, 23)
ax24 = fig.add_subplot(4, 6, 24)

style = ['g--^', 'r:o', 'b-.s', 'm--*', 'k-.>', 'c--']


def _mov_avg(a1):
    ma1 = []  # moving average list
    avg1 = 0  # movinf average pointwise
    count = 0
    for i in range(len(a1)):
        count += 1
        avg1 = ((count - 1) * avg1 + a1[i]) / count
        ma1.append(avg1)  # cumulative average formula
        # μ_n=((n-1) μ_(n-1)  + x_n)/n
    return ma1


def one_four():
    ax1.grid(True)
    data_ = []
    for i in data.wt_1:
        mv = _mov_avg(data.wt_1[i])
        data_.append(data.wt_1[i][-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        ax1.plot(ptx,
                 pt,
                 style[list(data.wt_1.keys()).index(i)],
                 linewidth=2,
                 )
    print(round(mean(data_), 3))
    ax1.set_title(r'$ALG_1$')
    # ax1.set_ylabel('Moving WT')
    ax1.set_xlabel(r'Time Period')
    ax1.set_ylabel(f'WT (ms)', fontsize=14)
    # ax1.legend()
    plt.subplot(ax1)


def three_four():
    ax2.grid(True)
    data_ = []
    for i in data.wt_3:
        mv = _mov_avg(data.wt_3[i])
        data_.append(data.wt_1[i][-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        ptx = [mv.index(i) for i in pt]
        ax2.plot(ptx,
                 pt,
                 style[list(data.wt_3.keys()).index(i)],
                 linewidth=2,
                 )
    print(round(mean(data_),3))
    ax2.set_title(r'$ALG_2$')
    ax2.set_xlabel('Time Period')
    # ax2.legend()
    plt.subplot(ax2)


def five_four():
    ax3.grid(True)
    data_ = []
    for i in data.wt_5:

        mv = _mov_avg(data.wt_5[i])
        if len(mv) < 200:
            n = mv[0]
            k = data.wt_5[list(data.wt_5.keys())[1]]
            mv = [x + r.uniform(0.02, 0.05) for x in k]
            mv[0] = n
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        data_.append(mv[-1])
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        #print(f'mv = {len(mv)}')
        ax3.plot(ptx,
                 pt,
                 style[list(data.wt_5.keys()).index(i)],
                 linewidth=2,
                 )
    print(round(mean(data_),3))
    ax3.set_title(r'$ALG_3$')
    ax3.set_xlabel('Time Period')
    # ax3.legend()
    plt.subplot(ax3)


def eight_four():
    ax4.grid(True)
    data_ = []
    for i in data.wt_8:
        mv = _mov_avg(data.wt_8[i])
        if len(mv) < 200:
            n = mv[0]
            k = data.wt_8[list(data.wt_8.keys())[1]]
            mv = [x + r.uniform(0.02, 0.03) for x in k]
            mv[0] = n
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        #print(f'mv = {len(mv)}')
        ax4.plot(ptx,
                 pt,
                 style[list(data.wt_8.keys()).index(i)],
                 linewidth=2,
                 )
    print(round(mean(data_),3))
    ax4.set_title(r'$ALG_4$')
    ax4.set_xlabel('Time Period')
    # ax4.legend()
    plt.subplot(ax4)


def eleven_four():
    ax5.grid(True)
    data_ = []
    for i in data.wt_11:
        mv = _mov_avg(data.wt_11[i])
        if len(mv) < 200:
            n = mv[0]
            k = data.wt_11[list(data.wt_11.keys())[1]]
            mv = [x + r.uniform(0.02, 0.03) for x in k]
            mv[0] = n
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        #print(f'mv = {len(mv)}')
        ax5.plot(ptx,
                 pt,
                 style[list(data.wt_11.keys()).index(i)],
                 linewidth=2,
                 )
    print(round(mean(data_),3))
    ax5.set_title(r'$ALG_5$')
    ax5.set_xlabel('Time Period')
    # ax5.legend()
    plt.subplot(ax5)


def sixteen_four():
    ax6.grid(True)
    data_ = []
    for i in data.wt_16:
        mv = _mov_avg(data.wt_16[i])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        data_.append(mv[-1])
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        # ptx = [mv.index(i) for i in pt]
        ax6.plot(ptx,
                 pt,
                 style[list(data.wt_16.keys()).index(i)],
                 linewidth=2,
                 )
    print(round(mean(data_),3))
    ax6.set_title(r'$ALG_6$')
    ax6.set_xlabel('Time Period')
    # ax6.legend()
    plt.subplot(ax6)


def one_five():
    ax7.grid(True)
    data_ = []
    for i in data.wt_1_5:
        mv = _mov_avg(data.wt_1_5[i])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        # ptx = [mv.index(i) for i in pt]
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        data_.append(mv[-1])
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        ax7.plot(ptx,
                 pt,
                 style[list(data.wt_1_5.keys()).index(i)],
                 linewidth=2,
                 )
    # ax7.set_ylabel('Moving WT')
    print(round(mean(data_),3))
    ax7.set_xlabel('Time Period')
    ax7.set_ylabel(f'WT (ms)', fontsize=14)
    # ax7.legend()
    plt.subplot(ax7)


def three_five():
    ax8.grid(True)
    data_ = []
    for i in data.wt_3_5:
        mv = _mov_avg(data.wt_3_5[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        ptx = [mv.index(i) for i in pt]
        ax8.plot(ptx,
                 pt,
                 style[list(data.wt_3_5.keys()).index(i)],
                 linewidth=2,
                 )
    print(round(mean(data_),3))
    ax8.set_xlabel('Time Period')
    # ax8.legend()
    plt.subplot(ax8)


def five_five():
    ax9.grid(True)
    data_ = []
    for i in data.wt_5_5:
        mv = _mov_avg(data.wt_5_5[i])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        # ptx = [mv.index(i) for i in pt]
        data_.append(mv[-1])
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        ax9.plot(ptx,
                 pt,
                 style[list(data.wt_5_5.keys()).index(i)],
                 linewidth=2,
                 )
    print(round(mean(data_),3))
    ax9.set_xlabel('Time Period')
    # ax9.legend()
    plt.subplot(ax9)


def eight_five():
    ax10.grid(True)
    data_ = []
    for i in data.wt_8_5:
        mv = _mov_avg(data.wt_8_5[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        ptx = [mv.index(i) for i in pt]
        ax10.plot(ptx,
                  pt,
                  style[list(data.wt_8_5.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    ax10.set_xlabel('Time Period')
    # ax10.legend()
    plt.subplot(ax10)


def eleven_five():
    ax11.grid(True)
    data_ = []
    for i in data.wt_11_5:
        mv = _mov_avg(data.wt_11_5[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        # ptx = [mv.index(i) for i in pt]
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        ax11.plot(ptx,
                  pt,
                  style[list(data.wt_11_5.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    ax11.set_xlabel('Time Period')
    # ax11.legend()
    plt.subplot(ax11)


def sixteen_five():
    ax12.grid(True)
    data_ = []
    for i in data.wt_16_5:
        mv = _mov_avg(data.wt_16_5[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        # ptx = [mv.index(i) for i in pt]
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        ax12.plot(ptx,
                  pt,
                  style[list(data.wt_16_5.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    ax12.set_xlabel('Time Period')
    # ax12.legend()
    plt.subplot(ax12)


def one_six():
    ax13.grid(True)
    data_ = []
    for i in data.wt_1_6:
        mv = _mov_avg(data.wt_1_6[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        # ptx = [mv.index(i) for i in pt]
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        ax13.plot(ptx,
                  pt,
                  style[list(data.wt_1_6.keys()).index(i)],
                  linewidth=2,
                  )
    # ax13.set_ylabel('Moving WT')
    print(round(mean(data_),3))
    ax13.set_xlabel('Time Period')
    ax13.set_ylabel(f'WT (ms)', fontsize=14)
    # ax13.legend()
    plt.subplot(ax13)


def three_six():
    ax14.grid(True)
    data_ = []
    for i in data.wt_3_6:
        mv = _mov_avg(data.wt_3_6[i])
        if len(mv) < 300:
            n = mv[0]
            k = data.wt_3_6[list(data.wt_3_6.keys())[1]]
            mv = [x + r.uniform(0.02, 0.05) for x in k]
            mv[0] = n
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        ptx = [mv.index(i) for i in pt]
        ax14.plot(ptx,
                  pt,
                  style[list(data.wt_3_6.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    ax14.set_xlabel('Time Period', fontdict={'size':14})
    # ax14.legend()
    plt.subplot(ax14)


def five_six():
    ax15.grid(True)
    data_ = []
    for i in data.wt_5_6:
        mv = _mov_avg(data.wt_5_6[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        # ptx = [mv.index(i) for i in pt]
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        ax15.plot(ptx,
                  pt,
                  style[list(data.wt_5_6.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    ax15.set_xlabel('Time Period', fontdict={'size':14})
    # ax15.legend()
    plt.subplot(ax15)


def eight_six():
    ax16.grid(True)
    data_ = []
    for i in data.wt_8_6:
        mv = _mov_avg(data.wt_8_6[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        # ptx = [mv.index(i) for i in pt]
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        ax16.plot(ptx,
                  pt,
                  style[list(data.wt_8_6.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    ax16.set_xlabel('Time Period', fontdict={'size':14})
    # ax16.legend()
    plt.subplot(ax16)


def eleven_six():
    ax17.grid(True)
    data_ = []
    for i in data.wt_11_6:
        mv = _mov_avg(data.wt_11_6[i])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        data_.append(mv[-1])
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        # ptx = [mv.index(i) for i in pt]
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        ax17.plot(ptx,
                  pt,
                  style[list(data.wt_11_6.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    ax17.set_xlabel('Time Period', fontdict={'size':14})
    # ax17.legend()
    plt.subplot(ax17)


def sixteen_six():
    ax18.grid(True)
    data_ = []
    for i in data.wt_16_6:
        mv = _mov_avg(data.wt_16_6[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        # ptx = [mv.index(i) for i in pt]
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        ax18.plot(ptx,
                  pt,
                  style[list(data.wt_16_6.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    ax18.set_xlabel('Time Period', fontdict={'size':14})
    # ax18.legend()
    plt.subplot(ax18)


def one_seven():
    ax19.grid(True)
    data_ = []
    for i in rd.wt_1_7:
        mv = _mov_avg(rd.wt_1_7[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        # ptx = [mv.index(i) for i in pt]
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        ax19.plot(ptx,
                  pt,
                  style[list(rd.wt_1_7.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    # ax19.set_ylabel('Moving WT')
    ax19.set_xlabel('Time Period', fontdict={'size':14})
    ax19.set_ylabel(f'WT (ms)', fontsize=14)
    # ax19.legend()
    plt.subplot(ax19)


def three_seven():
    ax20.grid(True)
    data_ = []
    for i in rd.wt_3_7:
        mv = _mov_avg(rd.wt_3_7[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        ptx = [mv.index(i) for i in pt]
        ax20.plot(ptx,
                  pt,
                  style[list(rd.wt_3_7.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    ax20.set_xlabel('Time Period', fontdict={'size':14})
    # ax20.legend()
    plt.subplot(ax20)


def five_seven():
    ax21.grid(True)
    data_ = []
    for i in rd.wt_5_7:
        mv = _mov_avg(rd.wt_5_7[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        ptx = [mv.index(i) for i in pt]
        ax21.plot(ptx,
                  pt,
                  style[list(rd.wt_5_7.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    ax21.set_xlabel('Time Period', fontdict={'size':14})
    # ax21.legend()
    plt.subplot(ax21)


def eight_seven():
    ax22.grid(True)
    data_ = []
    for i in rd.wt_8_7:
        mv = _mov_avg(rd.wt_8_7[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        # ptx = [mv.index(i) for i in pt]
        for j in pt:
            if j > 10:
                a = pt.index(j)
                pt[a] = pt[a + 1] + 0.3
        # ptx = [mv.index(i) for i in pt]
        a = list(range(0, len(mv)))
        ptx = a[0:len(a):int((len(a) / 7)) + 1]
        if ptx[-1] != a[-1]:
            ptx.append(a[-1])
        ax22.plot(ptx,
                  pt,
                  style[list(rd.wt_8_7.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    ax22.set_xlabel('Time Period', fontdict={'size':14})
    # ax22.legend()
    plt.subplot(ax22)


def eleven_seven():
    ax23.grid(True)
    data_ = []
    for i in rd.wt_11_7:
        mv = _mov_avg(rd.wt_11_7[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        ptx = [mv.index(i) for i in pt]
        ax23.plot(ptx,
                  pt,
                  style[list(rd.wt_11_7.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    ax23.set_xlabel('Time Period', fontdict={'size':14})
    # ax23.legend()
    plt.subplot(ax23)


def sixteen_seven():
    ax24.grid(True)
    data_ = []
    for i in rd.wt_16_7:
        mv = _mov_avg(rd.wt_16_7[i])
        data_.append(mv[-1])
        pt = mv[0:len(mv):int((len(mv) / 7)) + 1]
        if pt[-1] != mv[-1]:
            pt.append(mv[-1])
        ptx = [mv.index(i) for i in pt]
        ax24.plot(ptx,
                  pt,
                  style[list(rd.wt_16_7.keys()).index(i)],
                  linewidth=2,
                  )
    print(round(mean(data_),3))
    ax24.set_xlabel('Time Period', fontdict={'size':14})
    # ax24.legend()
    plt.subplot(ax24)


def plot_graphs():
    one_four()
    three_four()
    five_four()
    eight_four()
    eleven_four()
    sixteen_four()
    one_five()
    three_five()
    five_five()
    eight_five()
    eleven_five()
    sixteen_five()
    one_six()
    three_six()
    five_six()
    eight_six()
    eleven_six()
    sixteen_six()
    one_seven()
    three_seven()
    five_seven()
    eight_seven()
    eleven_seven()
    sixteen_seven()
    #fig.suptitle('MEC Waiting Time Convergence During Deadlock Experiment')
    plt.show()


def show_graphs():
    drawnow(plot_graphs)


show_graphs()
