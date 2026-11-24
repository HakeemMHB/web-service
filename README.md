# SOAP, REST, GraphQL et gRPC : la même addition, quatre technologies

Projet SYIW23 (ENSIIE). La même opération, l'addition 5 + 7, est exposée avec SOAP/WSDL, REST, GraphQL et gRPC, pour comparer les quatre approches sur une fonctionnalité identique.

| Dossier | Technologie | Port |
|---|---|---|
| `soap/` | SOAP / WSDL (FastAPI, WSDL écrit à la main) | 8000 |
| `rest/` | REST (FastAPI) | 8001 |
| `graphql/` | GraphQL (Strawberry + FastAPI) | 8002 |
| `grpc/` | gRPC (grpcio, Protocol Buffers) | 50051 |

## Installation

Prérequis : Python 3.10 ou plus récent.

```bash
git clone https://github.com/HakeemMHB/web-service.git
cd web-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Dans chaque nouveau terminal, réactiver l'environnement avec `source venv/bin/activate`.

Chaque démonstration utilise deux terminaux : un pour le serveur et un pour les appels.

---

## 1. SOAP / WSDL

**Terminal 1 (serveur)** :

```bash
cd soap
uvicorn soap-server:app --port 8000
```

Le serveur doit être lancé depuis le dossier `soap/`, car il lit `calculator.wsdl` dans le dossier courant.

**Voir le contrat WSDL** : ouvrir http://localhost:8000/soap dans un navigateur.

Résultat attendu : le WSDL s'affiche, avec les quatre parties `message`, `portType` (opération `Add`), `binding` et `service`.

**Terminal 2 (appel)** :

```bash
curl -X POST http://localhost:8000/soap \
  -H "Content-Type: text/xml" \
  -d '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><Add><a>5</a><b>7</b></Add></soapenv:Body></soapenv:Envelope>'
```

Résultat attendu :

```xml
<?xml version="1.0"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body>
    <AddResponse xmlns="http://calculator.example/">
      <result>12</result>
    </AddResponse>
  </soapenv:Body>
</soapenv:Envelope>
```

À retenir : une seule URL (`POST /soap`) pour toutes les opérations, et une réponse de 251 octets pour transporter « 12 ».

---

## 2. REST

**Terminal 1 (serveur)** :

```bash
cd rest
uvicorn rest-server:app --port 8001
```

**Terminal 2 (appels)** :

```bash
curl "http://localhost:8001/add?a=5&b=7"
```

Résultat attendu :

```json
{"result":12}
```

Appel avec un paramètre manquant :

```bash
curl -i "http://localhost:8001/add?a=5"
```

Résultat attendu : `HTTP/1.1 422 Unprocessable Entity`, avec un JSON indiquant que le paramètre `b` est manquant.

**Documentation générée automatiquement** : ouvrir http://localhost:8001/docs dans un navigateur.

Résultat attendu : la page Swagger UI (OpenAPI) avec la route `GET /add`. Le JSON brut est sur http://localhost:8001/openapi.json.

À retenir : la réponse tient en une ligne de 13 octets, et l'erreur passe par le code HTTP.

---

## 3. GraphQL

**Terminal 1 (serveur)** :

```bash
cd graphql
uvicorn graphql_server:app --port 8002
```

**Terminal 2 (appels)**. Même URL, mais des champs différents :

```bash
curl -s -X POST http://localhost:8002/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ calcul(a: 5, b: 7) { somme } }"}'
```

Résultat attendu :

```json
{"data":{"calcul":{"somme":12}}}
```

```bash
curl -s -X POST http://localhost:8002/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ calcul(a: 5, b: 7) { somme produit } }"}'
```

Résultat attendu :

```json
{"data":{"calcul":{"somme":12,"produit":35}}}
```

Champ inexistant :

```bash
curl -s -i -X POST http://localhost:8002/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ calcul(a: 5, b: 7) { division } }"}'
```

Résultat attendu : `HTTP/1.1 200 OK` (et non 4xx), avec :

```json
{"data":null,"errors":[{"message":"Cannot query field 'division' on type 'Calcul'.","locations":[{"line":1,"column":24}]}]}
```

**Interface graphique** : ouvrir http://localhost:8002/graphql dans un navigateur (GraphiQL), puis saisir :

```graphql
{
  calcul(a: 5, b: 7) {
    somme
    produit
  }
}
```

Cliquer sur le bouton ▶. L'autocomplétion (Ctrl+Espace) propose les champs du schéma.

À retenir : c'est le client qui choisit les champs, et les erreurs sont renvoyées avec un code 200.

---

## 4. gRPC

**Générer le code à partir du contrat** (une seule fois) :

```bash
cd grpc
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto
ls
```

Résultat attendu : deux fichiers générés, `calculator_pb2.py` (les messages) et `calculator_pb2_grpc.py` (le stub et la base du serveur).

**Terminal 1 (serveur)** :

```bash
cd grpc
python grpc_server.py
```

Résultat attendu : `Serveur gRPC en écoute sur le port 50051`.

**Terminal 2 (client)** :

```bash
cd grpc
python grpc_client.py
```

Résultat attendu :

```
Résultat : 12
Requête sérialisée : 4 octets -> 08 05 10 07
Réponse sérialisée : 2 octets -> 08 0c
```

À retenir : les messages sont binaires et minuscules (2 octets pour la réponse), mais impossibles à lire ou à tester avec curl sans le fichier `.proto`.

---

## Récapitulatif : taille de la réponse « 12 »

| SOAP | REST | GraphQL | gRPC |
|---|---|---|---|
| 251 octets | 13 octets | 32 octets | 2 octets |

## En cas de problème

- `command not found: uvicorn` ou `ModuleNotFoundError` : l'environnement virtuel n'est pas activé (`source venv/bin/activate`).
- `FileNotFoundError: calculator.wsdl` : le serveur SOAP n'a pas été lancé depuis le dossier `soap/`.
- `ModuleNotFoundError: calculator_pb2` : le code gRPC n'a pas été généré (voir l'étape `protoc`).
- `address already in use` : un serveur tourne déjà sur ce port. L'arrêter avec Ctrl+C dans son terminal.
