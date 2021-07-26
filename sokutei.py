def write(name,naiyou,net):
    with open('./'+name+'('+net+').sp','w') as f:
        f.write(naiyou)
    print(name,".sp　というファイルを生成しました。")

def line():
    print("=======================================================")

def toikake():
    print("まだ、.spファイルを生成しますか？")
    print("yes:1 , no:0")

def sp1():
    print("測定するOPアンプのネットリストの名前をを入力してください")
    net1 = input()
    name="Slewrate"
    naiyou=("Slewrate simulation\n\n"
            ".options post\n"
            ".INCLUDE \"tsmc018.mdl\"  $ include your model parameter here\n"
            ".INCLUDE \""+net1+".net\"        $ include your opamp netlist here\n\n"
            "VDD	vdd 0	'half'\n"
            "VSS	0 vss	'half'\n\n" 
            "* For rise edge slewrate\n"
            "X1a     s1 in1 out1 vdd vss     opamp\n"
            "R1a     s1 0                    valr1\n"
            "R2a     out1 s1                 valr2\n\n" 
            "* For fall edge slewrate\n"
            "X1b     s2 in2 out2 vdd vss     opamp\n"
            "R1b     s2 0                    valr1\n"
            "R2b     out2 s2                 valr2\n\n" 
            "* Offset voltage\n"
            "X1c     ss 0 os vdd vss         opamp\n"
            "R1c     ss 0                    valr1\n"
            "R2c     os ss                   valr2\n\n\n" 
            "VIN1    in1 0                   PULSE '-vp' 'vp' td tr tf pw1 pp1\n"
            "VIN2    in2 0                   PULSE 'vp' '-vp' td tr tf pw1 pp1\n\n" 
            ".PARAM half='psvoltage/2' valr1=10k valr2=10k grad=1e11\n"
            "+ vp=             $ pulse amplitude\n"
            "+ td=100n         $ pulse delay\n"
            "+ tr='vp/grad'    $ pulse transition time\n"
            "+ tf='vp/grad'\n"
            "+ pw1=300u        $ pulse width\n"
            "+ pp1=400u        $ pulse period\n"
            ".TRAN 10p 200u\n"
            ".MEAS TRAN vps  FIND  V(out1,os) AT=0\n"
            ".MEAS TRAN vpt  FIND  V(out1,os) AT=200u\n"
            ".MEAS TRAN vns  FIND  V(out2,os) AT=0\n"
            ".MEAS TRAN vnt  FIND  V(out2,os) AT=200u\n"
            ".MEAS TRAN srr1 DERIV V(out1,os) WHEN V(out1,os)='0.9*vps'\n"
            ".MEAS TRAN srr2 DERIV V(out1,os) WHEN V(out1,os)=0\n"
            ".MEAS TRAN srr3 DERIV V(out1,os) WHEN V(out1,os)='0.9*vpt'\n"
            ".MEAS TRAN srr  PARAM='(srr1+srr2+srr3)/3'\n"
            ".MEAS TRAN srf1 DERIV V(out2,os) WHEN V(out2,os)='0.9*vns'\n"
            ".MEAS TRAN srf2 DERIV V(out2,os) WHEN V(out2,os)=0\n"
            ".MEAS TRAN srf3 DERIV V(out2,os) WHEN V(out2,os)='0.9*vnt'\n"
            ".MEAS TRAN srf  PARAM='(srf1+srf2+srf3)/3'\n"
            ".MEAS TRAN sr   PARAM='min(abs(srr),abs(srf))'\n"
            ".END\n")
    write(name, naiyou,net1)

def sp2():
    print("2.出力抵抗の.spファイルを生成します。")
    line()
    print("測定するOPアンプのネットリストの名前をを入力してください")
    net2 = input()
    name="OutputResistance"
    naiyou=("Simulation for output resistance\n"
            ".options post\n"
            ".INCLUDE \"tsmc018.mdl\" $ include your model parameter here\n"
            ".INCLUDE \""+net2+".net\" $ include your opamp netlist here\n\n"
            "VIN inp 0 dc 0\n"
            "VDD vdd 0 'half'\n"
            "VSS 0 vss 'half'\n\n"
            "X1 s inp out vdd vss opamp\n"
            "R1 s 0 valr1\n"
            "R2 out s valr2\n\n"
            ".op\n"
            ".PARAM half='psvoltage/2' valr1=10k valr2=10k\n"
            ".TF V(out) VIN\n"
            ".END\n")
    write(name, naiyou,net2)

def sp3():
    print("3.出力電圧範囲の.spファイルを生成します。")
    line()
    print("測定するOPアンプのネットリストの名前をを入力してください")
    net3 = input()
    name="OutVoltRange"
    naiyou=("Output voltage range simulation\n\n"
            ".options post\n"
            ".INCLUDE \"tsmc018.mdl\"  $ include your model parameter here\n"
            ".INCLUDE \""+net3+".net\"        $ include your opamp netlist here\n\n"
            "VIN     in1 0   dc 0\n"
            "E1      0 in2 in1 0             1\n"
            "VDD     vdd 0   'half'\n"
            "VSS     0 vss   'half'\n\n\n"
            "* Positive side\n"
            "X1a     inm1 0 out1 vdd vss     opamp\n"
            "R1a     in1 inm1                rload\n"
            "R2a     inm1 out1               rload\n\n"
            "* Negative side\n"
            "X1b     inm2 0 out2 vdd vss     opamp\n"
            "R1b     in2 inm2                rload\n"
            "R2b     inm2 out2               rload\n\n"
            "* offset voltage\n"
            "X1c     inm3 0 os vdd vss       opamp\n"
            "2R1c     0 inm3                  rload\n"
            "2R2c     inm3 os                 rload\n\n"
            ".PARAM half='psvoltage/2' rload=20k\n"
            ".DC VIN 10m half '(half-10m)/100'\n"
            ".PRINT V(out1,os) V(out2,os)\n"
            "2+ PAR'1-ABS(V(out1,os))/V(in1)' PAR'1-ABS(V(out2,os))/V(in1)'\n\n"
            ".END\n\n")
    write(name, naiyou,net3)

def sp4():
    print("4.消費電力、消費電流の.spファイルを生成します。")
    line()
    print("測定するOPアンプのネットリストの名前をを入力してください")
    net4 = input()
    name="DCSimulationForBiasCurrent&PowerDissipation"
    naiyou=("DC simulation for bias current and power dissipation\n\n"
            ".options post\n"
            ".INCLUDE \"tsmc018.mdl\" $ include your model parameter here\n"
            ".INCLUDE \""+net4+".net\" $ include your opamp netlist here\n\n"
            "VIN inp 0 dc 0\n"
            "VDD vdd 0 'step'\n"
            "VSS 0 vss 'step'\n\n"
            "X1 s inp out vdd vss opamp\n"
            "R1 s 0 valr1\n"
            "R2 out s valr2\n\n"
            ".op\n"
            ".PARAM half='psvoltage/2' valr1=10k valr2=10k\n"
            ".DC VIN -0.01 0.01 0.01 SWEEP step POI 3 '0.9*half' 'half' '1.1*half'\n"
            ".TEMP -40 25 80\n"
            ".MEAS DC ivdd FIND I(VDD) AT=0\n"
            ".MEAS DC ivss FIND I(VSS) AT=0\n"
            ".MEAS DC ib PARAM='max(abs(ivdd),abs(ivss))'\n"
            ".MEAS DC pdis PARAM='ib*2*step'\n"
            ".EN\n\n")
    write(name, naiyou,net4)

def sp5():
    print("5.全高調波歪の.spファイルを生成します。")
    line()
    print("測定するOPアンプのネットリストの名前をを入力してください")
    net5 = input()
    name="THD"
    naiyou=("Simulation for THD\n\n"
            ".options post \n"
            ".INCLUDE \"tsmc018.mdl\"  $ include your model parameter here\n"
            ".INCLUDE \""+net5+".net\"        $ include your opamp netlist here\n\n"
            "VIN	inp 0 	SIN 0 2.5m 100 1m\n"
            "VDD	vdd 0	PULSE 0 half 0 0.1n 0.1n 1.5015 2.002\n"
            "VSS	0 vss	PULSE 0 half 0 0.1n 0.1n 1.5015 2.002\n\n"
            "X1	s inp out vdd vss	opamp\n"
            "R1	s 0			valr1\n"
            "R2	out s			valr2\n\n"
            ".PARAM half='psvoltage/2' valr1=10k valr2=10k\n"
            ".TRAN 10n 1.001 START='1.001-10m'\n"
            ".FOUR 100 V(out)\n"
            ".END\n\n")
    write(name, naiyou,net5)

def sp6():
    print("6.直流利得、位相余裕、利得帯域幅の.spファイルを生成します。")
    line()
    print("測定するOPアンプのネットリストの名前をを入力してください")
    net6 = input()
    name="DCGain&PhaseMargin&Bandwidth"
    naiyou=("Simulation for DC gain, phase margin and gain bandwidth product \n\n"
            ".options post\n"
            ".INCLUDE \"tsmc018.mdl\" $ include your model parameter here\n"
            ".INCLUDE \""+net6+".net\" $ include your opamp netlist here\n\n"
            "VIN inp 0 dc 0 ac 1\n"
            "VDD vdd 0 'half'\n"
            "VSS 0 vss 'half'\n\n"
            "X1 s inp out vdd vss opamp\n"
            "RL out 0 valrl\n"
            "RF out s valrf\n"
            "CF s 0 valcf\n\n"
            ".op\n"
            ".PARAM half='psvoltage/2' valrl=20k valrf=1T valcf=1m\n"
            ".AC DEC 100 0.1 10G\n"
            ".PRINT VDB(out) VP(out)\n"
            ".MEAS AC dcgain FIND VDB(out) AT=0.1\n"
            ".END\n\n")
    write(name, naiyou,net6)

def sp7():
    print("7.電源電圧変動除去比の.spファイルを生成します。")
    line()
    print("測定するOPアンプのネットリストの名前をを入力してください")
    net7 = input()
    name="PSRR"
    naiyou=("PSRR simulation\n\n"
            ".options post \n"
            ".INCLUDE \"tsmc018.mdl\"  $ include your model parameter here\n"
            ".INCLUDE \""+net7+".net\"        $ include your opamp netlist here\n\n"
            "VIN     in 0    	dc 0 ac 1\n"
            "VDD	vdd 0		half\n"
            "VDD1	vdd vdd1	dc 0 ac 1\n"
            "VSS	0 vss		half\n"
            "VSS1	vss2 vss	dc 0 ac 1\n\n"
            "* For differential gain\n"
            "X1      s in od vdd vss opamp\n"
            "R1      od s                    valrf\n"
            "C1      s 0                     valcf\n"
            "R2      od 0                    valrl\n\n"
            "* For VDD\n"
            "X1a     s1 0 odd vdd1 vss       opamp\n"
            "R1a     odd s1                  valrf\n"
            "C1a	s1 0	                valcf\n"
            "R2a     odd 0                   valrl\n\n"
            "* For VSS\n"
            "X1b     s2 0 oss vdd vss2       opamp\n"
            "R1b     oss s2                  valrf\n"
            "C1b	s2 0			valcf\n"
            "R2b     oss 0                   valrl\n\n"
            ".PARAM half='psvoltage/2' valrl=20k valrf=1T valcf=1m\n"
            "+ valr1=10k valr2=10k\n"
            ".AC DEC 100 0.1 10G\n"
            ".MEAS AC pd   FIND VDB(od,odd) AT=0.1\n"
            ".MEAS AC ps   FIND VDB(od,oss) AT=0.1\n"
            ".MEAS AC psrr PARAM='min(pd,ps)' AT=0.1\n"
            ".END\n\n")
    write(name, naiyou,net7)

def sp8():
    print("7.電源電圧変動除去比の.spファイルを生成します。")
    line()
    print("測定するOPアンプのネットリストの名前をを入力してください")
    net8 = input()
    name="CMRR"
    naiyou=("CMRR simulation\n\n"
            ".options post\n"
            ".INCLUDE \"tsmc018.mdl\"  $ include your model parameter here\n"
            ".INCLUDE \""+net8+".net\"        $ include your opamp netlist here\n\n"
            "VIN     in 0    dc 0 ac 1\n"
            "VDD	vdd 0	half\n"
            "VSS	0 vss	half\n\n"
            "X1      s1 in oc vdd vss        opamp\n"
            "R11     oc s1           valrf\n"
            "C11     s1 in           valcf\n"
            "R21     oc 0            valrl\n\n"
            "X2      s2 in od vdd vss        opamp\n"
            "R12     od s2           valrf\n"
            "C12     s2 0            valcf\n"
            "R22     od 0            valrl\n\n"
            ".PARAM half='psvoltage/2' valrl=20k valrf=1T valcf=1m\n"
            ".AC DEC 100 0.1 10G\n"
            ".MEAS AC cmrr MAX VDB(od,oc) FROM=0.1 TO=10G\n"
            ".END\n\n")
    write(name, naiyou,net8)

def sp9():
    print("9.同相入力範囲の.spファイルを生成します。")
    line()
    print("測定するOPアンプのネットリストの名前をを入力してください")
    net9 = input()
    name="CommonModeRange.sp"
    naiyou=("Common mode range simulation\n\n"
            ".options post \n"
            ".INCLUDE \"tsmc018.mdl\"  $ include your model parameter here\n"
            ".INCLUDE \""+net9+".net\"        $ include your opamp netlist here\n\n"
            "VIN     in1 0   dc 0\n"
            "E1      0 in2 in1 0      \n"
            "VDD     vdd 0   'half'\n"
            "VSS     0 vss   'half'\n\n\n"
            "* Positive side\n"
            "X1a     inm1 inp1 outx1 vdd vss opamp\n"
            "R1a     in1 inp1                'rload/2'\n"
            "R2a     inp1 0                  'rload/2'\n"
            "R3a     in1 inm1                'rload/2'\n"
            "R4a     inm1 out1               rload\n"
            "E1a     out1 0 outx1 0          bgain\n"
            "R5a     outx1 0                 rload\n\n"
            "* Negative side\n"
            "X1b     inm2 inp2 outx2 vdd vss opamp\n"
            "R1b     in2 inp2                'rload/2'\n"
            "R2b     inp2 0                  'rload/2'\n"
            "R3b     in2 inm2                'rload/2'\n"
            "R4b     inm2 out2               rload\n"
            "E1b     out2 0 outx2 0          bgain\n"
            "R5b     outx2 0                 rload\n\n"
            "* offset voltage\n"
            "X2      inm3 0 osx vdd vss      opamp\n"
            "R12     0 inm3                  'rload/2'\n"
            "R22     inm3 os                 rload\n"
            "E2      os 0 osx 0              bgain\n"
            "R32     osx 0                   rload\n\n"
            ".PARAM half='psvoltage/2' rload=20k bgain=10\n"
            ".DC VIN 10m psvoltage '(psvoltage-10m)/100'\n"
            ".PRINT V(out1,os) V(out2,os)\n"
            "+ PAR'1-ABS(V(out1,os))/(0.5*V(in1))' PAR'1-ABS(V(out2,os))/(0.5*V(in1))'\n\n"
            ".END\n\n")
    write(name,naiyou,net9)

def sp10():
    print("10.入力換算雑音の.spファイルを生成します。")
    line()
    print("測定するOPアンプのネットリストの名前をを入力してください")
    net10 = input()
    name="InputReferedNoise"
    naiyou=("Input refered noise simulation\n\n"
            ".options post\n"
            ".INCLUDE \"tsmc018.mdl\"  $ include your model parameter here\n"
            ".INCLUDE \""+net10+".net\"        $ include your opamp netlist here\n\n"
            "VIN	inp 0 	dc 0\n"
            "VDD	vdd 0	'half'\n"
            "VSS	0 vss	'half'\n\n"
            "X1      s inp out vdd vss       opamp\n"
            "R1      s 0                     nores valr1\n"
            "R2      out s                   nores valr2\n\n"
            ".MODEL nores R noise=0\n"
            ".PARAM half='psvoltage/2' valr1=10k valr2=10k\n"
            ".AC DEC 100 0.1 1MEG\n"
            ".NOISE V(out) VIN 10\n"
            ".END\n\n")
    write(name,naiyou,net10)

line()
print("このツールはオペアンプの性能評価の.spファイルを生成するツールです。")
line()

i=1
while i==1:
    print("対応する番号を入力してください。\n"
        "1.スルーレート\n"
        "2.出力抵抗\n"
        "3.出力電圧範囲\n"
        "4.消費電力、消費電流\n"
        "5.全高調波歪\n"
        "6.直流利得、位相余裕、利得帯域幅\n"
        "7.電源電圧変動除去比\n"
        "8.同相除去\n"
        "9.同相入力範囲\n"
        "10.入力換算雑音\n")
    x=int(input())

    line()
    if x==1:
        sp1()
        line()
        toikake()
        i = int(input())
        line()
    elif x==2:
        sp2()
        line()
        toikake()
        i = int(input())
        line()
    elif x==3:
        sp3()
        line()
        toikake()
        i = int(input())
        line()
    elif x==4:
        sp4()
        line()
        toikake()
        i = int(input())
        line()
    elif x==5:
        sp5()
        line()
        toikake()
        i = int(input())
        line()
    elif x==6:
        sp6()
        line()
        toikake()
        i = int(input())
        line()
    elif x==7:
        sp7()
        line()
        toikake()
        i = int(input())
        line()
    elif x==8:
        sp8()
        line()
        toikake()
        i = int(input())
        line()
    elif x==9:
        sp9()
        line()
        toikake()
        i = int(input())
        line()
    elif x==10:
        sp10()
        line()
        toikake()
        i = int(input())
        line()
    else:
        print("対応する番号意外が入力されたため")
        toikake()
        i = int(input())
        line()

exit=0
while exit==0:
    print("終了したい場合は何かキーを押してください。")
    exit = input()
