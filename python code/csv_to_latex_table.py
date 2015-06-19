import sys,os


def table_from_csv(out_file,csv_file,caption="Caption"):
    with open(out_file,"w") as pout:
        with open(csv_file,"r") as pin:
            flag = True
            
            for line in pin:
                s_line = line.split(",")
                
                if flag:
                    flag = False
                    pout.write("\\begin{table}[!ht]\n\\begin{adjustwidth}{-2.25in}{0in}\n")
                    pout.write("\\caption{{\\bf "+caption+"}}\n")
                    pout.write("\\begin{tabular}{|"+"".join(["l|" for item in s_line])+"}\n\hline\n")
                    
                    pout.write("&".join(["{\\bf "+item.replace("\n","").replace("#","\\#")+"}" for item in s_line])+"\\\\ \\hline\n")
                    continue
                temp = []
                for item in s_line:
                    try:
                        item = str(int(item))
                    except:
                        try:
                            item = "%.3f" % float(item)
                        except:
                            pass
                    temp.append(item)        
                pout.write("&".join(["{"+" "+item+"}" for item in temp])+"\\\\ \\hline\n")
                
            pout.write("\\end{tabular}\n\\end{adjustwidth}\n\\end{table}\n")
     


def main():
    table_from_csv("table.txt","""..\\results\\only participants\\graph_stats\\wan_metrics_single_graph.csv""")

if __name__ == "__main__":
    main()
