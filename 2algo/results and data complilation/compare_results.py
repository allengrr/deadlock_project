import results_data as rd

time_av_t = {'_4_2': 10374,
             '_5_2': 11052,
             '_6_2': 10861,

             '_4_3': 6465,
             '_5_3': 8200,
             '_6_3': 10791,

             '_4_7': 10329,
             '_5_7': 10951,
             '_6_7': 10136,

             '_4_10': 6721,
             '_5_10': 7418,
             '_6_10': 10913,

             '_4_12': 9172,
             '_5_12': 10441,
             '_6_12': 9618,

             '_4_16': 8364,
             '_5_16': 9225,
             '_6_16': 8536,

             }
time_av_u = {
    '_4_2': 544,
    '_5_2': 111,
    '_6_2': 211,

    '_4_3': 4479,
    '_5_3': 2898,
    '_6_3': 165,

    '_4_7': 580,
    '_5_7': 218,
    '_6_7': 919,

    '_4_10': 4193,
    '_5_10': 3743,
    '_6_10': 170,

    '_4_12': 1717,
    '_5_12': 651,
    '_6_12': 1337,

    '_4_16': 2527,
    '_5_16': 1855,
    '_6_16': 2396

}

_time = {2: {
    'timely': [rd.timely3_2_4, rd.timely4_2_4, rd.timely5_2_4, rd.timely3_2_5, rd.timely4_2_5,
               rd.timely5_2_5,
               rd.timely3_2_6,
               rd.timely4_2_6,
               rd.timely5_2_6,
               ],
    'untimely': [rd.untimely3_2_4, rd.untimely4_2_4, rd.untimely5_2_4, rd.untimely3_2_5, rd.untimely4_2_5,
                 rd.untimely5_2_5,
                 rd.untimely3_2_6,
                 rd.untimely4_2_6,
                 rd.untimely5_2_6,
                 ]
},
    3: {
        'timely': [rd.timely3_3_4, rd.timely4_3_4, rd.timely5_3_4, rd.timely3_3_5, rd.timely4_3_5,
                   rd.timely5_3_5,
                   rd.timely3_3_6,
                   rd.timely4_3_6,
                   rd.timely5_3_6,
                   ],
        'untimely': [rd.untimely3_3_4, rd.untimely4_3_4, rd.untimely5_3_4, rd.untimely3_3_5, rd.untimely4_3_5,
                     rd.untimely5_3_5,
                     rd.untimely3_3_6,
                     rd.untimely4_3_6,
                     rd.untimely5_3_6,
                     ]
    },
    7: {
        'timely': [rd.timely3_7_4, rd.timely4_7_4, rd.timely5_7_4, rd.timely3_7_5, rd.timely4_7_5,
                   rd.timely5_7_5,
                   rd.timely3_7_6,
                   rd.timely4_7_6,
                   rd.timely5_7_6,
                   ],
        'untimely': [rd.untimely3_7_4, rd.untimely4_7_4, rd.untimely5_7_4, rd.untimely3_7_5, rd.untimely4_7_5,
                     rd.untimely5_7_5,
                     rd.untimely3_7_6,
                     rd.untimely4_7_6,
                     rd.untimely5_7_6,
                     ],
    },
    10: {
        'timely': [rd.timely3_10_4, rd.timely4_10_4, rd.timely5_10_4, rd.timely3_10_5, rd.timely4_10_5,
                   rd.timely5_10_5,
                   rd.timely3_10_6,
                   rd.timely4_10_6,
                   rd.timely5_10_6,
                   ],
        'untimely': [rd.untimely3_10_4, rd.untimely4_10_4, rd.untimely5_10_4, rd.untimely3_10_5, rd.untimely4_10_5,
                     rd.untimely5_10_5,
                     rd.untimely3_10_6,
                     rd.untimely4_10_6,
                     rd.untimely5_10_6,
                     ],
    },
    12: {
        'timely': [rd.timely3_12_4, rd.timely4_12_4, rd.timely5_12_4, rd.timely3_12_5, rd.timely4_12_5,
                   rd.timely5_12_5,
                   rd.timely3_12_6,
                   rd.timely4_12_6,
                   rd.timely5_12_6,
                   ],
        'untimely': [rd.untimely3_12_4, rd.untimely4_12_4, rd.untimely5_12_4, rd.untimely3_12_5, rd.untimely4_12_5,
                     rd.untimely5_12_5,
                     rd.untimely3_12_6,
                     rd.untimely4_12_6,
                     rd.untimely5_12_6,
                     ],
    },
    16: {
        'timely': [rd.timely3_16_4, rd.timely4_16_4, rd.timely5_16_4, rd.timely3_16_5, rd.timely4_16_5,
                   rd.timely5_16_5,
                   rd.timely3_16_6,
                   rd.timely4_16_6,
                   rd.timely5_16_6,
                   ],
        'untimely': [rd.untimely3_16_4, rd.untimely4_16_4, rd.untimely5_16_4, rd.untimely3_16_5, rd.untimely4_16_5,
                     rd.untimely5_16_5,
                     rd.untimely3_16_6,
                     rd.untimely4_16_6,
                     rd.untimely5_16_6,
                     ],
    }
}

wait_time = {
    24: [rd.wt0_2_4, rd.wt1_2_4, rd.wt2_2_4, rd.wt3_2_4],
    25: [rd.wt0_2_5, rd.wt1_2_5, rd.wt2_2_5, rd.wt3_2_5, rd.wt4_2_5, ],
    26: [rd.wt0_2_6, rd.wt1_2_6, rd.wt2_2_6, rd.wt3_2_6, rd.wt4_2_6, rd.wt5_2_6],

    34: [rd.wt0_3_4, rd.wt1_3_4, rd.wt2_3_4, rd.wt3_3_4],
    35: [rd.wt0_3_5, rd.wt1_3_5, rd.wt2_3_5, rd.wt3_3_5, rd.wt4_3_5],
    36: [rd.wt0_3_6, rd.wt1_3_6, rd.wt2_3_6, rd.wt3_3_6, rd.wt4_3_6, rd.wt5_3_6],

    74: [rd.wt0_7_4, rd.wt1_7_4, rd.wt2_7_4, rd.wt3_7_4],
    75: [rd.wt0_7_5, rd.wt1_7_5, rd.wt2_7_5, rd.wt3_7_5, rd.wt4_7_5],
    76: [rd.wt0_7_6, rd.wt1_7_6, rd.wt2_7_6, rd.wt3_7_6, rd.wt4_7_6, rd.wt5_7_6],

    104: [rd.wt0_10_4, rd.wt1_10_4, rd.wt2_10_4, rd.wt3_10_4],
    105: [rd.wt0_10_5, rd.wt1_10_5, rd.wt2_10_5, rd.wt3_10_5, rd.wt4_10_5],
    106: [rd.wt0_10_6, rd.wt1_10_6, rd.wt2_10_6, rd.wt3_10_6, rd.wt4_10_6, rd.wt5_10_6],

    124: [rd.wt0_12_4, rd.wt1_12_4, rd.wt2_12_4, rd.wt3_12_4],
    125: [rd.wt0_12_5, rd.wt1_12_5, rd.wt2_12_5, rd.wt3_12_5, rd.wt4_12_5],
    126: [rd.wt0_12_6, rd.wt1_12_6, rd.wt2_12_6, rd.wt3_12_6, rd.wt4_12_6, rd.wt5_12_6],

    164: [rd.wt0_16_4, rd.wt1_16_4, rd.wt2_16_4, rd.wt3_16_4],
    165: [rd.wt0_16_5, rd.wt1_16_5, rd.wt2_16_5, rd.wt3_16_5, rd.wt4_16_5],
    166: [rd.wt0_16_6, rd.wt1_16_6, rd.wt2_16_6, rd.wt3_16_6, rd.wt4_16_6, rd.wt5_16_6],
}

_rtt_ = {
    24: [rd.rtt0_2_4, rd.rtt1_2_4, rd.rtt2_2_4, rd.rtt3_2_4],
    25: [rd.rtt0_2_5, rd.rtt1_2_5, rd.rtt2_2_5, rd.rtt3_2_5, rd.rtt4_2_5, ],
    26: [rd.rtt0_2_6, rd.rtt1_2_6, rd.rtt2_2_6, rd.rtt3_2_6, rd.rtt4_2_6, rd.rtt5_2_6],

    34: [rd.rtt0_3_4, rd.rtt1_3_4, rd.rtt2_3_4, rd.rtt3_3_4],
    35: [rd.rtt0_3_5, rd.rtt1_3_5, rd.rtt2_3_5, rd.rtt3_3_5, rd.rtt4_3_5],
    36: [rd.rtt0_3_6, rd.rtt1_3_6, rd.rtt2_3_6, rd.rtt3_3_6, rd.rtt4_3_6, rd.rtt5_3_6],

    74: [rd.rtt0_7_4, rd.rtt1_7_4, rd.rtt2_7_4, rd.rtt3_7_4],
    75: [rd.rtt0_7_5, rd.rtt1_7_5, rd.rtt2_7_5, rd.rtt3_7_5, rd.rtt4_7_5],
    76: [rd.rtt0_7_6, rd.rtt1_7_6, rd.rtt2_7_6, rd.rtt3_7_6, rd.rtt4_7_6, rd.rtt5_7_6],

    104: [rd.rtt0_10_4, rd.rtt1_10_4, rd.rtt2_10_4, rd.rtt3_10_4],
    105: [rd.rtt0_10_5, rd.rtt1_10_5, rd.rtt2_10_5, rd.rtt3_10_5, rd.rtt4_10_5],
    106: [rd.rtt0_10_6, rd.rtt1_10_6, rd.rtt2_10_6, rd.rtt3_10_6, rd.rtt4_10_6, rd.rtt5_10_6],

    124: [rd.rtt0_12_4, rd.rtt1_12_4, rd.rtt2_12_4, rd.rtt3_12_4],
    125: [rd.rtt0_12_5, rd.rtt1_12_5, rd.rtt2_12_5, rd.rtt3_12_5, rd.rtt4_12_5],
    126: [rd.rtt0_12_6, rd.rtt1_12_6, rd.rtt2_12_6, rd.rtt3_12_6, rd.rtt4_12_6, rd.rtt5_12_6],

    164: [rd.rtt0_16_4, rd.rtt1_16_4, rd.rtt2_16_4, rd.rtt3_16_4],
    165: [rd.rtt0_16_5, rd.rtt1_16_5, rd.rtt2_16_5, rd.rtt3_16_5, rd.rtt4_16_5],
    166: [rd.rtt0_16_6, rd.rtt1_16_6, rd.rtt2_16_6, rd.rtt3_16_6, rd.rtt4_16_6, rd.rtt5_16_6],
}

_cpu_ = {
    24: [rd.cpu0_2_4, rd.cpu1_2_4, rd.cpu2_2_4, rd.cpu3_2_4],
    25: [rd.cpu0_2_5, rd.cpu1_2_5, rd.cpu2_2_5, rd.cpu3_2_5, rd.cpu4_2_5, ],
    26: [rd.cpu0_2_6, rd.cpu1_2_6, rd.cpu2_2_6, rd.cpu3_2_6, rd.cpu4_2_6, rd.cpu5_2_6],

    34: [rd.cpu0_3_4, rd.cpu1_3_4, rd.cpu2_3_4, rd.cpu3_3_4],
    35: [rd.cpu0_3_5, rd.cpu1_3_5, rd.cpu2_3_5, rd.cpu3_3_5, rd.cpu4_3_5],
    36: [rd.cpu0_3_6, rd.cpu1_3_6, rd.cpu2_3_6, rd.cpu3_3_6, rd.cpu4_3_6, rd.cpu5_3_6],

    74: [rd.cpu0_7_4, rd.cpu1_7_4, rd.cpu2_7_4, rd.cpu3_7_4],
    75: [rd.cpu0_7_5, rd.cpu1_7_5, rd.cpu2_7_5, rd.cpu3_7_5, rd.cpu4_7_5],
    76: [rd.cpu0_7_6, rd.cpu1_7_6, rd.cpu2_7_6, rd.cpu3_7_6, rd.cpu4_7_6, rd.cpu5_7_6],

    104: [rd.cpu0_10_4, rd.cpu1_10_4, rd.cpu2_10_4, rd.cpu3_10_4],
    105: [rd.cpu0_10_5, rd.cpu1_10_5, rd.cpu2_10_5, rd.cpu3_10_5, rd.cpu4_10_5],
    106: [rd.cpu0_10_6, rd.cpu1_10_6, rd.cpu2_10_6, rd.cpu3_10_6, rd.cpu4_10_6, rd.cpu5_10_6],

    124: [rd.cpu0_12_4, rd.cpu1_12_4, rd.cpu2_12_4, rd.cpu3_12_4],
    125: [rd.cpu0_12_5, rd.cpu1_12_5, rd.cpu2_12_5, rd.cpu3_12_5, rd.cpu4_12_5],
    126: [rd.cpu0_12_6, rd.cpu1_12_6, rd.cpu2_12_6, rd.cpu3_12_6, rd.cpu4_12_6, rd.cpu5_12_6],

    164: [rd.cpu0_16_4, rd.cpu1_16_4, rd.cpu2_16_4, rd.cpu3_16_4],
    165: [rd.cpu0_16_5, rd.cpu1_16_5, rd.cpu2_16_5, rd.cpu3_16_5, rd.cpu4_16_5],
    166: [rd.cpu0_16_6, rd.cpu1_16_6, rd.cpu2_16_6, rd.cpu3_16_6, rd.cpu4_16_6, rd.cpu5_16_6],
}

_loc_ = {
    24: [rd.loc0_2_4, rd.loc1_2_4, rd.loc2_2_4, rd.loc3_2_4],
    25: [rd.loc0_2_5, rd.loc1_2_5, rd.loc2_2_5, rd.loc3_2_5, rd.loc4_2_5, ],
    26: [rd.loc0_2_6, rd.loc1_2_6, rd.loc2_2_6, rd.loc3_2_6, rd.loc4_2_6, rd.loc5_2_6],

    34: [rd.loc0_3_4, rd.loc1_3_4, rd.loc2_3_4, rd.loc3_3_4],
    35: [rd.loc0_3_5, rd.loc1_3_5, rd.loc2_3_5, rd.loc3_3_5, rd.loc4_3_5],
    36: [rd.loc0_3_6, rd.loc1_3_6, rd.loc2_3_6, rd.loc3_3_6, rd.loc4_3_6, rd.loc5_3_6],

    74: [rd.loc0_7_4, rd.loc1_7_4, rd.loc2_7_4, rd.loc3_7_4],
    75: [rd.loc0_7_5, rd.loc1_7_5, rd.loc2_7_5, rd.loc3_7_5, rd.loc4_7_5],
    76: [rd.loc0_7_6, rd.loc1_7_6, rd.loc2_7_6, rd.loc3_7_6, rd.loc4_7_6, rd.loc5_7_6],

    104: [rd.loc0_10_4, rd.loc1_10_4, rd.loc2_10_4, rd.loc3_10_4],
    105: [rd.loc0_10_5, rd.loc1_10_5, rd.loc2_10_5, rd.loc3_10_5, rd.loc4_10_5],
    106: [rd.loc0_10_6, rd.loc1_10_6, rd.loc2_10_6, rd.loc3_10_6, rd.loc4_10_6, rd.loc5_10_6],

    124: [rd.loc0_12_4, rd.loc1_12_4, rd.loc2_12_4, rd.loc3_12_4],
    125: [rd.loc0_12_5, rd.loc1_12_5, rd.loc2_12_5, rd.loc3_12_5, rd.loc4_12_5],
    126: [rd.loc0_12_6, rd.loc1_12_6, rd.loc2_12_6, rd.loc3_12_6, rd.loc4_12_6, rd.loc5_12_6],

    164: [rd.loc0_16_4, rd.loc1_16_4, rd.loc2_16_4, rd.loc3_16_4],
    165: [rd.loc0_16_5, rd.loc1_16_5, rd.loc2_16_5, rd.loc3_16_5, rd.loc4_16_5],
    166: [rd.loc0_16_6, rd.loc1_16_6, rd.loc2_16_6, rd.loc3_16_6, rd.loc4_16_6, rd.loc5_16_6],
}

_off_cloud_ = {
    24: [rd.off_cloud0_2_4, rd.off_cloud1_2_4, rd.off_cloud2_2_4, rd.off_cloud3_2_4],
    25: [rd.off_cloud0_2_5, rd.off_cloud1_2_5, rd.off_cloud2_2_5, rd.off_cloud3_2_5, rd.off_cloud4_2_5, ],
    26: [rd.off_cloud0_2_6, rd.off_cloud1_2_6, rd.off_cloud2_2_6, rd.off_cloud3_2_6, rd.off_cloud4_2_6,
         rd.off_cloud5_2_6],

    34: [rd.off_cloud0_3_4, rd.off_cloud1_3_4, rd.off_cloud2_3_4, rd.off_cloud3_3_4],
    35: [rd.off_cloud0_3_5, rd.off_cloud1_3_5, rd.off_cloud2_3_5, rd.off_cloud3_3_5, rd.off_cloud4_3_5],
    36: [rd.off_cloud0_3_6, rd.off_cloud1_3_6, rd.off_cloud2_3_6, rd.off_cloud3_3_6, rd.off_cloud4_3_6,
         rd.off_cloud5_3_6],

    74: [rd.off_cloud0_7_4, rd.off_cloud1_7_4, rd.off_cloud2_7_4, rd.off_cloud3_7_4],
    75: [rd.off_cloud0_7_5, rd.off_cloud1_7_5, rd.off_cloud2_7_5, rd.off_cloud3_7_5, rd.off_cloud4_7_5],
    76: [rd.off_cloud0_7_6, rd.off_cloud1_7_6, rd.off_cloud2_7_6, rd.off_cloud3_7_6, rd.off_cloud4_7_6,
         rd.off_cloud5_7_6],

    104: [rd.off_cloud0_10_4, rd.off_cloud1_10_4, rd.off_cloud2_10_4, rd.off_cloud3_10_4],
    105: [rd.off_cloud0_10_5, rd.off_cloud1_10_5, rd.off_cloud2_10_5, rd.off_cloud3_10_5, rd.off_cloud4_10_5],
    106: [rd.off_cloud0_10_6, rd.off_cloud1_10_6, rd.off_cloud2_10_6, rd.off_cloud3_10_6, rd.off_cloud4_10_6,
          rd.off_cloud5_10_6],

    124: [rd.off_cloud0_12_4, rd.off_cloud1_12_4, rd.off_cloud2_12_4, rd.off_cloud3_12_4],
    125: [rd.off_cloud0_12_5, rd.off_cloud1_12_5, rd.off_cloud2_12_5, rd.off_cloud3_12_5, rd.off_cloud4_12_5],
    126: [rd.off_cloud0_12_6, rd.off_cloud1_12_6, rd.off_cloud2_12_6, rd.off_cloud3_12_6, rd.off_cloud4_12_6,
          rd.off_cloud5_12_6],

    164: [rd.off_cloud0_16_4, rd.off_cloud1_16_4, rd.off_cloud2_16_4, rd.off_cloud3_16_4],
    165: [rd.off_cloud0_16_5, rd.off_cloud1_16_5, rd.off_cloud2_16_5, rd.off_cloud3_16_5, rd.off_cloud4_16_5],
    166: [rd.off_cloud0_16_6, rd.off_cloud1_16_6, rd.off_cloud2_16_6, rd.off_cloud3_16_6, rd.off_cloud4_16_6,
          rd.off_cloud5_16_6],
}

_off_mec_ = {
    24: [rd.off_mec0_2_4, rd.off_mec1_2_4, rd.off_mec2_2_4, rd.off_mec3_2_4],
    25: [rd.off_mec0_2_5, rd.off_mec1_2_5, rd.off_mec2_2_5, rd.off_mec3_2_5, rd.off_mec4_2_5, ],
    26: [rd.off_mec0_2_6, rd.off_mec1_2_6, rd.off_mec2_2_6, rd.off_mec3_2_6, rd.off_mec4_2_6, rd.off_mec5_2_6],

    34: [rd.off_mec0_3_4, rd.off_mec1_3_4, rd.off_mec2_3_4, rd.off_mec3_3_4],
    35: [rd.off_mec0_3_5, rd.off_mec1_3_5, rd.off_mec2_3_5, rd.off_mec3_3_5, rd.off_mec4_3_5],
    36: [rd.off_mec0_3_6, rd.off_mec1_3_6, rd.off_mec2_3_6, rd.off_mec3_3_6, rd.off_mec4_3_6, rd.off_mec5_3_6],

    74: [rd.off_mec0_7_4, rd.off_mec1_7_4, rd.off_mec2_7_4, rd.off_mec3_7_4],
    75: [rd.off_mec0_7_5, rd.off_mec1_7_5, rd.off_mec2_7_5, rd.off_mec3_7_5, rd.off_mec4_7_5],
    76: [rd.off_mec0_7_6, rd.off_mec1_7_6, rd.off_mec2_7_6, rd.off_mec3_7_6, rd.off_mec4_7_6, rd.off_mec5_7_6],

    104: [rd.off_mec0_10_4, rd.off_mec1_10_4, rd.off_mec2_10_4, rd.off_mec3_10_4],
    105: [rd.off_mec0_10_5, rd.off_mec1_10_5, rd.off_mec2_10_5, rd.off_mec3_10_5, rd.off_mec4_10_5],
    106: [rd.off_mec0_10_6, rd.off_mec1_10_6, rd.off_mec2_10_6, rd.off_mec3_10_6, rd.off_mec4_10_6, rd.off_mec5_10_6],

    124: [rd.off_mec0_12_4, rd.off_mec1_12_4, rd.off_mec2_12_4, rd.off_mec3_12_4],
    125: [rd.off_mec0_12_5, rd.off_mec1_12_5, rd.off_mec2_12_5, rd.off_mec3_12_5, rd.off_mec4_12_5],
    126: [rd.off_mec0_12_6, rd.off_mec1_12_6, rd.off_mec2_12_6, rd.off_mec3_12_6, rd.off_mec4_12_6, rd.off_mec5_12_6],

    164: [rd.off_mec0_16_4, rd.off_mec1_16_4, rd.off_mec2_16_4, rd.off_mec3_16_4],
    165: [rd.off_mec0_16_5, rd.off_mec1_16_5, rd.off_mec2_16_5, rd.off_mec3_16_5, rd.off_mec4_16_5],
    166: [rd.off_mec0_16_6, rd.off_mec1_16_6, rd.off_mec2_16_6, rd.off_mec3_16_6, rd.off_mec4_16_6, rd.off_mec5_16_6],
}


def average_timely():
    av = {}

    for i in _time:
        for j in _time[i]:
            _id = 4
            a = 0
            for t in range(3):
                _key = f'{j}_{_id}_{i}'
                av[_key] = sum(_time[i][j][a:a + 3])
                _id += 1
                a += 3

    return av


print(average_timely())
