# Mermaid Diagram Patterns

Reference patterns for creating consistent diagrams across documentation.

---

## ER Diagrams (Entity Relationships)

### Full Project ER Diagram

Use in `docs/data-model/_overview.md`:

```mermaid
erDiagram
    %% Core Entities
    USERS {
        int id PK
        string email UK
        string name
        timestamp created_at
    }

    ORDERS {
        int id PK
        int user_id FK
        decimal total
        string status
        timestamp created_at
    }

    ORDER_ITEMS {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal price
    }

    PRODUCTS {
        int id PK
        string name
        decimal price
        int stock
    }

    %% Relationships
    USERS ||--o{ ORDERS : "places"
    ORDERS ||--|{ ORDER_ITEMS : "contains"
    PRODUCTS ||--o{ ORDER_ITEMS : "included in"
```

### Relationship Cardinality Symbols

| Symbol | Meaning |
|--------|---------|
| `\|\|` | Exactly one |
| `o\|` | Zero or one |
| `}o` | Zero or many |
| `}\|` | One or many |
| `\|{` | One or many (other direction) |
| `o{` | Zero or many (other direction) |

### Common Relationship Patterns

```mermaid
erDiagram
    %% One-to-Many (most common)
    PARENT ||--o{ CHILD : "has many"

    %% Many-to-Many (via junction table)
    ENTITY_A }o--o{ JUNCTION : ""
    ENTITY_B }o--o{ JUNCTION : ""

    %% One-to-One
    USER ||--|| PROFILE : "has one"

    %% Self-referential
    EMPLOYEE }o--o| EMPLOYEE : "reports to"
```

---

## Flowcharts (ETL Pipeline)

### Pipeline Overview

Use in `docs/workflows/etl/_pipeline-overview.md`:

```mermaid
flowchart TB
    subgraph Sources["Data Sources"]
        S1[(Oracle DB)]
        S2[(PostgreSQL)]
        S3[/CSV Files/]
        S4{{External API}}
    end

    subgraph ETL["ETL Pipeline"]
        E1[Step 1: Extract]
        E2[Step 2: Validate]
        E3[Step 3: Transform]
        E4[Step 4: Enrich]
        E5[Step 5: Load]
    end

    subgraph Destinations["Destinations"]
        D1[(Data Warehouse)]
        D2[/Reports/]
        D3{{Downstream API}}
    end

    S1 --> E1
    S2 --> E1
    S3 --> E1
    S4 --> E4

    E1 --> E2 --> E3 --> E4 --> E5

    E5 --> D1
    E5 --> D2
    E5 --> D3

    style E3 fill:#f9f,stroke:#333
```

### Single Step Detail

Use in individual step files:

```mermaid
flowchart TD
    A[Input: Raw Data] --> B{Validation}
    B -->|Valid| C[Transform]
    B -->|Invalid| D[Error Log]

    C --> E{Business Rules}
    E -->|Rule 1| F[Apply Rule 1]
    E -->|Rule 2| G[Apply Rule 2]

    F --> H[Merge Results]
    G --> H

    H --> I[Output: Processed Data]

    style C fill:#bbf,stroke:#333
    style H fill:#bfb,stroke:#333
```

### Parallel Processing

```mermaid
flowchart TD
    A[Start] --> B[Split Data]

    B --> C1[Process Batch 1]
    B --> C2[Process Batch 2]
    B --> C3[Process Batch 3]

    C1 --> D[Merge Results]
    C2 --> D
    C3 --> D

    D --> E[End]
```

---

## Sequence Diagrams (API Flows)

### Basic API Request

Use in API endpoint documentation:

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API Gateway
    participant S as Service
    participant D as Database
    participant Ca as Cache

    C->>A: GET /api/resource
    A->>A: Validate JWT

    A->>Ca: Check cache
    alt Cache hit
        Ca-->>A: Cached data
        A-->>C: 200 OK (cached)
    else Cache miss
        A->>S: Forward request
        S->>D: Query data
        D-->>S: Results
        S->>Ca: Store in cache
        S-->>A: Response
        A-->>C: 200 OK
    end
```

### Complex Transaction

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant O as Order Service
    participant I as Inventory
    participant P as Payment
    participant N as Notification

    C->>A: POST /orders
    A->>O: Create order

    O->>I: Reserve inventory
    alt Inventory available
        I-->>O: Reserved
        O->>P: Process payment
        alt Payment success
            P-->>O: Confirmed
            O->>N: Send confirmation
            N-->>O: Sent
            O-->>A: Order created
            A-->>C: 201 Created
        else Payment failed
            P-->>O: Failed
            O->>I: Release inventory
            O-->>A: Payment failed
            A-->>C: 402 Payment Required
        end
    else Out of stock
        I-->>O: Unavailable
        O-->>A: Out of stock
        A-->>C: 409 Conflict
    end
```

---

## State Diagrams (Entity Lifecycle)

### Order Status Flow

```mermaid
stateDiagram-v2
    [*] --> Draft: Create order

    Draft --> Pending: Submit
    Draft --> Cancelled: Cancel

    Pending --> Processing: Payment received
    Pending --> Cancelled: Cancel/Timeout

    Processing --> Shipped: Ship order
    Processing --> Cancelled: Refund

    Shipped --> Delivered: Confirm delivery
    Shipped --> Returned: Return initiated

    Delivered --> [*]
    Returned --> Refunded: Process return
    Refunded --> [*]
    Cancelled --> [*]
```

---

## Class Diagrams (Code Structure)

### Service Architecture

```mermaid
classDiagram
    class BaseService {
        <<abstract>>
        +db: Session
        +logger: Logger
        +validate(data)
        +execute()*
    }

    class OrderService {
        +create_order(data)
        +get_order(id)
        +update_status(id, status)
    }

    class InventoryService {
        +check_stock(product_id)
        +reserve(product_id, qty)
        +release(product_id, qty)
    }

    class PaymentService {
        +process(order_id, amount)
        +refund(payment_id)
    }

    BaseService <|-- OrderService
    BaseService <|-- InventoryService
    BaseService <|-- PaymentService

    OrderService --> InventoryService: uses
    OrderService --> PaymentService: uses
```

---

## Styling Guidelines

### Color Conventions

| Element | Color | Hex | Use For |
|---------|-------|-----|---------|
| Current/Focus | Pink | `#f9f` | Highlighted element |
| Input | Light blue | `#bbf` | Data sources |
| Output | Light green | `#bfb` | Data destinations |
| Error | Light red | `#fbb` | Error paths |
| Success | Light green | `#bfb` | Success paths |

### Applying Styles

```mermaid
flowchart TD
    A[Normal] --> B[Highlighted]
    B --> C[Success]
    B --> D[Error]

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#bfb,stroke:#393
    style D fill:#fbb,stroke:#933
```

### Subgraph Styling

```mermaid
flowchart TB
    subgraph External["External Systems"]
        direction LR
        E1[System A]
        E2[System B]
    end

    subgraph Internal["Internal Services"]
        direction TB
        I1[Service 1]
        I2[Service 2]
    end

    E1 --> I1
    E2 --> I2

    style External fill:#e6f3ff,stroke:#0066cc
    style Internal fill:#e6ffe6,stroke:#006600
```

---

## Tips

1. **Keep diagrams focused**: One concept per diagram
2. **Use consistent naming**: Match entity/table names exactly
3. **Add legends** when using custom colors
4. **Test rendering**: Mermaid syntax can be finicky
5. **Prefer flowcharts** for processes, ER for data, sequence for interactions
