import openpyxl
from statsCollection import  *
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("summaryfile", help="name of summary file")
args = parser.parse_args()

def write_to_excel(data, output_file):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Write the header row using the keys of the first dictionary in the list
    header = list(data[0].keys())
    worksheet.append(header)

    # Write the data rows
    for row_data in data:
        row = []
        for key in header:
            if key in row_data:
                row.append(row_data[key])
            else:
                row.append('')
        worksheet.append(row)

    # Save the workbook
    workbook.save(output_file)
    
def readStats(benchmarksList,bpredid,ls,gs,cs,dictList):
    currentdir = "/home/010/j/jx/jxp220032/CS6304P2"
    for bm in benchmarksList:
        statsdir = currentdir + "/simstats/"+getStatsFileName(bm,bpredid,ls,gs,cs)
        statsdict = read_file_to_dict(statsdir+"/stats.txt")
        statsdict['LSize'] = ls
        statsdict['GSize'] = gs
        statsdict['CSize'] = cs
        statsdict['Benchmark']=bm
        if bpredid == 0 :
            statsdict['BranchPredictor'] = 'Local Predictor'
            statsdict['BpredID'] = 0
        if bpredid == 1 :
            statsdict['BranchPredictor'] = 'BiModal Predictor'
            statsdict['BpredID'] = 1
        if bpredid == 2 :
            statsdict['BranchPredictor'] = 'Tournament Predictor'
            statsdict['BpredID'] = 2
        dictList.append(statsdict)

def summarizeAllStats():
    currentdir = "/home/010/j/jx/jxp220032/CS6304P2"
    benchmarksList  = ['401.bzip2','429.mcf','456.hmmer','458.sjeng','470.lbm']
    dictList = []
    #local predictor
    for ls in [1024,2048,4096]:
        readStats(benchmarksList,0,ls,1024,1024,dictList)
    #biModal
    for gs in [1024,2048,4096]:
        for cs in [1024,2048,4096]:
            readStats(benchmarksList,1,1024,gs,cs,dictList)
    #tournament
    for gs in [1024,2048,4096]:
        for cs in [1024,2048,4096]:
            for ls in [1024,2048,4096]:
                readStats(benchmarksList,2,ls,gs,cs,dictList)

    write_to_excel(dictList,currentdir+"/"+args.summaryfile+".xlsx")
    print("writing summary at :"+currentdir+"/"+args.summaryfile+".xlsx")
summarizeAllStats()