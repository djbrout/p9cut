import numpy as np
import dilltools as dt
import os
from copy import copy

workingdir = '/scratch1/scratchdirs/dbrout/p9/results6skysigplusmod/'
os.system('cat '+workingdir+'detections_i_* > '+workingdir+'detections_i_all.txt')

data = dt.readcol(workingdir+'detections_i_all.txt',delim=',')

print data.keys()

import matplotlib as m
m.use('Agg')
import matplotlib.pyplot as plt

tot = len(data['sn'])
train = int(round(tot*.99))
print 'tot',tot,'train',train
sn = data['sn'][:train]
chsq1 = data['search_1fwhm_chisq'][:train]
chsq2 = data['search_2fwhm_chisq'][:train]
chsq3 = data['search_3fwhm_chisq'][:train]
tcs = data['templ_chi'][:train]
diffmag = data['mag'][:train]
fitmag = data['sm_mag'][:train]

snt = data['sn'][train:]
chsq1t = data['search_1fwhm_chisq'][train:]
chsq2t = data['search_2fwhm_chisq'][train:]
chsq3t = data['search_3fwhm_chisq'][train:]
tcst = data['templ_chi'][train:]
diffmagt = data['mag'][train:]
fitmagt = data['sm_mag'][train:]

#print sn[diffmag==20]
#print tcs.shape
#print chsq1.shape
#raw_input()

snlim = 4.




nreal = len(diffmag[(diffmag>0) & (diffmag != 20.00) & (sn > snlim)])
nbad = len(diffmag[(diffmag==0)& (sn > snlim)])
ntot = len(diffmag[(sn > snlim)])

wreal = (diffmag > 0) & (chsq3 < 1000) & (chsq3 >= 0.) & (diffmag != 20.00)#& (sn > snlim)
wfake = (diffmag == 0) & (chsq3 < 1000) & (chsq3 >= 0.)#& (sn > snlim)

wrealt = (diffmagt > 0) & (chsq3t < 1000) & (chsq3t >= 0.) & (diffmagt != 20.00)#& (sn > snlim)
wfaket = (diffmagt == 0) & (chsq3t < 1000) & (chsq3t >= 0.)#& (sn > snlim)

ll = .8
ul = 1.5
s=.26

plt.scatter(sn[wfake],chsq2[wfake],color='red',alpha=.5)
plt.scatter(sn[wreal],chsq2[wreal],color='green',alpha=.9,label='Train')
plt.scatter(snt[wfaket],chsq2t[wfaket],color='red',alpha=.5,marker='+')
plt.scatter(snt[wrealt],chsq2t[wrealt],color='green',alpha=.9,marker='+',label='Test')
plt.axhline(ll,color='black',linestyle='--')
plt.plot([0,10,500],[ul,ul,500*s + ul],color='black',linestyle='--')
#plt.axhline(ul,color='black',linestyle='--')
plt.xlim(4.,150.)
plt.ylim(0,20.)
plt.ylabel('2 FWHM Chi Squared')
plt.xlabel('S/N')
plt.legend()
plt.savefig(workingdir+'results_chi2.png')
print 'saved '+workingdir+'results_chi2.png'

plt.clf()
plt.scatter(sn[wfake],chsq1[wfake],color='red',alpha=.5)
plt.scatter(sn[wreal],chsq1[wreal],color='green',alpha=.9)
plt.axhline(ll,color='black',linestyle='--')
plt.plot([0,10,500],[ul,ul,500*s + ul],color='black',linestyle='--')
#plt.axhline(ul,color='black',linestyle='--')
plt.xlim(4.,150.)
plt.ylim(0,20.)
plt.ylabel('2 FWHM Chi Squared')
plt.xlabel('S/N')
plt.savefig(workingdir+'results_chi1.png')
print 'saved '+workingdir+'results_chi1.png'

plt.clf()
plt.scatter(sn[wfake],chsq3[wfake],color='red',alpha=.5)
plt.scatter(sn[wreal],chsq3[wreal],color='green',alpha=.9)
plt.axhline(ll,color='black',linestyle='--')
plt.plot([0,10,500],[ul,ul,500*s + ul],color='black',linestyle='--')
#plt.axhline(ul,color='black',linestyle='--')
plt.xlim(4.,150.)
plt.ylim(0,20.)
plt.ylabel('2 FWHM Chi Squared')
plt.xlabel('S/N')
plt.savefig(workingdir+'results_chi3.png')
print 'saved '+workingdir+'results_chi3.png'

plt.clf()
plt.hist([chsq2[wfake]-chsq1[wfake],chsq2[wreal]-chsq1[wreal]],color=['red','green'],bins=np.arange(-3.5,2,.2),normed=True)
plt.axvline(-.26,color='black',linestyle='--')
plt.xlim(-3.5,2.)
plt.xlabel('Chisq 2FWHM - 1FWHM')
plt.savefig(workingdir+'resultshist.png')
print 'saved '+workingdir+'resultshist.png'
plt.clf()
plt.hist([chsq3[wfake]-chsq1[wfake],chsq3[wreal]-chsq1[wreal]],color=['red','green'],bins=np.arange(-4.5,2,.2),normed=True)
plt.axvline(-.26,color='black',linestyle='--')
plt.xlim(-3.5,2.)
plt.xlabel('Chisq 3FWHM - 1FWHM')
plt.savefig(workingdir+'resultshist32.png')
print 'saved '+workingdir+'resultshist32.png'

plt.clf()
plt.scatter(fitmag[wfake],chsq1[wfake],color='red',alpha=.5)
plt.scatter(fitmag[wreal],chsq1[wreal],color='green',alpha=.9)
plt.axhline(.87,color='black',linestyle='--')
plt.axhline(1.37,color='black',linestyle='--')
plt.xlim(19.0,25.5)
plt.ylim(0,20.)
plt.ylabel('2 FWHM Chi Squared')
plt.xlabel('FitMag')
plt.savefig(workingdir+'resultsvsmag.png')
print 'saved '+workingdir+'resultsvsmag.png'
import sys
#sys.exit()
maxpe = 0
ulc = 0
llc = 0
uld = 0
ps = 0
maxp = 0
maxe = 0
snsplit = 10.
for i in np.arange(0.79,.81,.01):
    for j in np.arange(.5,1.,.01):
        for k in np.arange(-.9,-.7,.1):
            for s in np.arange(0.12,.3,.001)[::-1]:
                #if True:
                #s = 0.
                upperlimchi = i+j
                lowerlimchi = i
                upperlimdiff = k

                wwreal = (chsq3 > lowerlimchi) & (chsq3 < upperlimchi) & (diffmag > 0) & (diffmag != 20.00) & (sn > snlim) & (sn < snsplit)
                wwreal2 = (chsq3 > lowerlimchi) & (chsq3 < (s*sn)+upperlimchi) & (diffmag > 0) & (diffmag != 20.00) & (sn > snlim) & (sn > snsplit)
                print len(diffmag[wwreal]),len(diffmag[wwreal2]),len(diffmag[np.logical_or(wwreal,wwreal2)]),
                wwreal3 = (chsq3-chsq1 < upperlimdiff) & (diffmag > 0) & (diffmag != 20.00) & (sn > snlim)

                wwbad = (chsq3 > lowerlimchi) & (chsq3 < upperlimchi) & (diffmag == 0) & (sn > snlim)  & (sn < snsplit)
                wwbad2 = (chsq3 > lowerlimchi) & (chsq3 < (s*sn)+upperlimchi) & (diffmag == 0) & (sn > snlim) & (sn > snsplit)
                wwbad3 = (chsq3-chsq1 < upperlimdiff) & (diffmag == 0) & (sn > snlim)

                p = 1 - float(len(diffmag[np.logical_or(wwbad3, np.logical_or(wwbad,
                        wwbad2))]))/float(len(diffmag[np.logical_or(wwbad3,
                        np.logical_or(wwreal3,np.logical_or(np.logical_or(np.logical_or(wwreal,
                        wwreal2),wwbad),wwbad2)))]))
                e = float(len(diffmag[np.logical_or(wwreal3,np.logical_or(wwreal, wwreal2))]))/float(nreal)
                if p+e > maxpe:
                    ulc = upperlimchi
                    llc = lowerlimchi
                    uld = upperlimdiff
                    ps = copy(s)
                    maxp = p
                    maxe = e
                    maxpe = p+e
                #if p+e > 1.909:
                print 'upperlimchi',upperlimchi,'lowerlimchi',lowerlimchi,'upperlimdiff',upperlimdiff,'slope',s,'Purity',round(p,3),'Eff',round(e,3)
                #raw_input()


print '-'*50
print '-'*50
print 'upperlimchi', ulc, 'lowerlimchi', llc, 'upperlimdiff', uld, 'Purity', round(maxp,4),'Slope',ps, 'Eff', round(maxe, 4)
print '-'*50
print '-'*50


upperlimchi = ulc
lowerlimchi = llc
upperlimdiff = uld
s = copy(ps)

# # sn = data['sn'][train:]
# # chsq1 = data['search_1fwhm_chisq'][train:]
# # chsq2 = data['search_2fwhm_chisq'][train:]
# # chsq3 = data['search_3fwhm_chisq'][train:]
# # tcs = data['templ_chi'][train:]
# # diffmag = data['mag'][train:]
#
# nreal = len(diffmag[(diffmag>0) & (diffmag != 20.00) & (sn > snlim)])
# nbad = len(diffmag[(diffmag==0)& (sn > snlim)])
# ntot = len(diffmag[(sn > snlim)])

wwreal = (chsq3 > lowerlimchi) & (chsq3 < upperlimchi) & (diffmag > 0) & (diffmag != 20.00) & (sn > snlim) & (sn < snsplit)
wwreal2 = (chsq3 > lowerlimchi) & (chsq3 < (s*sn)+upperlimchi) & (diffmag > 0) & (diffmag != 20.00) & (sn > snlim) & (sn > snsplit)
wwreal3 = (chsq3-chsq1 < upperlimdiff) & (diffmag > 0) & (diffmag != 20.00) & (sn > snlim)

wwbad = (chsq3 > lowerlimchi) & (chsq3 < upperlimchi) & (diffmag == 0) & (sn > snlim)  & (sn < snsplit)
wwbad2 = (chsq3 > lowerlimchi) & (chsq3 < (s*sn)+upperlimchi) & (diffmag == 0) & (sn > snlim) & (sn > snsplit)
wwbad3 = (chsq3-chsq1 < upperlimdiff) & (diffmag == 0) & (sn > snlim)

p = 1 - float(len(diffmag[np.logical_or(wwbad3, np.logical_or(wwbad,
                        wwbad2))]))/float(len(diffmag[np.logical_or(wwbad3,
                        np.logical_or(wwreal3,np.logical_or(np.logical_or(np.logical_or(wwreal,
                        wwreal2),wwbad),wwbad2)))]))
e = float(len(diffmag[np.logical_or(wwreal3,np.logical_or(wwreal, wwreal2))]))/float(nreal)
print '*'*50
print '*'*50
print 'upperlimchi',upperlimchi,'lowerlimchi',lowerlimchi,'upperlimdiff',upperlimdiff,'slope',ps,'Purity',round(p,3),'Eff',round(e,3)
print ''
print 'total',ntot
print 'contamination',len(diffmag[np.logical_or(wwbad3, np.logical_or(wwbad,wwbad2))])
print ''
print 'total good',nreal
print 'fit good',len(diffmag[np.logical_or(wwreal3,np.logical_or(wwreal, wwreal2))])

print ''
print 'total bad',nbad
print 'eliminated',nbad-len(diffmag[np.logical_or(wwbad3,np.logical_or(wwbad, wwbad2))])
print '*'*50
print '*'*50


inn = open(workingdir+'detections_i_all.txt','r').readlines()
out = open(workingdir+'predictions_i.txt','w')


for i,line in enumerate(inn):
    print i,line
    print i,line[-2]
    raw_input()
    #out.write('')