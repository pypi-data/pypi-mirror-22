from . import tplot_common

def tplot_names():
    index = 0
    for key, _ in tplot_common.data_quants.items():
        if isinstance(tplot_common.data_quants[key].data, list):
            if isinstance(key, str):
                names_to_print = tplot_common.data_quants[key].name + "  data from: "
                for name in tplot_common.data_quants[key].data:
                    names_to_print = names_to_print + " " + name
                print(index, ":", names_to_print)
                index+=1
        else:
            if isinstance(key, str):
                names_to_print = tplot_common.data_quants[key].name
                print(index, ":", names_to_print)
                index+=1
    return