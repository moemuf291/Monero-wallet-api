# Monero Escrow API

A production-ready, role-based escrow API backend in Python using Flask.  
**Note:** This version tracks escrow agreements in the database but does not move real funds.

**Data in the instance/escrow.db is not real its simply testing data

---

## Features

- **API key authentication** via `X-API-Key` header
- **Role-based access control** (`user` and `admin`)
- **Escrow management:** create, check status, release, refund
- **SQLAlchemy ORM** for database
- **Marshmallow** for validation
- **CORS enabled** for frontend integration
- **Ready for Monero wallet integration (future)**

---



---

## Setup

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd monero-escrow
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Set up environment variables

- Copy `.env.example` to `.env` and adjust as needed.

### 4. Initialize the database and create users

- Create a user or admin API key using the script below.

### 5. Run the Flask app

```sh
python run.py
```

---

## Creating User and Admin API Keys

Use the combined script below to create either a user or admin API key.

**File:** `create_api_user.py`



**Usage:**

- To create a user API key:
  ```sh
  python create_api_user.py user
  ```
- To create an admin API key:
  ```sh
  python create_api_user.py admin
  ```
- To specify a custom name:
  ```sh
  python create_api_user.py admin alice_admin
  python create_api_user.py user bob_user
  ```

The script will print the API key to your terminal.  
Copy and use this key in your API requests!

---

## API Usage

### Authentication

All endpoints require an `X-API-Key` header with a valid API key.

---

### Endpoints

#### 1. Create Escrow (User or Admin)

- **POST** `/api/v1/escrow/create`
- **Headers:** `X-API-Key: <user or admin key>`
- **Body:**
  ```json
  {
    "buyer_id": "buyer1",
    "seller_id": "seller1",
    "amount": "1.23"
  }
  ```
- **Response:** Escrow details (JSON)

**Example curl:**
```sh
curl -X POST http://127.0.0.1:5000/api/v1/escrow/create \
  -H "X-API-Key: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{"buyer_id": "buyer1", "seller_id": "seller1", "amount": "1.23"}'
```

---

#### 2. Check Escrow Status (User or Admin)

- **GET** `/api/v1/escrow/status/<uuid>`
- **Headers:** `X-API-Key: <user or admin key>`
- **Response:** Escrow details (JSON)

**Example curl:**
```sh
curl -X GET http://127.0.0.1:5000/api/v1/escrow/status/<uuid> \
  -H "X-API-Key: <your_api_key>"
```

---

#### 3. Release Escrow (Admin Only)

- **POST** `/api/v1/escrow/release/<uuid>`
- **Headers:** `X-API-Key: <admin key>`
- **Response:** Updated escrow details (JSON)
- **Note:** Escrow must have status `funded`.

**Example curl:**
```sh
curl -X POST http://127.0.0.1:5000/api/v1/escrow/release/<uuid> \
  -H "X-API-Key: <your_admin_api_key>"
```

---

#### 4. Refund Escrow (Admin Only)

- **POST** `/api/v1/escrow/refund/<uuid>`
- **Headers:** `X-API-Key: <admin key>`
- **Response:** Updated escrow details (JSON)
- **Note:** Escrow must have status `funded`.

**Example curl:**
```sh
curl -X POST http://127.0.0.1:5000/api/v1/escrow/refund/<uuid> \
  -H "X-API-Key: <your_admin_api_key>"
```

---
## Escrow Statuses and How to Fund an Escrow

### Status Summary Table

| Status           | Meaning                                      | What you can do                |
|------------------|----------------------------------------------|--------------------------------|
| waiting_payment  | Escrow created, waiting for payment/funding  | Nothing (wait/fund)            |
| funded           | Escrow has been funded (buyer paid)          | Admin can release or refund    |
| completed        | Escrow released to seller                    | Done                           |
| refunded         | Escrow refunded to buyer                     | Done                           |

---

### How to Fund (Simulate Funding) an Escrow

In this system, "funded" means the buyer has paid.  
For testing, you can manually set an escrow’s status to `funded` in the database.

**Steps:**

1. Open your terminal and navigate to your database directory:
    ```sh
    cd instance
    sqlite3 escrow.db
    ```

2. At the `sqlite>` prompt, run:
    ```sql
    UPDATE escrow_transactions SET status='funded' WHERE id='<ESCROW_UUID>';
    ```

    Replace `<ESCROW_UUID>` with the actual UUID of your escrow.

3. (Optional) Check the status:
    ```sql
    SELECT id, status FROM escrow_transactions WHERE id='<ESCROW_UUID>';
    ```

    You should see:
    ```
    <ESCROW_UUID>|funded
    ```

---

**Once the escrow is funded, an admin can release or refund it using the appropriate API endpoint.**

## User vs. Admin

| Role   | Can Create Escrow | Can Check Status | Can Release/Refund |
|--------|-------------------|------------------|-------------------|
| User   | Yes               | Yes              | No                |
| Admin  | Yes               | Yes              | Yes               |

- **API keys** are generated and stored in the `api_users` table.
- Use the script `create_api_user.py` to create users and get their API keys.

---

## What to Expect

- **Creating an escrow** logs the transaction in the database (no real money is moved).
- **Checking status** returns the escrow’s current state.
- **Releasing/refunding** changes the status in the database (admin only, and only if status is `funded`).
- **No real Monero is moved**—this is a secure, role-based escrow record system ready for future integration with Monero wallet RPC.

---

## Database Usage

### Where is the database?
- By default, it’s at `instance/escrow.db` (SQLite).

### How to view/edit the database:

#### A. Using DB Browser for SQLite (GUI)
- Download from [sqlitebrowser.org](https://sqlitebrowser.org/dl/)
- Open `instance/escrow.db`
- Browse and edit tables (`escrow_transactions`, `api_users`)

#### B. Using the SQLite Command Line
```sh
cd instance
sqlite3 escrow.db
```
- List tables:
  ```sql
  .tables
  ```
- Show all escrows:
  ```sql
  SELECT * FROM escrow_transactions;
  ```
- Show all users:
  ```sql
  SELECT * FROM api_users;
  ```
- Update status (simulate funding for testing release/refund):
  ```sql
  UPDATE escrow_transactions SET status='funded' WHERE id='<uuid>';
  ```

#### C. Using Python
```python
import sqlite3
conn = sqlite3.connect('instance/escrow.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM escrow_transactions;")
print(cursor.fetchall())
conn.close()
```

---

## CORS (Frontend Integration)

- CORS is enabled by default, so you can build a separate frontend (HTML/JS, React, etc.) that calls the API.

---

## Security

- All endpoints require a valid API key.
- Only admins can release or refund escrows.
- All actions are logged in the database.

---

## Extending the System

- Integrate with Monero wallet RPC for real payment handling.
- Add user registration and authentication.
- Build a frontend dashboard for users/admins.

## System Architecture: How the Monero Escrow API Works

Your escrow system is made up of several components that work together to securely manage escrow transactions. Here’s how each part fits in:

---

### **Component Overview**

| Component             | What it Does                                                                                   |
|-----------------------|-----------------------------------------------------------------------------------------------|
| **User**              | Interacts with your API (e.g., via web, app, or curl) to create/check/release escrows.        |
| **Escrow API (Flask)**| Handles business logic, stores escrow records, and communicates with the Monero wallet RPC.   |
| **monero-wallet-rpc** | Manages a Monero wallet, creates subaddresses, checks for payments, and sends transactions.   |
| **monerod**           | Syncs with the Monero blockchain and relays transactions/blocks to and from the network.      |
| **Monero Blockchain** | The decentralized ledger where all Monero transactions are recorded.                          |

---

### **How Data Flows**

1. **User** sends a request to your **Escrow API** (e.g., to create an escrow).
2. **Escrow API** sends a JSON-RPC request to **monero-wallet-rpc** (e.g., to create a subaddress or check for payment).
3. **monero-wallet-rpc** communicates with **monerod** to get blockchain data or broadcast transactions.
4. **monerod** syncs with the **Monero blockchain** and relays information back up the chain.

---

### **Architecture Diagram**

```mermaid
graph TD
    
```

---

### **Summary**

- The **User** never talks directly to the blockchain.
- The **Escrow API** is the only component your users interact with.
- The **Escrow API** talks to **monero-wallet-rpc** for all Monero wallet operations.
- **monero-wallet-rpc** talks to **monerod** for blockchain data and transaction broadcasting.
- **monerod** syncs with the **Monero blockchain** network.

---




## How to Get the Admin and User API Keys

API keys are required for all requests to the Monero Escrow API.  
Each user (admin or regular) has a unique API key stored in the `api_users` table.

### 1. Create a User or Admin API Key

Use the provided script `create_api_user.py` to create either a user or admin API key.

**Usage:**

- To create a user API key:
  ```sh
  python create_api_user.py user
  ```
- To create an admin API key:
  ```sh
  python create_api_user.py admin
  ```
- To specify a custom name:
  ```sh
  python create_api_user.py admin alice_admin
  python create_api_user.py user bob_user
  ```

The script will print the API key to your terminal.  
Copy and use this key in your API requests!

---

### 2. View All API Keys in the Database

You can also view all API keys directly in the database.

**Using SQLite command line:**

```sh
sqlite3 instance/escrow.db
```
Then at the `sqlite>` prompt:

```sql
SELECT id, name, api_key, role FROM api_users;
```

**Using DB Browser for SQLite:**

- Open `instance/escrow.db`
- Browse the `api_users` table to see all API keys and roles.

---

### 3. Using the API Key

For every API request, add a header:



## Escrow UUID and API Usage Examples

### What is `escrow_uuid`?

- The `escrow_uuid` is the unique identifier (UUID) for each escrow transaction.
- It is generated by the API when you create a new escrow.
- You will find it in the `"id"` field of the JSON response when you create an escrow, or in the `id` column of the `escrow_transactions` table in your database.

**Example create response:**
```json
{
  "id": "415bf99f-5bd9-4966-9bb7-dba7c38d5c83",
  "buyer_id": "buyer1",
  "seller_id": "seller1",
  "amount": "1.23",
  "status": "waiting_payment",
  ...
}
```
Here, `415bf99f-5bd9-4966-9bb7-dba7c38d5c83` is the `escrow_uuid`.

---






### Summary Table

| Action           | curl Command Example                                                                                  | What it Does                                      |
|------------------|------------------------------------------------------------------------------------------------------|---------------------------------------------------|
| Create Escrow    | See [Create Escrow Transaction](#1-create-escrow-transaction-user-or-admin)                          | Creates a new escrow and returns its UUID         |
| Check Status     | See [Check Escrow Status](#2-check-escrow-status-user-or-admin)                                      | Shows the status/details of a specific escrow     |
| Release Escrow   | See [Release Escrow](#3-release-escrow-admin-only)                                                   | Admin marks escrow as completed                   |
| Refund Escrow    | See [Refund Escrow](#4-refund-escrow-admin-only)                                                     | Admin marks escrow as refunded                    |
| Set as Funded    | See [Manually Set Escrow as Funded](#5-optional-manually-set-escrow-as-funded-for-testing)           | Simulates payment by updating status in database  |

---

**Remember:**  
- The `escrow_uuid` is the unique ID for each escrow, found in the `"id"` field of the create response or in the database.
- Always use the correct API key for the action (user or admin).

---

## License

MIT (or your chosen license)

---


