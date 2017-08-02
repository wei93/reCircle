# views.py
import os

from django.shortcuts import render, HttpResponse

# Database
productDB = {'P1':{'pid': 'P1', 'lifespan' :12, 'components' : ['47-25459-01','471-00027-01','503-00141-01'],'costToDisassemble':6},
             'P2':{'pid': 'P2', 'lifespan' :3, 'components' : ['471-00027-01'],'costToDisassemble':2}}
componentDB = {'47-25459-01': {'hasWarranty':'true','weight': 1.5, 'materials':['metalOther','plasticPET','naturalWood'],'compPercent':[0.1,0.2,0.7]},
'471-00027-01':{'hasWarranty':'true','weight': 0.75,'materials':['naturalWood','plasticLDPE','silicon'],'compPercent':[0.30,0.40,0.30]},
'503-00141-01':{'hasWarranty': 'na', 'weight': 2,'materials': ['plasticHDPE','paperCorrugated'],'compPercent': [0.50,0.50]}}
materialDB = {'metalOther':{'recyclability':0.4,
'envt_contaminant':0.7},
'plasticPET':{'recyclability':0.8,
'envt_contaminant':0.6},
'naturalWood':{'recyclability':0.9,
'envt_contaminant':0.9},
'plasticLDPE':{'recyclability':0.5,
'envt_contaminant':0.4},
'silicon':{'recyclability':0.4,
'envt_contaminant':0.7},
'plasticHDPE':{'recyclability':0.3,
'envt_contaminant':0.3},
'paperCorrugated':{'recyclability':0.9,
'envt_contaminant':0.9}}

def profile(request):

    parsedData = []
    return render(request, 'app/profile.html', {'data': parsedData})


def productdetail(request):
    parsedData = []

    if request.method == 'POST':
        productID = request.POST.get('productid')
        recyclabilityWeight = float(request.POST.get('w1'))
        reparabilityWeight = float(request.POST.get('w2'))
        resalebilityWeight = float(request.POST.get('w3'))

        numberOfComponentsWithWarranty = 0

        numberOfComponents = 0

        numberOfComponents = len(productDB[productID]['components'])
        listOfComponents = productDB[productID]['components']

        for comp in listOfComponents:
            if componentDB[comp]['hasWarranty']=='true':
                numberOfComponentsWithWarranty+=1

        recyclabilityScore = 0

        #-------Calculate reparability based on number of components and the cost to disassemble---------

        reparabilityScore = 0

        if numberOfComponents > 10:
            subScoreNumberOfComponents = 0
        elif numberOfComponents > 5:
            subScoreNumberOfComponents = 5
        else:
            subScoreNumberOfComponents = 10

        timeToDisassemble = productDB[productID]['costToDisassemble']

        if timeToDisassemble > 10:
            subScoreCostToDisassemble = 0
        elif timeToDisassemble > 5:
            subScoreCostToDisassemble = 5
        else:
            subScoreCostToDisassemble = 10

        reparabilityScore = (float(subScoreNumberOfComponents)/10+float(subScoreCostToDisassemble)/10)/2 #out of 10


        #-------Calculate resalability based on number of components and warranty on each component and product lifepan

        lifeSpan = productDB[productID]['lifespan']

        if lifeSpan > 10:
            subScoreLifespan = 10
        elif lifeSpan >5:
            subScoreLifespan = 5
        else:
            subScoreLifespan = 0

        resalabilityScore = ((float(numberOfComponentsWithWarranty)/numberOfComponents)*10 + subScoreLifespan )/2 #out of 10

        #-------Calculate recyclability based on materials used in each component

        totWeight=0
        for comp in listOfComponents:
            totWeight+=componentDB[comp]['weight']

        for comp in listOfComponents:
            listOfMaterials = componentDB[comp]['materials']
            listOfMaterialsPercent = componentDB[comp]['compPercent']
            i=0
            subScoreMat=[]
            for mat in listOfMaterials:
                subScoreMat = listOfMaterialsPercent[i]*((0.5*materialDB[mat]['recyclability'])+(0.5*materialDB[mat]['envt_contaminant']))
                i+=1
                recyclabilityScore += (float(componentDB[comp]['weight'])/totWeight)*subScoreMat

        score1 = recyclabilityWeight*recyclabilityScore
        score2 = resalebilityWeight*resalabilityScore
        score3 = reparabilityWeight*reparabilityScore*10
        totalScore = (recyclabilityWeight*recyclabilityScore + resalebilityWeight*resalabilityScore + reparabilityWeight*reparabilityScore*10)/3

        productDB[productID]['s1'] = score1
        productDB[productID]['s2'] = score2
        productDB[productID]['s3'] = score3
        productDB[productID]['score'] = totalScore
        parsedData.append(productDB[productID])

    return render(request, 'app/ProductDetail.html', {'data': parsedData})


def download_pdf(request):
    filename = 'C:/Users/emgao/Desktop/RecyclabilityAnalysis.pdf'
    file = open('C:/Users/emgao/Desktop/RecyclabilityAnalysis.pdf', 'rb')
    response = HttpResponse(file.read(), content_type="application/pdf")
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' % 'report.pdf'
    return response

