# Boards Endpoints

1. Create a Board (POST /boards/)

Input: JSON object with a name field (e.g., {"name": "Project A"}).

Output: JSON object with the ID of the newly created board (e.g., {"id": "648d1..."}).


2. Get All Boards (GET /boards/)

Input: None.

Output: List of all boards, including their IDs, names, and lists (names and IDs) (e.g., [{ "_id": "648d1...", "name": "Project A", "lists": [{"id": "648e2...", "name": "To Do"}] }]).


3. Get a Single Board (GET /boards/<board_id>)

Input: board_id (as a URL parameter).

Output: JSON object of the board with its ID, name, and lists (names and IDs) (e.g., {"_id": "648d1...", "name": "Project A", "lists": [{"id": "648e2...", "name": "To Do"}]}).


4. Update a Board (PUT /boards/<board_id>)

Input: board_id (as a URL parameter), JSON object with name (e.g., {"name": "Updated Board Name"}).

Output: Success message (e.g., {"message": "Board updated successfully"}).


5. Delete a Board (DELETE /boards/<board_id>)

Input: board_id (as a URL parameter).

Output: Success message (e.g., {"message": "Board deleted successfully"}).


6. Create a List in a Board (POST /boards/<board_id>/lists)

Input: board_id (as a URL parameter), JSON object with name (e.g., {"name": "To Do"}).

Output: JSON object with the ID and name of the newly created list (e.g., {"id": "648e2...", "name": "To Do"}).


7. Get All Lists in a Board (GET /boards/<board_id>/lists)

Input: board_id (as a URL parameter).

Output: List of lists in the board, including IDs and names (e.g., [{"_id": "648e2...", "name": "To Do"}]).



# Lists Endpoints

1. Update a List (PUT /lists/<list_id>)

Input: list_id (as a URL parameter), JSON object with name (e.g., {"name": "Updated List Name"}).

Output: Success message (e.g., {"message": "List updated successfully"}).


2. Delete a List (DELETE /lists/<list_id>)

Input: list_id (as a URL parameter).

Output: Success message (e.g., {"message": "List deleted successfully"}).


3. Create a Card in a List (POST /lists/<list_id>/cards)

Input: list_id (as a URL parameter), JSON object with title and optionally description (e.g., {"title": "Task 1", "description": "Details"}).

Output: JSON object with the ID, title, and description of the newly created card (e.g., {"id": "648f3...", "title": "Task 1", "description": "Details"}).


4. Get All Cards in a List (GET /lists/<list_id>/cards)

Input: list_id (as a URL parameter).

Output: List of cards in the list, including IDs, titles, and descriptions (e.g., [{"_id": "648f3...", "title": "Task 1", "description": "Details"}]).



# Cards Endpoints

1. Get a Card (GET /cards/<card_id>)

Input: card_id (as a URL parameter).

Output: JSON object with the card’s details (e.g., {"_id": "648f3...", "title": "Task 1", "description": "Details"}).


2. Update a Card (PUT /cards/<card_id>)

Input: card_id (as a URL parameter), JSON object with title and/or description (e.g., {"title": "Updated Task"}).

Output: Success message (e.g., {"message": "Card updated successfully"}).


3. Delete a Card (DELETE /cards/<card_id>)

Input: card_id (as a URL parameter).

Output: Success message (e.g., {"message": "Card deleted successfully"}).