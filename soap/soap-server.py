"""
    Pas de sweep.move dans python 3.12
    on peut faire le serveur à la main
    et c'est pas mal comme ça on pourra comparer avec REST et voir combien SOAP est lourd et compliqué à mettre en place.
"""

# Généré par Claude
from fastapi import FastAPI, Request, Response

app = FastAPI()

WSDL = open("calculator.wsdl").read() # Faudra le faire, ça va planter au début

@app.get("/soap")
def wsdl(wsdl: str = None):
    return Response(content=WSDL, media_type="text/xml")

@app.post("/soap")
async def soap(request: Request):
    body = (await request.body()).decode()
    # extraction naïve des deux opérandes
    a = int(body.split("<a>")[1].split("</a>")[0])
    b = int(body.split("<b>")[1].split("</b>")[0])
    envelope = f"""<?xml version="1.0"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body>
    <AddResponse xmlns="http://calculator.example/">
      <result>{a + b}</result>
    </AddResponse>
  </soapenv:Body>
</soapenv:Envelope>"""
    return Response(content=envelope, media_type="text/xml")