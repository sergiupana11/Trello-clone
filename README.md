# Setup

## 1. Create a virtual environment
```bash
python -m venv .venv
```

## 2. Activate venv
```bash
source .venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Start MongoDB Docker image
```bash
docker pull mongodb/mongodb-community-server:latest

docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest

# check that the container has started using this commands (you will need to install mongosh)
mongosh --port 27017

db.runCommand(
   {
      hello: 1
   }
)
```
## 5. Run the application
```bash
python app.py
```
