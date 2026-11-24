import grpc

import calculator_pb2
import calculator_pb2_grpc

with grpc.insecure_channel("localhost:50051") as channel:
    stub = calculator_pb2_grpc.CalculatorStub(channel)
    requete = calculator_pb2.AddRequest(a=5, b=7)
    reponse = stub.Add(requete)

print("Résultat :", reponse.result)
print("Requête sérialisée :", len(requete.SerializeToString()), "octets ->", requete.SerializeToString().hex(" "))
print("Réponse sérialisée :", len(reponse.SerializeToString()), "octets ->", reponse.SerializeToString().hex(" "))
