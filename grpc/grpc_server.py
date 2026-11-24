from concurrent import futures

import grpc

import calculator_pb2
import calculator_pb2_grpc


class Calculator(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        return calculator_pb2.AddReply(result=request.a + request.b)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
calculator_pb2_grpc.add_CalculatorServicer_to_server(Calculator(), server)
server.add_insecure_port("[::]:50051")
server.start()
print("Serveur gRPC en écoute sur le port 50051")
server.wait_for_termination()
