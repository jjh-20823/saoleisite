# TODO The analyser should be editable and extensible (for auto-judge), and the dict is not a good way to transfer data
# https://docs.rs/ms_toollib/1.4.2/ms_toollib/struct.BaseVideo.html


from datetime import datetime

import ms_toollib as ms

QG_CONST = (36, 162, 435)
MODE_NAMES = ["beg", "int", "exp"]


def video_anal(file):
    temp_name = "temp/" + file.name
    with open(temp_name, "wb+") as temp_f:
        for chunk in file.chunks():
            temp_f.write(chunk)
    v = ms.AvfVideo(temp_name)
    v.parse_video()
    v.analyse()
    v.current_time = 999999
    result = {
        "software": "".join(chr(i) for i in v.software),
        "identification": "".join(chr(i) for i in v.player_designator),
        "start_time": datetime.strptime(
            "".join(chr(i) for i in v.start_time[:-5]), r"%d.%m.%Y.%H:%M:%S"
        ),  # too lazy to transfer it :)
        "mode": MODE_NAMES[v.level - 3],
        "nf": bool(v.flag > 0),
        "time": v.time,
        "bv": v.bbbv,
        "cl": v.cl,
        "ce": v.ce,
        "flags": v.flag,
    }
    result["bvs"] = result["bv"] / result["time"]
    result["qg"] = pow(result["time"], 1.7) / result["bv"]
    result["stnb"] = QG_CONST[v.level - 3] / result["qg"]
    result["ioe"] = result["bv"] / result["cl"]
    result["thrp"] = result["bv"] / result["ce"]
    result["cls"] = result["cl"] / result["time"]
    result["ces"] = result["ce"] / result["time"]
    return result
